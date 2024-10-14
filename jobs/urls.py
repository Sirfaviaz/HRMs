# jobs/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import JobPostingViewSet, CandidateApplicationViewSet

router = DefaultRouter()
router.register(r'job-postings', JobPostingViewSet, basename='jobposting')
router.register(r'applications', CandidateApplicationViewSet, basename='candidateapplication')


urlpatterns = [
    path('', include(router.urls)),
]
