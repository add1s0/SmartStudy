"""Tests for the local content generation helpers."""
from study.utils import generate_flashcards, generate_quiz_questions, generate_summary

SAMPLE_TEXT = (
    "Photosynthesis allows plants to turn light energy into chemical energy. "
    "Chlorophyll absorbs light inside plant cells. "
    "Plants use carbon dioxide and water during this process. "
    "Oxygen is released as a useful by-product."
)


def test_summary_uses_first_three_meaningful_sentences() -> None:
    """The summary should remain short and use the opening facts."""
    summary = generate_summary(SAMPLE_TEXT)

    assert "Photosynthesis allows plants" in summary
    assert "Plants use carbon dioxide" in summary
    assert "Oxygen is released" not in summary


def test_summary_returns_short_text_when_no_long_sentence_exists() -> None:
    """Short notes should still appear instead of producing an empty summary."""
    assert generate_summary("Very short.") == "Very short."


def test_flashcards_are_created_from_sentences() -> None:
    """Each meaningful fact should become one simple flashcard."""
    flashcards = generate_flashcards(SAMPLE_TEXT)

    assert len(flashcards) == 4
    assert flashcards[0]["question"].startswith("What is an important fact")
    assert "Photosynthesis" in flashcards[0]["answer"]


def test_quiz_questions_contain_four_answers() -> None:
    """Generated quiz dictionaries should include one correct and three wrong answers."""
    questions = generate_quiz_questions(SAMPLE_TEXT)

    assert len(questions) == 4
    assert questions[0]["correct_answer"].startswith("Photosynthesis")
    assert questions[0]["wrong_answer1"]
    assert questions[0]["wrong_answer2"]
    assert questions[0]["wrong_answer3"]
