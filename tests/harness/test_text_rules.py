from core.harness.text_rules import (find_all_caps, find_banned_words,
                                      find_bracket_tags, find_emoji)


def test_text_rules():
    assert set(find_banned_words("Bí kíp thực chiến nhé")) == {"nhé", "thực chiến", "bí kíp"}
    assert find_banned_words("Nội dung bình thường") == []
    assert find_emoji("Xong ✅") == ["✅"]
    assert find_bracket_tags("[NOTE] và [userId]") == ["[NOTE]"]
    assert find_all_caps("API CRUD là gì") == []
    assert find_all_caps("CẢNH BÁO QUAN TRỌNG") != []
