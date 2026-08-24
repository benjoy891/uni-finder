from django.urls import path, include
from .views import UniversityListView, UniversityDetailView, ProgramListView


urlpatterns = [
    path('', UniversityListView.as_view(), name="university-list"),
    path('<int:pk>/', UniversityDetailView.as_view(), name="university-detail"),
    path('<int:pk>/programs/', ProgramListView.as_view(), name="program-list"),

]