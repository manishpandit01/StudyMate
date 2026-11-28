
from django.urls import path
from . import views

urlpatterns = [
    path("signup/",views.signup_view,name="signup"),
    path("login/",views.login_view,name="login"),
    path("dashboard/",views.dashboard_view,name="dashboard"),
    path("logout/",views.logout_view,name="logout"),
    path("subjects/",views.subjects_view,name="subjects"),
    path("subjects/<int:subject_id>/",views.subject_detail_view,name="subject_detail"),
    path("upload/",views.upload_study_material_view,name="upload"),
    path("ask/",views.ask_question_view,name="ask_question"),
]
