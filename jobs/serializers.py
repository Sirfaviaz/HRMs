from rest_framework import serializers
from .models import JobPosting, CandidateApplication

class JobPostingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPosting
        fields = '__all__'


class CandidateApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CandidateApplication
        fields = '__all__'
        read_only_fields = ['application_date', 'status']