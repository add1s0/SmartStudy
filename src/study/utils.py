"""Small text helpers used instead of an external AI service."""
import random
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
    return f"Попълнете липсващата част: _____ {visible_text}"


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
    """Create more meaningful quiz questions from the material's sentences."""
    sentences = _meaningful_sentences(text)
    questions: list[dict] = []
    if len(sentences) < 2:
        return []

    for sentence in sentences[:5]:
        distractors = [s for s in sentences if s != sentence]
        if len(distractors) < 3:
            distractors.extend(
                [
                    "Това твърдение не е споменато в материала.",
                    "Обратното на това твърдение е вярно.",
                    "Това твърдение принадлежи към друг предмет.",
                ]
            )
        wrong_answers = random.sample(distractors, min(3, len(distractors)))

        questions.append(
            {
                "question": "Кое от следните твърдения е вярно според материала?",
                "correct_answer": sentence,
                "wrong_answer1": wrong_answers[0],
                "wrong_answer2": wrong_answers[1],
                "wrong_answer3": wrong_answers[2],
            }
        )
    return questions
