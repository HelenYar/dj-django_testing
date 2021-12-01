import pytest
from django.urls import reverse
from students.models import Course
from students.serializers import CourseSerializer
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT
from model_bakery import baker

def test_example():
    assert True, "Just test example"


@pytest.mark.django_db
def test_first_courses(client, course_factory):
    url = reverse("courses-list")
    course = course_factory(name="Экономика")
    resp = client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json[0]["name"] == course.name


@pytest.mark.django_db
def test_courses_list(client, course_factory):
    url = reverse("courses-list")
    courses = course_factory(_quantity=3)
    resp = client.get(url)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert len(resp_json) == 3

@pytest.mark.django_db
def test_filter_id(client, course_factory):
    url = reverse("courses-list")
    course = course_factory(_quantity=5)
    resp = client.get(url, {"id": course[4].id})
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json[0]["id"] == course[4].id

@pytest.mark.django_db
def test_filter_name(client, course_factory):
    url = reverse("courses-list")
    course = course_factory(_quantity=5)
    resp = client.get(url, {"name": course[4].name})
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert resp_json[0]["name"] == course[4].name


@pytest.mark.django_db
def test_create(client):
    url = reverse("courses-list")
    course_name = "Информатика"
    data = {"name": course_name}
    resp = client.post(url, data)
    assert resp.status_code == HTTP_201_CREATED
    resp_json = resp.json()
    assert course_name == resp_json["name"]


@pytest.mark.django_db
def test_update(client, course_factory):
    course = course_factory(name="Социолгия")
    url = reverse("courses-detail", args=(course.id, ))
    update_name = "Политология"
    data = {"name": update_name}
    resp = client.patch(url, data)
    assert resp.status_code == HTTP_200_OK
    resp_json = resp.json()
    assert update_name == resp_json["name"]


@pytest.mark.django_db
def test_delete(client, course_factory):
    course = course_factory(name="Физика")
    url = reverse("courses-detail", args=(course.id, ))
    resp = client.delete(url)
    assert resp.status_code == HTTP_204_NO_CONTENT
    assert len(Course.objects.filter(name="Физика")) == 0