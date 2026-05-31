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


def generate_flashcards(text: str) -> list[dict]:
    """Create simple question-and-answer flashcards from meaningful sentences."""
    sentences = _meaningful_sentences(text)
    return [
        {
            "question": f"What is an important fact about topic {index}?",
            "answer": sentence,
        }
        for index, sentence in enumerate(sentences[:5], start=1)
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
