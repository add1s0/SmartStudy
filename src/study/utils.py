"""Small text helpers used instead of an external AI service."""
import re


def _meaningful_sentences(text: str) -> list[str]:
    """Return cleaned sentences that contain enough words to be useful."""
    sentences = re.split(r"(?<=[.!?])\s+|\n+", text.strip())
    return [
        sentence.strip()
        for sentence in sentences
        if len(sentence.strip().split()) >= 4
    ]


def generate_summary(text: str) -> str:
    """Create a short summary from the first meaningful sentences."""
    sentences = _meaningful_sentences(text)
    if not sentences:
        return text.strip()
    return " ".join(sentences[:3])


def _flashcard_question(sentence: str) -> str:
    """Turn a sentence into a simple fill-in-the-blank question."""
    words = sentence.split()
    hidden_words = 1
    if words and words[0].lower() in {"a", "an", "the"} and len(words) > 1:
        hidden_words = 2
    visible_text = " ".join(words[hidden_words:])
    return f"Complete this statement from the material: _____ {visible_text}"


def generate_flashcards(text: str) -> list[dict]:
    """Create simple question-and-answer flashcards from meaningful sentences."""
    sentences = _meaningful_sentences(text)
    return [
        {
            "question": _flashcard_question(sentence),
            "answer": sentence,
        }
        for sentence in sentences[:5]
    ]


def generate_quiz_questions(text: str) -> list[dict]:
    """Create simple multiple-choice questions from meaningful sentences."""
    sentences = _meaningful_sentences(text)
    questions: list[dict] = []
    for index, sentence in enumerate(sentences[:5], start=1):
        questions.append(
            {
                "question": f"Which statement correctly describes topic {index}?",
                "correct_answer": sentence,
                "wrong_answer1": "This topic is not mentioned in the material.",
                "wrong_answer2": "The opposite of this statement is correct.",
                "wrong_answer3": "This statement belongs to a different subject.",
            }
        )
    return questions
