import os
import json
import pytest
from core.llm import call_llm

def test_llm_as_a_judge():
    """
    Test Evaluation using LLM-as-a-judge pattern to verify the quality of generated learning materials.
    Requires GEMINI_API_KEY or OPENAI_API_KEY in the environment.
    """
    # Skip test if no API keys are present to avoid failing in CI environments without keys
    if not os.getenv("GEMINI_API_KEY") and not os.getenv("OPENAI_API_KEY") and not os.getenv("GOOGLE_API_KEY"):
        pytest.skip("No LLM API keys configured. Skipping LLM-as-a-judge test.")

    # A mock syllabus context and a mock generated learning material
    mock_syllabus = "Lesson: Python Variables. Topics covered: Declaration, integer, float, string."
    mock_generated_content = "<h2>Biến trong Python</h2><p>Để khai báo biến, ta dùng cú pháp <code>x = 10</code>. Ở đây x là một số nguyên (integer).</p>"

    system_prompt = (
        "Bạn là một chuyên gia sư phạm và kỹ sư phần mềm. "
        "Nhiệm vụ của bạn là đánh giá chất lượng học liệu dựa trên khung chương trình được cung cấp. "
        "Hãy xuất ra định dạng JSON với 2 trường: 'status' (APPROVED hoặc REJECTED) và 'feedback' (Lý do)."
    )

    user_prompt = f"""
    Khung chương trình:
    {mock_syllabus}

    Nội dung học liệu:
    {mock_generated_content}

    Hãy đánh giá xem nội dung học liệu có bám sát khung chương trình không.
    """

    response = call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
        json_mode=True,
        agent_name="LLM_Evaluator"
    )

    assert response is not None, "LLM returned empty response."
    try:
        clean_resp = response.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_resp)
        assert "status" in data, "'status' key missing from LLM JSON response"
        assert "feedback" in data, "'feedback' key missing from LLM JSON response"
        assert data["status"] in ["APPROVED", "REJECTED"], "Status must be APPROVED or REJECTED"
    except json.JSONDecodeError:
        pytest.fail(f"LLM did not return a valid JSON string. Response: {response}")
