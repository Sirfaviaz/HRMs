from django.urls import path
from .views import AttendanceRecordListView, AttendanceStatusView, ClockInView, ClockOutView

urlpatterns = [
    path('clock-in/', ClockInView.as_view(), name='clock-in'),
    path('clock-out/', ClockOutView.as_view(), name='clock-out'),
    path('records/', AttendanceRecordListView.as_view(), name='attendance-records'),
     path('status/', AttendanceStatusView.as_view(), name='attendance-status')
]