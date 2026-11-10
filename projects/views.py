from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.models import Component

from .models import Project
from .serializers import ProjectSerializer


# GET (список) і POST (створення)
class ProjectListAPIView(APIView):
    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Невалідні дані", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


# GET (один), PATCH (редагування) і DELETE
class ProjectDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            return None

    def get(self, request, pk):
        project = self.get_object(pk)
        if not project:
            return Response(
                {"detail": "Проєкт не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProjectSerializer(project)
        return Response(serializer.data)

    def patch(self, request, pk):
        project = self.get_object(pk)
        if not project:
            return Response(
                {"detail": "Проєкт не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProjectSerializer(project, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {"detail": "Невалідні дані", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        project = self.get_object(pk)
        if not project:
            return Response(
                {"detail": "Проєкт не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# GET проєкти, де використовується компонент
class ComponentProjectsAPIView(APIView):
    def get(self, request, pk):
        if not Component.objects.filter(pk=pk).exists():
            return Response(
                {"detail": "Компонент не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        projects = Project.objects.filter(project_components__component_id=pk)
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)
