from core.harness.text_rules import (find_all_caps, find_banned_words,
                                      find_bracket_tags, find_emoji)


def test_text_rules():
    assert set(find_banned_words("Bí kíp thực chiến nhé")) == {"nhé", "thực chiến", "bí kíp"}
    assert find_banned_words("Nội dung bình thường") == []
    assert find_emoji("Xong ✅") == ["✅"]
    assert find_bracket_tags("[NOTE] và [userId]") == ["[NOTE]"]
    assert find_all_caps("API CRUD là gì") == []
    assert find_all_caps("CẢNH BÁO QUAN TRỌNG") != []


def test_deck_scripts_use_shared_text_rules():
    from core.harness import text_rules
    from core.harness.gates._skill_loader import load_skill_script
    for mod in (load_skill_script("slide_deck", "deck_lint"), load_skill_script("slide_deck", "check_deck")):
        assert mod.BANNED is text_rules.BANNED_WORDS
        assert mod.EMOJI is text_rules.EMOJI_RE
        assert mod.BRACKET_TAG is text_rules.BRACKET_TAG_RE
