from django.urls import path

from .views import (
    CategoryDetailAPIView,
    CategoryListAPIView,
    ComponentDetailAPIView,
    ComponentListAPIView,
    ManufacturerDetailAPIView,
    ManufacturerListAPIView,
)

urlpatterns = [
    path("categories/", CategoryListAPIView.as_view()),
    path("categories/<int:pk>/", CategoryDetailAPIView.as_view()),
    path("manufacturers/", ManufacturerListAPIView.as_view()),
    path("manufacturers/<int:pk>/", ManufacturerDetailAPIView.as_view()),
    path("components/", ComponentListAPIView.as_view()),
    path("components/<int:pk>/", ComponentDetailAPIView.as_view()),
]
