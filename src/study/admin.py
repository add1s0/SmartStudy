from django.contrib import admin

from .models import Exam, QuizQuestion, QuizResult, StudyMaterial

admin.site.register(StudyMaterial)
admin.site.register(QuizQuestion)
admin.site.register(QuizResult)
admin.site.register(Exam)
