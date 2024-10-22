from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CandidateApplication, CandidateStage, JobPosting
from django.core.mail import send_mail

@receiver(post_save, sender=JobPosting)
def check_vacancies_filled(sender, instance, **kwargs):
    # Check if vacancies equals filled
    if instance.filled >= instance.vacancies:
        instance.is_active = False
        instance.save()
    elif instance.is_active is False and instance.filled < instance.vacancies:
        instance.is_active = True
        instance.save()


@receiver(post_save, sender=JobPosting)
def reject_unmoved_candidates(sender, instance, **kwargs):
    if not instance.is_active:  # When the job posting is closed
        unmoved_candidates = CandidateApplication.objects.filter(
            job_posting=instance,
            stages__isnull=True,  # Candidates who have not been assigned to any stages
            status='Active'
        )
        unmoved_candidates.update(status='Rejected')


@receiver(post_save, sender=CandidateStage)
def update_candidate_status(sender, instance, **kwargs):
    if instance.result == 'Fail':
        instance.candidate_application.status = 'Rejected'
        instance.candidate_application.save()


@receiver(post_save, sender=CandidateStage)
def notify_employee_assignment(sender, instance, created, **kwargs):
    if instance.assigned_employee and created:
        # Send notification email
        send_mail(
            'New Stage Assigned',
            f'You have been assigned to the stage: {instance.stage.name} for candidate {instance.candidate_application.first_name} {instance.candidate_application.last_name}.',
            'noreply@yourcompany.com',
            [instance.assigned_employee.user.email],
            fail_silently=False,
        )