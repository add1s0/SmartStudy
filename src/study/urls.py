from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("materials/", views.material_list, name="material_list"),
    path("materials/add/", views.material_create, name="material_create"),
    path("materials/<int:material_id>/", views.material_detail, name="material_detail"),
    path("materials/<int:material_id>/edit/", views.material_edit, name="material_edit"),
    path(
        "materials/<int:material_id>/delete/",
        views.material_delete,
        name="material_delete",
    ),
    path("quiz/<int:material_id>/", views.quiz_mode, name="quiz_mode"),
    path("exams/", views.exam_list, name="exam_list"),
    path("exams/add/", views.exam_create, name="exam_create"),
    path("exams/<int:exam_id>/", views.exam_detail, name="exam_detail"),
    path("statistics/", views.statistics, name="statistics"),
    path("focus/", views.focus_mode, name="focus_mode"),
]
