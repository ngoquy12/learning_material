# core/vector_store.py
import os
import json
import math
from typing import List, Dict, Any

class LightweightVectorStore:
    """
    A lightweight, zero-dependency Vector Store that runs locally.
    Uses Gemini or OpenAI embeddings for vector search,
    with a fallback TF-IDF/BM25 keyword search if no API keys are present.
    """
    def __init__(self, storage_path: str = "vector_store.json"):
        self.storage_path = storage_path
        self.documents = []  # List[Dict[str, Any]] -> {"text": str, "vector": List[float], "metadata": Dict}
        self.load()

    def load(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    self.documents = json.load(f)
            except Exception as e:
                print(f"  [VectorStore Warning] Failed to load store: {e}")
                self.documents = []

    def save(self):
        try:
            with open(self.storage_path, "w", encoding="utf-8") as f:
                json.dump(self.documents, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"  [VectorStore Warning] Failed to save store: {e}")

    def _get_embedding(self, text: str) -> List[float]:
        """Call Gemini or OpenAI to get vector embedding, or return empty list for local TF-IDF search."""
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")

        # Skip remote embedding if using local proxy or invalid key to avoid noisy API key errors
        base_url = os.getenv("GEMINI_BASE_URL", "")
        if "127.0.0.1" in base_url or "localhost" in base_url:
            return []

        if gemini_key and gemini_key.strip() != "dummy":
            try:
                import google.generativeai as genai  # type: ignore
                genai.configure(
                    api_key=gemini_key,
                    client_options={"api_endpoint": base_url} if base_url else None,
                    transport="rest"
                )
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document"
                )
                return result.get("embedding", [])
            except Exception:
                return []

        return []

        if openai_key:
            try:
                from openai import OpenAI  # type: ignore
                client = OpenAI(api_key=openai_key)
                response = client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                return response.data[0].embedding
            except Exception as e:
                print(f"  [VectorStore LLM Warning] OpenAI embedding failed: {e}")

        return []

    def add_documents(self, docs_with_metadata: List[Dict[str, Any]]):
        """Adds documents, embeds them, and persists to disk."""
        updated = False
        for doc in docs_with_metadata:
            text = doc.get("text", "").strip()
            if not text:
                continue
            
            # Prevent duplicates
            if any(existing["text"] == text for existing in self.documents):
                continue
                
            vector = self._get_embedding(text)
            self.documents.append({
                "text": text,
                "vector": vector,
                "metadata": doc.get("metadata", {})
            })
            updated = True
            
        if updated:
            self.save()

    def _cosine_similarity(self, v1: List[float], v2: List[float]) -> float:
        if not v1 or not v2 or len(v1) != len(v2):
            return 0.0
        dot_product = sum(a * b for a, b in zip(v1, v2))
        norm1 = math.sqrt(sum(a * a for a in v1))
        norm2 = math.sqrt(sum(b * b for b in v2))
        if norm1 == 0.0 or norm2 == 0.0:
            return 0.0
        return dot_product / (norm1 * norm2)

    def _bm25_score(self, query_terms: List[str], doc_text: str, avgdl: float, total_docs: int, term_doc_counts: Dict[str, int], k1: float = 1.5, b: float = 0.75) -> float:
        """BM25 sparse keyword ranking score."""
        doc_words = doc_text.lower().split()
        doc_len = len(doc_words)
        if doc_len == 0 or avgdl == 0:
            return 0.0

        # Term frequencies in document
        tf_map = {}
        for w in doc_words:
            tf_map[w] = tf_map.get(w, 0) + 1

        score = 0.0
        for term in query_terms:
            if term not in tf_map:
                continue
            f = tf_map[term]
            n_q = term_doc_counts.get(term, 0)
            idf = math.log((total_docs - n_q + 0.5) / (n_q + 0.5) + 1.0)
            numerator = f * (k1 + 1.0)
            denominator = f + k1 * (1.0 - b + b * (doc_len / avgdl))
            score += idf * (numerator / denominator)

        return score

    def hybrid_query(self, query_text: str, k: int = 3, alpha: float = 0.5) -> List[Dict[str, Any]]:
        """
        Hybrid Search combining Dense Vector Cosine Similarity + Sparse BM25 Keyword Search.
        alpha (0.0 to 1.0): Weight of Dense Vector score vs Sparse BM25 score.
        """
        if not self.documents:
            return []

        query_terms = [t for t in query_text.lower().split() if len(t) > 1]
        total_docs = len(self.documents)
        
        # Calculate collection stats for BM25
        doc_lengths = [len(doc.get("text", "").lower().split()) for doc in self.documents]
        avgdl = sum(doc_lengths) / max(1, total_docs)

        term_doc_counts: Dict[str, int] = {}
        for term in set(query_terms):
            cnt = sum(1 for doc in self.documents if term in doc.get("text", "").lower())
            term_doc_counts[term] = cnt

        # Get dense query vector
        query_vector = self._get_embedding(query_text)

        raw_scores = []
        for doc in self.documents:
            doc_text = doc.get("text", "")
            
            # 1. Dense score
            dense_score = 0.0
            if query_vector and doc.get("vector"):
                dense_score = max(0.0, self._cosine_similarity(query_vector, doc.get("vector", [])))

            # 2. Sparse BM25 score
            bm25_score = self._bm25_score(query_terms, doc_text, avgdl, total_docs, term_doc_counts)
            
            raw_scores.append({
                "doc": doc,
                "dense": dense_score,
                "bm25": bm25_score
            })

        # Normalize BM25 scores to [0, 1] range
        max_bm25 = max((item["bm25"] for item in raw_scores), default=1.0)
        if max_bm25 == 0.0:
            max_bm25 = 1.0

        scored_docs = []
        for item in raw_scores:
            norm_bm25 = item["bm25"] / max_bm25
            norm_dense = item["dense"]  # Cosine is already in [0, 1]
            
            # Combine scores
            hybrid_score = (alpha * norm_dense) + ((1.0 - alpha) * norm_bm25)
            scored_docs.append((hybrid_score, item["doc"]))

        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored_docs[:k]]

    def query(self, query_text: str, k: int = 3) -> List[Dict[str, Any]]:
        """Queries the vector store using Hybrid Search (Dense + BM25)."""
        return self.hybrid_query(query_text=query_text, k=k, alpha=0.5)

