from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User

from .models import Exam, StudyMaterial


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Потребителско име")
    password = forms.CharField(label="Парола", widget=forms.PasswordInput)


class RegisterForm(UserCreationForm):
    """Form used to create a student account."""

    username = forms.CharField(label="Потребителско име")
    email = forms.EmailField(label="Имейл адрес", required=True)
    password1 = forms.CharField(label="Парола", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Потвърди парола", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")
        help_texts = {"username": None}


class StudyMaterialForm(forms.ModelForm):
    """Form for adding and editing study materials."""

    class Meta:
        model = StudyMaterial
        fields = ("title", "subject", "content")
        labels = {"title": "Заглавие", "subject": "Предмет", "content": "Съдържание"}
        widgets = {"content": forms.Textarea(attrs={"rows": 10})}


class ExamForm(forms.ModelForm):
    """Form for adding an exam."""

    class Meta:
        model = Exam
        fields = ("title", "subject", "exam_date", "material")
        labels = {
            "title": "Заглавие",
            "subject": "Предмет",
            "exam_date": "Дата на изпита",
            "material": "Материал",
        }
        widgets = {"exam_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args: object, user: User | None = None, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["material"].queryset = StudyMaterial.objects.filter(user=user)
