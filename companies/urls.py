from django.urls import path
from . import views

urlpatterns = [
    path("", views.CompanyAPIView.as_view()),
    path("<int:company_id>", views.CompanyAPIView.as_view()),
    path("<int:company_id>/departments", views.get_company_departments),
    path("<int:company_id>/employees", views.get_company_employees),
]
