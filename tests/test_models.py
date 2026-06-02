"""Basic model tests that do not require a database connection."""
from datetime import date

from django.contrib.auth.models import User

from study.models import Exam, QuizResult, StudyMaterial


def test_study_material_string_uses_title() -> None:
    """Materials should have a readable name in the admin site."""
    material = StudyMaterial(title="Biology Notes")

    assert str(material) == "Biology Notes"


def test_quiz_result_string_contains_student_and_percentage() -> None:
    """Quiz results should be easy to identify in the admin site."""
    user = User(username="alex")
    material = StudyMaterial(title="Physics Notes")
    result = QuizResult(user=user, material=material, percentage=80)

    assert str(result) == "alex: Physics Notes (80%)"


def test_exam_string_uses_title() -> None:
    """Exams should have a readable name in the admin site."""
    exam = Exam(title="Final Biology Exam", exam_date=date(2026, 6, 20))

    assert str(exam) == "Final Biology Exam"
