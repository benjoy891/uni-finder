from django.urls import path, include
from .views import UniversityView, ProgramView


urlpatterns = [
    path('', UniversityView.as_view(), name="university-list"),
    path('<int:pk>/', UniversityView.as_view(), name="university-modify"),
    path('<int:pk>/programs/', ProgramView.as_view(), name="program-list"),
    path('programs/<int:pk>/', ProgramView.as_view(), name="program-modify"),

]