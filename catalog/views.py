from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Category, Component, Manufacturer
from .serializers import (
    CategorySerializer,
    ComponentSerializer,
    ManufacturerSerializer,
)

# ---------- Категорії ----------


class CategoryListAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Невалідні дані", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CategoryDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return None

    def get(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response(
                {"detail": "Категорію не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def patch(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response(
                {"detail": "Категорію не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {"detail": "Невалідні дані", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        category = self.get_object(pk)
        if not category:
            return Response(
                {"detail": "Категорію не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        if Component.objects.filter(category=category).exists():
            return Response(
                {"detail": "Неможливо видалити категорію, бо в ній є компоненти"},
                status=status.HTTP_409_CONFLICT,
            )
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- Виробники ----------


class ManufacturerListAPIView(APIView):
    def get(self, request):
        manufacturers = Manufacturer.objects.all()
        serializer = ManufacturerSerializer(manufacturers, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ManufacturerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Невалідні дані", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ManufacturerDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Manufacturer.objects.get(pk=pk)
        except Manufacturer.DoesNotExist:
            return None

    def get(self, request, pk):
        manufacturer = self.get_object(pk)
        if not manufacturer:
            return Response(
                {"detail": "Виробника не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ManufacturerSerializer(manufacturer)
        return Response(serializer.data)

    def patch(self, request, pk):
        manufacturer = self.get_object(pk)
        if not manufacturer:
            return Response(
                {"detail": "Виробника не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ManufacturerSerializer(
            manufacturer, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {"detail": "Невалідні дані", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        manufacturer = self.get_object(pk)
        if not manufacturer:
            return Response(
                {"detail": "Виробника не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        if Component.objects.filter(manufacturer=manufacturer).exists():
            return Response(
                {"detail": "Неможливо видалити виробника, бо в нього є компоненти"},
                status=status.HTTP_409_CONFLICT,
            )
        manufacturer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ---------- Компоненти ----------


class ComponentListAPIView(APIView):
    def get(self, request):
        components = Component.objects.all()
        serializer = ComponentSerializer(components, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ComponentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"detail": "Невалідні дані", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ComponentDetailAPIView(APIView):
    def get_object(self, pk):
        try:
            return Component.objects.get(pk=pk)
        except Component.DoesNotExist:
            return None

    def get(self, request, pk):
        component = self.get_object(pk)
        if not component:
            return Response(
                {"detail": "Компонент не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ComponentSerializer(component)
        return Response(serializer.data)

    def patch(self, request, pk):
        component = self.get_object(pk)
        if not component:
            return Response(
                {"detail": "Компонент не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ComponentSerializer(component, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(
            {"detail": "Невалідні дані", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        component = self.get_object(pk)
        if not component:
            return Response(
                {"detail": "Компонент не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        if component.project_components.exists():
            return Response(
                {"detail": "Неможливо видалити компонент, бо він є в проєктах"},
                status=status.HTTP_409_CONFLICT,
            )
        component.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
