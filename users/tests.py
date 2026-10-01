from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from datetime import timedelta

from django.utils import timezone
from universities.models import AdmissionRequirement, LanguageRequirement, University, Program
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


class ProgramDetailAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="teststudent",
            password="testpassword"
        )
        today = timezone.localdate()

        self.trier = University.objects.create(
            name="Trier University",
            country="Germany",
            city="Trier",
            address="Trier, Germany",
            website="https://example.com"
        )
        self.nlp_program = Program.objects.create(
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
        self.ds_program = Program.objects.create(
            university=self.trier,
            name="MSc Data Science",
            degree="MASTER",
            teaching_language="ENGLISH",
            semester="WINTER",
            application_platform="DIRECT",
            nc_status="NC_FREE",
        )
        AdmissionRequirement.objects.create(
            program=self.nlp_program,
            required_german_gpa=2.5,
            gre=False,
            gmat=False,
            aps_required=True,
        )

        LanguageRequirement.objects.create(
            program=self.nlp_program,
            language="ENGLISH",
            exam="IELTS",
            minimum_score_numeric=6.5,
        )
        LanguageRequirement.objects.create(
            program=self.nlp_program,
            language="GERMAN",
            exam="GOETHE",
            minimum_level="B2",
        )
        LanguageRequirement.objects.create(
            program=self.nlp_program,
            language="ENGLISH",
            exam="TOEFL",
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
            application_platform="DIRECT",
            nc_status="NC",
            vpd_required=True,
        )

        self.url = reverse("student-program-detail", kwargs={"pk": self.nlp_program.pk})

    def get_program_data(self, program):
        self.client.force_authenticate(user=self.user)
        url = reverse("student-program-detail", kwargs={"pk": program.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        return response.data["data"]

    def test_detail_requires_authentication(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_user_can_get_program(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["result"])
        self.assertEqual(response.data["message"], "Program retrieved successfully.")

    def test_detail_returns_correct_program_fields(self):
        data = self.get_program_data(self.nlp_program)
        self.assertEqual(data["id"], self.nlp_program.id)
        self.assertEqual(data["name"], "MSc Natural Language Processing")
        self.assertEqual(data["degree"], "MASTER")
        self.assertEqual(data["teaching_language"], "ENGLISH")
        self.assertEqual(data["semester"], "WINTER")
        self.assertEqual(data["application_platform"], "UNI_ASSIST")
        self.assertEqual(data["nc_status"], "NC_FREE")
        self.assertFalse(data["vpd_required"])

    def test_detail_returns_nested_university(self):
        data = self.get_program_data(self.nlp_program)
        university = data["university"]
        self.assertEqual(university["id"], self.trier.id)
        self.assertEqual(university["name"], "Trier University")
        self.assertEqual(university["country"], "Germany")
        self.assertEqual(university["city"], "Trier")
        self.assertEqual(university["address"], "Trier, Germany")
        self.assertEqual(university["website"], "https://example.com")

    def test_detail_university_does_not_include_programs(self):
        data = self.get_program_data(self.nlp_program)
        self.assertNotIn("programs", data["university"])

    def test_detail_returns_only_requested_program(self):
        data = self.get_program_data(self.ds_program)
        self.assertEqual(data["id"], self.ds_program.id)
        self.assertEqual(data["name"], "MSc Data Science")

    def test_detail_returns_program_of_other_university(self):
        data = self.get_program_data(self.passau_program)
        self.assertEqual(data["name"], "MSc Computer Science")
        self.assertEqual(data["university"]["id"], self.passau.id)
        self.assertEqual(data["university"]["name"], "University of Passau")
        self.assertTrue(data["vpd_required"])

    def test_detail_not_found(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("student-program-detail", kwargs={"pk": 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(response.data["result"])
        self.assertEqual(response.data["error"]["type"], "Not Found")
        self.assertEqual(response.data["message"], "Program Not Found.")

    def test_detail_program_includes_admission_requirement(self):
        data = self.get_program_data(self.nlp_program)
        requirement = data["admission_requirement"]
        self.assertEqual(requirement["required_german_gpa"], "2.50")
        self.assertFalse(requirement["gre"])
        self.assertFalse(requirement["gmat"])
        self.assertTrue(requirement["aps_required"])

    def test_detail_program_without_admission_requirement(self):
        data = self.get_program_data(self.ds_program)
        self.assertIsNone(data["admission_requirement"])

    def test_detail_program_includes_language_requirements(self):
        data = self.get_program_data(self.nlp_program)
        self.assertEqual(len(data["language_requirements"]), 3)

    def test_detail_language_requirement_required_score(self):
        data = self.get_program_data(self.nlp_program)
        scores = {r["exam"]: r["required_score"] for r in data["language_requirements"]}
        self.assertEqual(scores["IELTS"], "6.50")
        self.assertEqual(scores["GOETHE"], "B2")
        self.assertIsNone(scores["TOEFL"])

    def test_detail_program_without_language_requirements(self):
        data = self.get_program_data(self.ds_program)
        self.assertEqual(data["language_requirements"], [])