# tests/test_refactoring.py
import pytest
import os
from core.validators.master_validator import validate_resource, VALIDATOR_REGISTRY
from agents.knowledge_memory_agent import TFIDFMatcher, recall_memories
from core.graph import compile_learning_content_workflow

def test_master_validator_registry():
    # Verify that validators have been registered dynamically after importing
    from core.validators.master_validator import _ensure_validators_imported
    _ensure_validators_imported()
    assert len(VALIDATOR_REGISTRY) > 0
    assert "READING" in VALIDATOR_REGISTRY
    assert "QUIZ" in VALIDATOR_REGISTRY
    assert "PRACTICE" in VALIDATOR_REGISTRY
    assert "PROJECT" in VALIDATOR_REGISTRY
    assert "COMPILED_SESSION" in VALIDATOR_REGISTRY

def test_tfidf_matcher_logic():
    # Verify semantic TF-IDF calculation and Cosine similarity
    documents = [
        "Vòng lặp for dùng để duyệt qua các phần tử trong danh sách.",
        "Cú pháp if else dùng để rẽ nhánh điều kiện logic trong chương trình.",
        "Hàm function giúp đóng gói và tái sử dụng mã nguồn."
    ]
    matcher = TFIDFMatcher(documents)
    
    # Query related to loops
    scores_loop = matcher.get_similarity("Làm thế nào để lặp qua list?")
    assert scores_loop[0] > scores_loop[1]
    assert scores_loop[0] > scores_loop[2]
    
    # Query related to conditions
    scores_cond = matcher.get_similarity("Kiểm tra điều kiện if else.")
    assert scores_cond[1] > scores_cond[0]
    assert scores_cond[1] > scores_cond[2]

def test_graph_compilation():
    # Verify that the new graph compiles without error
    workflow = compile_learning_content_workflow()
    assert workflow is not None
    # Check that new node exists in registry
    assert "generate_blueprint" in workflow.nodes
