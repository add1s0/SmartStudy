from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Exam, StudyMaterial


class RegisterForm(UserCreationForm):
    """Form used to create a student account."""

    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class StudyMaterialForm(forms.ModelForm):
    """Form for adding and editing study materials."""

    class Meta:
        model = StudyMaterial
        fields = ("title", "subject", "content")
        widgets = {"content": forms.Textarea(attrs={"rows": 10})}


class ExamForm(forms.ModelForm):
    """Form for adding an exam."""

    class Meta:
        model = Exam
        fields = ("title", "subject", "exam_date", "material")
        widgets = {"exam_date": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args: object, user: User | None = None, **kwargs: object) -> None:
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["material"].queryset = StudyMaterial.objects.filter(user=user)
