# jobs/models.py


from django.db import models
from departments.models import Department, Position
from employees.models import Employee  # Import Employee model

class JobPosting(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)  # Nullable Position
    location = models.CharField(max_length=255)
    employment_type = models.CharField(max_length=50, choices=[
        ('Full-Time', 'Full-Time'),
        ('Part-Time', 'Part-Time'),
        ('Contract', 'Contract'),
        ('Internship', 'Internship'),
    ])
    posted_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    incharge_employee = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True)  # Nullable employee

    def __str__(self):
        return self.title




class CandidateApplication(models.Model):
    job_posting = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(null=True, blank=True)
    application_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Applied', 'Applied'),
        ('Reviewed', 'Reviewed'),
        ('Interview Scheduled', 'Interview Scheduled'),
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected'),
    ], default='Applied')

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.job_posting.title}"
