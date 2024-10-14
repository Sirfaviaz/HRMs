from rest_framework import viewsets, permissions
from .models import JobPosting
from .serializers import JobPostingSerializer, CandidateApplication,CandidateApplicationSerializer

class JobPostingViewSet(viewsets.ModelViewSet):
    queryset = JobPosting.objects.all()
    serializer_class = JobPostingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]  # Only admins can modify
        else:
            permission_classes = [permissions.AllowAny]  # Anyone can view
        return [permission() for permission in permission_classes]


class CandidateApplicationViewSet(viewsets.ModelViewSet):
    queryset = CandidateApplication.objects.all()
    serializer_class = CandidateApplicationSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    def get_permissions(self):
        if self.action in ['create']:
            permission_classes = [permissions.AllowAny]  # Anyone can apply
        else:
            permission_classes = [permissions.IsAdminUser]  # Only admins can view/update applications
        return [permission() for permission in permission_classes]