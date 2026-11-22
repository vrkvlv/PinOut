import logging

from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.permissions import IsAdminOrReadOnly

from .models import Category, Component, Manufacturer
from .serializers import (
    CategorySerializer,
    ComponentSerializer,
    ManufacturerSerializer,
)

logger = logging.getLogger(__name__)

COMPONENT_EXAMPLE = OpenApiExample(
    "Arduino Uno",
    value={
        "name": "Arduino Uno R3",
        "description": "Плата на ATmega328P",
        "application": "Навчальні проєкти",
        "specs": "14 цифрових пінів, 6 аналогових",
        "price": "450.00",
        "image": "",
        "datasheet_url": "",
        "category_id": 1,
        "manufacturer_id": 1,
    },
    request_only=True,
)

# тут категорії


class CategoryListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer

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
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = CategorySerializer

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


# отут виробрники


class ManufacturerListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ManufacturerSerializer

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
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ManufacturerSerializer

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


# отут компоненти


@extend_schema(tags=["Components"])
class ComponentListAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ComponentSerializer

    @extend_schema(
        summary="Список компонентів",
        responses={200: ComponentSerializer(many=True)},
    )
    def get(self, request):
        logger.debug("Запит списку компонентів")
        components = Component.objects.all()
        serializer = ComponentSerializer(components, many=True)
        return Response(serializer.data)

    @extend_schema(
        summary="Створити компонент (тільки admin)",
        description="Потрібен JWT-токен користувача з is_staff=True.",
        request=ComponentSerializer,
        examples=[COMPONENT_EXAMPLE],
        responses={
            201: ComponentSerializer,
            400: OpenApiResponse(description="Невалідні дані"),
            401: OpenApiResponse(description="Не передано токен"),
            403: OpenApiResponse(description="Користувач не admin"),
        },
    )
    def post(self, request):
        serializer = ComponentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(
                "Компонент id=%s створено користувачем %s",
                serializer.data["id"],
                request.user.username,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.warning("Невалідні дані компонента: %s", serializer.errors)
        return Response(
            {"detail": "Невалідні дані", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


@extend_schema(tags=["Components"])
class ComponentDetailAPIView(APIView):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = ComponentSerializer

    def get_object(self, pk):
        try:
            return Component.objects.get(pk=pk)
        except Component.DoesNotExist:
            logger.warning("Компонент id=%s не знайдено", pk)
            return None

    @extend_schema(
        summary="Один компонент",
        responses={
            200: ComponentSerializer,
            404: OpenApiResponse(description="Компонент не знайдено"),
        },
    )
    def get(self, request, pk):
        component = self.get_object(pk)
        if not component:
            return Response(
                {"detail": "Компонент не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ComponentSerializer(component)
        return Response(serializer.data)

    @extend_schema(
        summary="Змінити компонент (тільки admin)",
        request=ComponentSerializer,
        examples=[
            OpenApiExample("Нова ціна", value={"price": "399.99"}, request_only=True)
        ],
        responses={
            200: ComponentSerializer,
            400: OpenApiResponse(description="Невалідні дані"),
            401: OpenApiResponse(description="Не передано токен"),
            403: OpenApiResponse(description="Користувач не admin"),
            404: OpenApiResponse(description="Компонент не знайдено"),
        },
    )
    def patch(self, request, pk):
        component = self.get_object(pk)
        if not component:
            return Response(
                {"detail": "Компонент не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ComponentSerializer(component, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            logger.info(
                "Компонент id=%s змінено користувачем %s", pk, request.user.username
            )
            return Response(serializer.data)
        logger.warning("Невалідні дані компонента id=%s: %s", pk, serializer.errors)
        return Response(
            {"detail": "Невалідні дані", "errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @extend_schema(
        summary="Видалити компонент (тільки admin)",
        responses={
            204: OpenApiResponse(description="Видалено"),
            401: OpenApiResponse(description="Не передано токен"),
            403: OpenApiResponse(description="Користувач не admin"),
            404: OpenApiResponse(description="Компонент не знайдено"),
            409: OpenApiResponse(description="Компонент використовується в проєктах"),
        },
    )
    def delete(self, request, pk):
        component = self.get_object(pk)
        if not component:
            return Response(
                {"detail": "Компонент не знайдено"}, status=status.HTTP_404_NOT_FOUND
            )
        if component.project_components.exists():
            logger.warning("Спроба видалити компонент id=%s, який є в проєктах", pk)
            return Response(
                {"detail": "Неможливо видалити компонент, бо він є в проєктах"},
                status=status.HTTP_409_CONFLICT,
            )
        component.delete()
        logger.info(
            "Компонент id=%s видалено користувачем %s", pk, request.user.username
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
