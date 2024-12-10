from django.urls import path
from . import views

urlpatterns = [
    path("", views.EmployeeAPIView.as_view()),
    path("<int:employee_id>", views.EmployeeAPIView.as_view()),
    path("<int:employee_id>/status", views.EmployeeStatusTransitionView.as_view())
]
