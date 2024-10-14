from django.shortcuts import render

# admin_app/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from employees.models import Employee
from jobs.models import CandidateApplication, JobPosting

class AdminStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total_employees = Employee.objects.count()
        active_job_postings = JobPosting.objects.filter(is_active=True).count()
        pending_onboarding = CandidateApplication.objects.filter(status='Offered').count()
        return Response({
            'totalEmployees': total_employees,
            'activeJobPostings': active_job_postings,
            'pendingOnboarding': pending_onboarding,
        })

