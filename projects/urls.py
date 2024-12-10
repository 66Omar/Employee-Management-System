from django.urls import path
from projects import views

urlpatterns = [
    path("", views.ProjectAPIView.as_view()),
    path("<int:project_id>", views.ProjectAPIView.as_view()),
]
