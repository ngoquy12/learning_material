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
        """Call Gemini or OpenAI to get vector embedding."""
        gemini_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        openai_key = os.getenv("OPENAI_API_KEY") or os.getenv("LLM_API_KEY")

        if gemini_key:
            try:
                import google.generativeai as genai  # type: ignore
                base_url = os.getenv("GEMINI_BASE_URL")
                if base_url:
                    try:
                        genai.configure(
                            api_key=gemini_key,
                            client_options={"api_endpoint": base_url},
                            transport="rest"
                        )
                        result = genai.embed_content(
                            model="models/embedding-001",
                            content=text,
                            task_type="retrieval_document"
                        )
                        return result.get("embedding", [])
                    except Exception as proxy_err:
                        print(f"  [VectorStore Warning] Proxy embedding failed: {proxy_err}. Retrying directly with Google API...")
                
                # Direct call to Google Generative AI API (bypass proxy)
                genai.configure(
                    api_key=gemini_key,
                    client_options={"api_endpoint": "https://generativelanguage.googleapis.com"},
                    transport="rest"
                )
                result = genai.embed_content(
                    model="models/embedding-001",
                    content=text,
                    task_type="retrieval_document"
                )
                return result.get("embedding", [])
            except Exception as e:
                print(f"  [VectorStore LLM Warning] Gemini embedding failed: {e}")

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

    def _keyword_similarity(self, query: str, document: str) -> float:
        """Fallback TF-IDF/Overlap scorer."""
        query_words = set(query.lower().split())
        doc_words = document.lower().split()
        if not query_words or not doc_words:
            return 0.0
            
        # Term Frequency in document
        matches = sum(1 for w in doc_words if w in query_words)
        return matches / len(doc_words)

    def query(self, query_text: str, k: int = 3) -> List[Dict[str, Any]]:
        """Queries the vector store and returns top K matches."""
        if not self.documents:
            return []

        query_vector = self._get_embedding(query_text)
        results = []

        if query_vector:
            # Vector cosine similarity matching
            for doc in self.documents:
                sim = self._cosine_similarity(query_vector, doc.get("vector", []))
                results.append((sim, doc))
        else:
            # Fallback keyword overlap matching
            for doc in self.documents:
                sim = self._keyword_similarity(query_text, doc.get("text", ""))
                results.append((sim, doc))

        # Sort descending by similarity
        results.sort(key=lambda x: x[0], reverse=True)
        return [res[1] for res in results[:k]]
