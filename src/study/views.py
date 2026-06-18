import random
from datetime import date

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExamForm, RegisterForm, StudyMaterialForm
from .models import Exam, QuizQuestion, QuizResult, StudyMaterial
from .utils import generate_quiz_questions, generate_summary

STUDY_PLAN = [
    "Преглед на материала",
    "Практика с тестове",
    "Преглед на грешките",
    "Крайно повторение",
]

OLD_QUIZ_PROMPTS = [
    "Which statement correctly describes",
    "Кое твърдение описва правилно тема",
]


def home(request: HttpRequest) -> HttpResponse:
    """Display the public landing page."""
    return render(request, "study/home.html")


def register(request: HttpRequest) -> HttpResponse:
    """Create a user account and log the student in."""
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})


@login_required
def dashboard(request: HttpRequest) -> HttpResponse:
    """Display a quick overview of the student's study data."""
    materials = StudyMaterial.objects.filter(user=request.user)
    exams = Exam.objects.filter(user=request.user).order_by("exam_date")
    context = {
        "total_materials": materials.count(),
        "total_exams": exams.count(),
        "nearest_exam": exams.filter(exam_date__gte=date.today()).first(),
    }
    return render(request, "study/dashboard.html", context)


@login_required
def material_list(request: HttpRequest) -> HttpResponse:
    """List only the signed-in student's materials."""
    materials = StudyMaterial.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "study/material_list.html", {"materials": materials})


def _get_user_material(request: HttpRequest, material_id: int) -> StudyMaterial:
    """Return a material only if it belongs to the signed-in user."""
    return get_object_or_404(StudyMaterial, id=material_id, user=request.user)


def _get_user_exam(request: HttpRequest, exam_id: int) -> Exam:
    """Return an exam only if it belongs to the signed-in user."""
    return get_object_or_404(Exam, id=exam_id, user=request.user)


def _average_quiz_score(material: StudyMaterial) -> float:
    """Return the material's average quiz score."""
    return material.quiz_results.aggregate(Avg("percentage"))["percentage__avg"] or 0


def _create_generated_content(material: StudyMaterial) -> None:
    """Create a summary and quiz questions for one material."""
    material.summary = generate_summary(material.content)
    material.save(update_fields=["summary"])
    QuizQuestion.objects.bulk_create(
        [
            QuizQuestion(material=material, **question)
            for question in generate_quiz_questions(material.content)
        ]
    )


def _ensure_localized_generated_content(material: StudyMaterial) -> None:
    """Regenerate study content if old prompts are still stored."""
    has_old_quiz_questions = any(
        material.quiz_questions.filter(question__contains=prompt).exists()
        for prompt in OLD_QUIZ_PROMPTS
    )
    if has_old_quiz_questions:
        material.quiz_questions.all().delete()
        _create_generated_content(material)


def _prepare_quiz_questions(questions: list[QuizQuestion]) -> None:
    """Add shuffled answer options to quiz questions for the template."""
    for question in questions:
        question.options = [
            question.correct_answer,
            question.wrong_answer1,
            question.wrong_answer2,
            question.wrong_answer3,
        ]
        random.shuffle(question.options)


def _calculate_quiz_score(request: HttpRequest, questions: list[QuizQuestion]) -> int:
    """Count the correct answers submitted by the user."""
    return sum(
        request.POST.get(f"question_{question.id}") == question.correct_answer
        for question in questions
    )


def _percentage(score: int, total: int) -> float:
    """Calculate percentage and avoid division by zero."""
    return (score / total * 100) if total else 0


def _quiz_recommendation(percentage: float) -> str:
    """Return a study recommendation based on a quiz percentage."""
    if percentage >= 80:
        return "Отлична подготовка"
    if percentage >= 50:
        return "Препоръчва се още повторение"
    return "Прегледай материала отново"


def _exam_recommendation(preparedness: float) -> str:
    """Return an exam recommendation based on preparedness."""
    if preparedness >= 80:
        return "Готов за изпит"
    if preparedness >= 50:
        return "Нуждае се от допълнителен преговор"
    return "Нуждаеш се от повече подготовка"


@login_required
def material_create(request: HttpRequest) -> HttpResponse:
    """Add material and automatically generate study activities."""
    if request.method == "POST":
        form = StudyMaterialForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.user = request.user
            material.save()
            _create_generated_content(material)
            return redirect("material_detail", material_id=material.id)
    else:
        form = StudyMaterialForm()
    return render(request, "study/material_form.html", {"form": form, "title": "Нов материал"})


@login_required
def material_detail(request: HttpRequest, material_id: int) -> HttpResponse:
    """Show one material owned by the signed-in student."""
    material = _get_user_material(request, material_id)
    return render(request, "study/material_detail.html", {"material": material})


@login_required
def material_edit(request: HttpRequest, material_id: int) -> HttpResponse:
    """Edit material and regenerate its activities when the text changes."""
    material = _get_user_material(request, material_id)
    if request.method == "POST":
        form = StudyMaterialForm(request.POST, instance=material)
        if form.is_valid():
            form.save()
            material.quiz_questions.all().delete()
            _create_generated_content(material)
            return redirect("material_detail", material_id=material.id)
    else:
        form = StudyMaterialForm(instance=material)
    return render(request, "study/material_form.html", {"form": form, "title": "Редактирай материал"})


@login_required
def material_delete(request: HttpRequest, material_id: int) -> HttpResponse:
    """Delete a material after confirmation."""
    material = _get_user_material(request, material_id)
    if request.method == "POST":
        material.delete()
        return redirect("material_list")
    return render(request, "study/material_confirm_delete.html", {"material": material})


@login_required
def quiz_mode(request: HttpRequest, material_id: int) -> HttpResponse:
    """Display a quiz, calculate its score, and save the result."""
    material = _get_user_material(request, material_id)
    _ensure_localized_generated_content(material)
    questions = list(material.quiz_questions.all())
    if request.method == "POST":
        score = _calculate_quiz_score(request, questions)
        total = len(questions)
        percentage = _percentage(score, total)
        QuizResult.objects.create(
            user=request.user,
            material=material,
            score=score,
            total_questions=total,
            percentage=percentage,
        )
        return render(
            request,
            "study/quiz_result.html",
            {
                "material": material,
                "score": score,
                "total": total,
                "percentage": percentage,
                "recommendation": _quiz_recommendation(percentage),
            },
        )
    _prepare_quiz_questions(questions)
    return render(request, "study/quiz_mode.html", {"material": material, "questions": questions})


@login_required
def exam_list(request: HttpRequest) -> HttpResponse:
    """List the student's exams."""
    exams = Exam.objects.filter(user=request.user).order_by("exam_date")
    return render(request, "study/exam_list.html", {"exams": exams})


@login_required
def exam_create(request: HttpRequest) -> HttpResponse:
    """Add an exam connected to one of the student's materials."""
    if request.method == "POST":
        form = ExamForm(request.POST, user=request.user)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.user = request.user
            exam.save()
            return redirect("exam_detail", exam_id=exam.id)
    else:
        form = ExamForm(user=request.user)
    return render(request, "study/exam_form.html", {"form": form})


@login_required
def exam_detail(request: HttpRequest, exam_id: int) -> HttpResponse:
    """Show exam readiness and a simple study plan."""
    exam = _get_user_exam(request, exam_id)
    preparedness = _average_quiz_score(exam.material)
    context = {
        "exam": exam,
        "days_remaining": (exam.exam_date - date.today()).days,
        "preparedness": preparedness,
        "recommendation": _exam_recommendation(preparedness),
        "study_plan": STUDY_PLAN,
    }
    return render(request, "study/exam_detail.html", context)


@login_required
def statistics(request: HttpRequest) -> HttpResponse:
    """Display study statistics for the signed-in student."""
    results = QuizResult.objects.filter(user=request.user)
    context = {
        "total_materials": StudyMaterial.objects.filter(user=request.user).count(),
        "total_quizzes": results.count(),
        "average_score": results.aggregate(Avg("percentage"))["percentage__avg"] or 0,
    }
    return render(request, "study/statistics.html", context)


@login_required
def focus_mode(request: HttpRequest) -> HttpResponse:
    """Display the Pomodoro timer."""
    return render(request, "study/focus_mode.html")
