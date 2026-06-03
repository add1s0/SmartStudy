from django.contrib.auth.models import User
from django.db import models


class StudyMaterial(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    content = models.TextField()
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title 


class QuizQuestion(models.Model):
   
    material = models.ForeignKey(
        StudyMaterial, on_delete=models.CASCADE, related_name="quiz_questions"
    )
    question = models.CharField(max_length=300)
    correct_answer = models.CharField(max_length=300)
    wrong_answer1 = models.CharField(max_length=300)
    wrong_answer2 = models.CharField(max_length=300)
    wrong_answer3 = models.CharField(max_length=300)

    def __str__(self) -> str:
        return self.question


class QuizResult(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    material = models.ForeignKey(
        StudyMaterial, on_delete=models.CASCADE, related_name="quiz_results"
    )
    score = models.PositiveIntegerField()
    total_questions = models.PositiveIntegerField()
    percentage = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}: {self.material.title} ({self.percentage:.0f}%)"


class Exam(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=100)
    exam_date = models.DateField()
    material = models.ForeignKey(
        StudyMaterial, on_delete=models.CASCADE, related_name="exams"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title
