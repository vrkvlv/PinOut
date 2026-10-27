from django.urls import path

from .views import ComponentProjectsAPIView, ProjectDetailAPIView, ProjectListAPIView

urlpatterns = [
    path("projects/", ProjectListAPIView.as_view()),
    path("projects/<int:pk>/", ProjectDetailAPIView.as_view()),
    path("components/<int:pk>/projects/", ComponentProjectsAPIView.as_view()),
]
