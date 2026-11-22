import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from catalog.models import Category, Component, Manufacturer


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username="admin", password="AdminPass123!", is_staff=True
    )


@pytest.fixture
def regular_user():
    return User.objects.create_user(username="user", password="UserPass123!")


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.force_authenticate(user=admin_user)
    return client


@pytest.fixture
def user_client(regular_user):
    client = APIClient()
    client.force_authenticate(user=regular_user)
    return client


@pytest.fixture
def category():
    return Category.objects.create(name="Мікроконтролери")


@pytest.fixture
def manufacturer():
    return Manufacturer.objects.create(name="Arduino", country="Italy")


@pytest.fixture
def component(category, manufacturer):
    return Component.objects.create(
        name="Arduino Uno",
        price="450.00",
        category=category,
        manufacturer=manufacturer,
    )


@pytest.fixture
def component_data(category, manufacturer):
    return {
        "name": "Arduino Nano",
        "price": "300.00",
        "category_id": category.id,
        "manufacturer_id": manufacturer.id,
    }
