import pytest

from catalog.models import Component
from projects.models import Project, ProjectComponent

URL = "/api/components/"


def detail_url(pk):
    return f"/api/components/{pk}/"


# get


@pytest.mark.django_db
def test_anyone_can_get_list(api_client, component):
    response = api_client.get(URL)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["name"] == "Arduino Uno"


@pytest.mark.django_db
def test_anyone_can_get_one(api_client, component):
    response = api_client.get(detail_url(component.id))
    assert response.status_code == 200
    assert response.data["category"]["name"] == "Мікроконтролери"


@pytest.mark.django_db
def test_get_not_existing_returns_404(api_client):
    response = api_client.get(detail_url(999))
    assert response.status_code == 404


# post


@pytest.mark.django_db
def test_admin_can_create(admin_client, component_data):
    response = admin_client.post(URL, component_data, format="json")
    assert response.status_code == 201
    assert Component.objects.filter(name="Arduino Nano").exists()


@pytest.mark.django_db
def test_anonymous_cannot_create(api_client, component_data):
    response = api_client.post(URL, component_data, format="json")
    assert response.status_code == 401
    assert Component.objects.count() == 0


@pytest.mark.django_db
def test_regular_user_cannot_create(user_client, component_data):
    response = user_client.post(URL, component_data, format="json")
    assert response.status_code == 403
    assert Component.objects.count() == 0


@pytest.mark.django_db
def test_create_with_negative_price_returns_400(admin_client, component_data):
    component_data["price"] = "-5.00"
    response = admin_client.post(URL, component_data, format="json")
    assert response.status_code == 400
    assert "price" in response.data["errors"]


@pytest.mark.django_db
def test_create_without_name_returns_400(admin_client, component_data):
    del component_data["name"]
    response = admin_client.post(URL, component_data, format="json")
    assert response.status_code == 400
    assert "name" in response.data["errors"]


# patch


@pytest.mark.django_db
def test_admin_can_update_price(admin_client, component):
    response = admin_client.patch(
        detail_url(component.id), {"price": "399.99"}, format="json"
    )
    assert response.status_code == 200
    component.refresh_from_db()
    assert str(component.price) == "399.99"


@pytest.mark.django_db
def test_regular_user_cannot_update(user_client, component):
    response = user_client.patch(
        detail_url(component.id), {"price": "1.00"}, format="json"
    )
    assert response.status_code == 403


@pytest.mark.django_db
def test_update_not_existing_returns_404(admin_client):
    response = admin_client.patch(detail_url(999), {"price": "1.00"}, format="json")
    assert response.status_code == 404


# delete


@pytest.mark.django_db
def test_admin_can_delete(admin_client, component):
    response = admin_client.delete(detail_url(component.id))
    assert response.status_code == 204
    assert not Component.objects.filter(id=component.id).exists()


@pytest.mark.django_db
def test_anonymous_cannot_delete(api_client, component):
    response = api_client.delete(detail_url(component.id))
    assert response.status_code == 401
    assert Component.objects.filter(id=component.id).exists()


@pytest.mark.django_db
def test_delete_not_existing_returns_404(admin_client):
    response = admin_client.delete(detail_url(999))
    assert response.status_code == 404


@pytest.mark.django_db
def test_cannot_delete_component_used_in_project(admin_client, component):
    project = Project.objects.create(title="Світлофор", difficulty="easy")
    ProjectComponent.objects.create(project=project, component=component)

    response = admin_client.delete(detail_url(component.id))

    assert response.status_code == 409
    assert Component.objects.filter(id=component.id).exists()
