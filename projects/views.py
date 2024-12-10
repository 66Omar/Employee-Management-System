from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from projects.models import Project
from .serializers import *
from django.shortcuts import get_object_or_404
from employees.utils import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ProjectAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @staticmethod
    def get_queryset():
        return Project.objects.select_related("company", "department").prefetch_related(
            "assigned_employees"
        )

    def get(self, request, project_id=None):
        if project_id:
            return self.get_project_by_id(request, project_id)
        projects = self.get_queryset().all()
        serialized_projects = ProjectSerializer(projects, many=True).data
        return Response(serialized_projects, status=status.HTTP_200_OK)

    def get_project_by_id(self, request, project_id):
        project = get_object_or_404(self.get_queryset(), id=project_id)
        serialized_project = ProjectSerializer(project).data
        return Response(serialized_project, status=status.HTTP_200_OK)

    def post(self, request):
        if not IsAdminOrManager(request.user.id, request.data.get("company")):
            return Response(
                {"detail": "Unauthorized Employee"}, status=status.HTTP_401_UNAUTHORIZED
            )
        project_serializer = CreateProjectSerializer(data=request.data)
        if not project_serializer.is_valid():
            return Response(
                project_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        project_serializer.save()
        return Response(project_serializer.data, status=status.HTTP_201_CREATED)

    def patch(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if not IsAdminOrManager(request.user.id, project.company_id):
            return Response(
                {"detail": "Unauthorized Employee"}, status=status.HTTP_401_UNAUTHORIZED
            )

        project_serializer = UpdateProjectSerializer(
            project, data=request.data, partial=True
        )
        if not project_serializer.is_valid():
            return Response(
                project_serializer.errors, status=status.HTTP_400_BAD_REQUEST
            )
        project_serializer.save()
        return Response(project_serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, project_id):
        project = get_object_or_404(Project, id=project_id)
        if not IsAdmin(request.user.id, project.company_id):
            return Response(
                {"detail": "Unauthorized Employee"}, status=status.HTTP_401_UNAUTHORIZED
            )
        serialized_project = ProjectSerializer(project).data
        project.delete()
        return Response(serialized_project, status=status.HTTP_200_OK)
