from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from django.utils import timezone
from employees.models import Employee
from attendance.models import AttendanceRecord
from attendance.serializers import AttendanceRecordSerializer

class ClockInView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print("request:",request.user.id)
        emp = request.user.id
        employee = Employee.objects.get(id=emp)

        today = timezone.now().date()
        attendance, created = AttendanceRecord.objects.get_or_create(employee=employee, date=today)
        if attendance.clock_in_time:
            return Response({"detail": "Already clocked in."}, status=status.HTTP_400_BAD_REQUEST)
        attendance.clock_in_time = timezone.now()
        attendance.save()
        return Response({"detail": "Clock-in successful."}, status=status.HTTP_200_OK)
    


class ClockOutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        id = request.user.id
        employee = Employee.objects.get(id = id)
        today = timezone.now().date()
        try:
            attendance = AttendanceRecord.objects.get(employee=employee, date=today)
            if attendance.clock_out_time:
                return Response({"detail": "Already clocked out."}, status=status.HTTP_400_BAD_REQUEST)
            attendance.clock_out_time = timezone.now()
            attendance.save()
            return Response({"detail": "Clock-out successful."}, status=status.HTTP_200_OK)
        except AttendanceRecord.DoesNotExist:
            return Response({"detail": "Clock-in first."}, status=status.HTTP_400_BAD_REQUEST)



class AttendanceRecordListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        employee = request.user.employee
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        records = AttendanceRecord.objects.filter(
            employee=employee,
            date__range=[start_date, end_date]
        )
        serializer = AttendanceRecordSerializer(records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AttendanceStatusView(APIView):
    """
    View to get the clock-in status for the current day.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        print("1abc",request.user.id)
        id = request.user.id
        # Get the current employee based on the authenticated user
        employee = Employee.objects.get(id = id)
        print("abc",employee.id)
        today = timezone.now().date()

        try:
            # Check today's attendance record
            # print("true")
            attendance = AttendanceRecord.objects.get(employee=employee, date=today)
            print("attendance",attendance, attendance.clock_out_time)
            if attendance.clock_in_time and not attendance.clock_out_time:
                print("True")
                return Response({"is_clocked_in": True}, status=status.HTTP_200_OK)
            else:
                return Response({"is_clocked_in": False}, status=status.HTTP_200_OK)
        except AttendanceRecord.DoesNotExist:
            return Response({"is_clocked_in": False}, status=status.HTTP_200_OK)