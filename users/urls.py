from django.urls import path, include
from .views import StudentUniversityDetailView, UserRegistrationView, UserLoginView, StudentUniversityListView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name="user-registration"),
    path('login/', UserLoginView.as_view(), name="user-login"),
    path('universities/', StudentUniversityListView.as_view(), name="universities-list"),
    path('university/<int:pk>/', StudentUniversityDetailView.as_view(), name="university-detail"),
]