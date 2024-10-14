from django.urls import path, include
from rest_framework.routers import DefaultRouter
from employees.views import EmployeeViewSet, EmployeeProfileView, SendInfoLinkView, ValidateTokenView, SubmitPersonalInfoView,EmployeeDocumentsView

router = DefaultRouter()
router.register(r'employees', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
    path('profile/', EmployeeProfileView.as_view(), name='employee-profile'),  # Profile URL under /employees/
    path('send-info-link/', SendInfoLinkView.as_view(), name='send-info-link'),
    path('validate-token/<uid>/<token>/', ValidateTokenView.as_view(), name='validate-token'),
    path('submit-info/<uid>/<token>/', SubmitPersonalInfoView.as_view(), name='submit-personal-info'),
    path('document-list/<int:employee_id>/documents/', EmployeeDocumentsView.as_view(), name='employee-documents'),
]
