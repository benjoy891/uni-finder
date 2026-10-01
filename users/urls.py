from django.urls import path, include
from .views import StudentProgramDetailView, UserRegistrationView, UserLoginView, StudentUniversityListView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="user-registration"),
    path('login/', UserLoginView.as_view(), name="user-login"),
    path('universities/', StudentUniversityListView.as_view(), name="student-university-list"),
    path('university/<int:pk>/', StudentProgramDetailView.as_view(), name="student-program-detail"),
]