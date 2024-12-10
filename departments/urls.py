from django.urls import path
from departments import views

urlpatterns = [
    path("", views.DepartmentAPIView.as_view()),
    path("<int:department_id>", views.DepartmentAPIView.as_view()),
    path("<int:department_id>/employees", views.get_department_employees),
]
