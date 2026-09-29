from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import timedelta

from django.utils import timezone
from universities.models import AdmissionRequirement, University, Program
from django.contrib.auth import get_user_model

User = get_user_model()


class UniversityListAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="teststudent",
            password="testpassword"
        )
        self.url = reverse("student-university-list")
        today = timezone.localdate()

        self.trier = University.objects.create(
            name="Trier University",
            country="Germany",
            city="Trier",
            address="Trier, Germany",
            website="https://example.com"
        )
        self.trier_program = Program.objects.create(
            university=self.trier,
            name="MSc Natural Language Processing",
            degree="MASTER",
            teaching_language="ENGLISH",
            semester="WINTER",
            application_start=today - timedelta(days=10),
            application_end=today + timedelta(days=30),
            application_platform="UNI_ASSIST",
            nc_status="NC_FREE",
            vpd_required=False,
        )
        AdmissionRequirement.objects.create(
            program=self.trier_program,
            required_german_gpa=2.5,
            gre=False,
            gmat=False,
            aps_required=True,
        )

        self.passau = University.objects.create(
            name="University of Passau",
            country="Germany",
            city="Passau",
            address="Passau, Germany",
            website="https://example.com"
        )
        self.passau_program = Program.objects.create(
            university=self.passau,
            name="MSc Computer Science",
            degree="MASTER",
            teaching_language="GERMAN",
            semester="SUMMER",
            application_start=today - timedelta(days=10),
            application_end=today + timedelta(days=30),
            application_platform="DIRECT",
            nc_status="NC",
            vpd_required=True,
        )
        AdmissionRequirement.objects.create(
            program=self.passau_program,
            required_german_gpa=1.8,
            gre=True,
            gmat=True,
            aps_required=False,
        )

    def test_list_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_list_universities(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["result"])

    def test_filter_by_city(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"city": "Trier"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 1)
        self.assertEqual(universities[0]["city"], "Trier")

    def test_search_university(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"search": "Trier"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 1)
        self.assertIn("Trier", universities[0]["name"])

    def test_filter_by_degree(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"degree": "MASTER"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 2)

    def test_filter_by_teaching_language(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"teaching_language": "ENGLISH"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 1)
        self.assertEqual(universities[0]["name"], "Trier University")

    def test_filter_by_semester(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"semester": "WINTER"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 1)
        self.assertEqual(universities[0]["name"], "Trier University")

    def test_filter_by_gre_required(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"gre_required": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 1)
        self.assertEqual(universities[0]["name"], "University of Passau")

    def test_filter_by_required_gpa(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"required_gpa": "2.0"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 1)
        self.assertEqual(universities[0]["name"], "Trier University")

    def test_filter_by_nc_status(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"nc_status": "NC_FREE"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 1)
        self.assertEqual(universities[0]["name"], "Trier University")

    def test_filter_by_vpd_required(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"vpd_required": "true"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 1)
        self.assertEqual(universities[0]["name"], "University of Passau")

    def test_filter_status_open(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"status": "OPEN"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 2)

    def test_filter_status_closed_returns_nothing(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"status": "CLOSED"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 0)

    def test_combined_filters(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {
            "degree": "MASTER",
            "teaching_language": "ENGLISH",
            "semester": "WINTER",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 1)
        self.assertEqual(universities[0]["name"], "Trier University")

    def test_combined_filters_return_no_results(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {
            "teaching_language": "ENGLISH",
            "semester": "SUMMER",
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 0)

    def test_ordering_by_name_descending(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"ordering": "-name"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        names = [u["name"] for u in universities]
        self.assertEqual(names, ["University of Passau", "Trier University"])

    def test_university_with_multiple_programs_appears_once_per_program(self):
        Program.objects.create(
            university=self.trier,
            name="MSc Data Science",
            degree="MASTER",
            teaching_language="ENGLISH",
            semester="WINTER",
            application_platform="DIRECT",
            nc_status="NC_FREE",
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"degree": "MASTER"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        universities = response.data["data"]
        self.assertEqual(len(universities), 3)
        trier_programs = [u["program_name"] for u in universities if u["name"] == "Trier University"]
        self.assertCountEqual(trier_programs, ["MSc Natural Language Processing", "MSc Data Science"])


    def test_filters_must_match_same_program(self):
        uni = University.objects.create(
            name="Test Uni", country="Germany", city="Bonn",
            address="Bonn", website="https://example.com",
        )
        Program.objects.create(
            university=uni, name="BSc A", degree="BACHELOR", teaching_language="ENGLISH",
            semester="WINTER", application_platform="DIRECT", nc_status="NC_FREE",
        )
        Program.objects.create(
            university=uni, name="MSc B", degree="MASTER", teaching_language="ENGLISH",
            semester="SUMMER", application_platform="DIRECT", nc_status="NC_FREE",
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url, {"city": "Bonn", "degree": "MASTER", "semester": "WINTER"})
        self.assertEqual(len(response.data["data"]), 0)