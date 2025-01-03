from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Create your tests here.
from materials.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):
    """Тестируем CRUD для курсов"""

    def setUp(self):
        """Setup"""
        self.user = User.objects.create(email="test_admin@gmail.com")
        self.user.set_password("Nike130296")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title="test_course", description="test_description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="test_lesson",
            description="test_description_lesson",
            owner=self.user,
            course=self.course,
        )

    def test_course_retrieve(self):
        """Проверка возврата конкретного курса"""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.get(url)
        print(response.status_code)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Expected 200, got {response.status_code} instead.",
        )

        self.assertEqual(
            data.get("title"),
            self.course.title,
        )

    def test_course_create(self):
        """Тест создания курса."""
        url = reverse("materials:course-list")
        data = {
            "title": "test_course_create_2",
            "description": "test_description_create_2",
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"Expected 201, got {response.status_code} instead.",
        )

        self.assertEqual(
            data.get("title"),
            "test_course_create_2",
        )

    def test_course_update(self):
        """Тест обновления курса."""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        data = {"title": "test_course_updated"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Expected 200, got {response.status_code} instead.",
        )
        self.assertEqual(
            data.get("title"),
            "test_course_updated",
        )

    def test_course_delete(self):
        """Тест на удаление курса."""
        url = reverse("materials:course-detail", args=(self.course.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            f"Expected 204, got {response.status_code} instead.",
        )

        self.assertEqual(
            Course.objects.filter(pk=self.course.pk).exists(),
            False,
        )

    def test_course_list(self):
        """Тест списка курсов."""
        url = reverse("materials:course-list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "title": self.course.title,
                    "description": self.course.description,
                    "preview": None,
                    "count_lessons": 1,
                    "lessons": [
                        {
                            "id": self.lesson.pk,
                            "title": self.lesson.title,
                            "description": self.lesson.description,
                            "preview": None,
                            "video_link": None,
                            "course": self.course.pk,
                            "owner": self.user.pk,
                        }
                    ],
                    "owner": self.user.pk,
                    "subscription": None,
                }
            ],
        }

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Expected 200, got {response.status_code} instead.",
        )
        self.assertEqual(
            data,
            result,
        )


class LessonTestCase(APITestCase):
    """Тестируем CRUD для курсов"""

    def setUp(self):
        """Setup"""
        self.user = User.objects.create(email="test_admin@gmail.com")
        self.user.set_password("Nike130296")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(
            title="test_course", description="test_description", owner=self.user
        )
        self.lesson = Lesson.objects.create(
            title="test_lesson",
            description="test_description_lesson",
            owner=self.user,
            course=self.course,
        )

    def test_lesson_retrieve(self):
        """Проверка возврата конкретного курса"""
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        print(response.status_code)
        data = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Expected 200, got {response.status_code} instead.",
        )

        self.assertEqual(
            data.get("title"),
            self.lesson.title,
        )

    def test_lesson_create(self):
        """Тест создания курса."""
        url = reverse("materials:lesson_create")
        data = {
            "title": "test_lesson_create",
            "description": "test_description_create_lesson",
            "owner": self.user.pk,
        }
        response = self.client.post(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
            f"Expected 201, got {response.status_code} instead.",
        )

        self.assertEqual(
            data.get("title"),
            "test_lesson_create",
        )

    def test_lesson_update(self):
        """Тест обновления курса."""
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {"title": "test_lesson_updated"}
        response = self.client.patch(url, data)
        data = response.json()
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Expected 200, got {response.status_code} instead.",
        )
        self.assertEqual(
            data.get("title"),
            "test_lesson_updated",
        )

    def test_lesson_delete(self):
        """Тест на удаление курса."""
        url = reverse("materials:lesson_destroy", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
            f"Expected 204, got {response.status_code} instead.",
        )

        self.assertEqual(
            Lesson.objects.filter(pk=self.course.pk).exists(),
            False,
        )

    def test_lesson_list(self):
        """Тест списка курсов."""
        url = reverse("materials:lessons_list")
        response = self.client.get(url)
        data = response.json()
        result = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.lesson.pk,
                    "title": self.lesson.title,
                    "description": self.lesson.description,
                    "preview": None,
                    "video_link": None,
                    "course": self.course.pk,
                    "owner": self.user.pk,
                }
            ],
        }

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
            f"Expected 200, got {response.status_code} instead.",
        )
        self.assertEqual(
            data,
            result,
        )
