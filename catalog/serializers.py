from rest_framework import serializers

from .models import Category, Component, Manufacturer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description"]


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ["id", "name", "country", "description"]


class ComponentSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # читання
    manufacturer = ManufacturerSerializer(read_only=True)

    category_id = serializers.PrimaryKeyRelatedField(  # створіння редагування
        queryset=Category.objects.all(), source="category", write_only=True
    )
    manufacturer_id = serializers.PrimaryKeyRelatedField(
        queryset=Manufacturer.objects.all(), source="manufacturer", write_only=True
    )

    class Meta:
        model = Component
        fields = [
            "id",
            "name",
            "description",
            "application",
            "specs",
            "price",
            "image",
            "datasheet_url",
            "category",
            "manufacturer",
            "category_id",
            "manufacturer_id",
        ]
