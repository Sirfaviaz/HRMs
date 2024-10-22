from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, viewsets, generics
from django.utils import timezone
from accounts.permissions import IsHRUser
from employees.models import Employee
from attendance.models import AttendanceRecord, LeaveRequest
from attendance.serializers import AttendanceRecordSerializer, LeaveRequestSerializer
from rest_framework.decorators import action


class ClockInView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        print("request:",request.user.id)
        emp = request.user.id
        employee = Employee.objects.get(user=emp)

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
        employee = Employee.objects.get(user = id)
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
        user_id = request.user
        employee = Employee.objects.get(user=user_id)
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
        


class LeaveRequestViewSet(viewsets.ModelViewSet):
    queryset = LeaveRequest.objects.all()
    serializer_class = LeaveRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # For employees, return only their leave requests
        if self.request.user.is_hr:
            return LeaveRequest.objects.all()  # HR can view all leave requests
        else:
            return LeaveRequest.objects.filter(employee__user=self.request.user)  # Employees can view only their own leave requests

    def perform_create(self, serializer):
    # Ensure the user has an associated employee
        if not hasattr(self.request.user, 'employee'):
            return Response({"employee": ["User is not linked to an employee."]}, status=status.HTTP_400_BAD_REQUEST)

        # Automatically assign the employee field based on the current user
        serializer.save(employee=self.request.user.employee)

    # Custom action for HR to approve/reject leave requests
    @action(detail=True, methods=['patch'], permission_classes=[permissions.IsAuthenticated, IsHRUser])
    def update_status(self, request, pk=None):
        leave_request = self.get_object()
        status = request.data.get('status')

        if status not in ['Approved', 'Rejected']:
            return Response({'detail': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        leave_request.status = status
        leave_request.save()
        return Response({'status': leave_request.status})
    

from django.utils import timezone
from rest_framework import permissions, generics
from django.shortcuts import get_object_or_404

class EmployeeAttendanceRecordsView(generics.ListAPIView):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        selected_employee_id = self.request.query_params.get('employee_id', None)
        date = self.request.query_params.get('date', None)

        # Check if the user is an HR/Admin and is selecting a specific employee
        if selected_employee_id and (user.is_hr or user.is_admin):
            # Get the selected employee by ID
            selected_employee = get_object_or_404(Employee, id=selected_employee_id)
        else:
            # Default to the logged-in employee
            selected_employee = Employee.objects.get(user=user)

        # Filter by date if provided
        if date:
            return AttendanceRecord.objects.filter(employee=selected_employee, date=date)
        else:
            # Default to the current month if no date is specified
            now = timezone.now()
            start_date = timezone.datetime(now.year, now.month, 1).date()
            end_date = timezone.datetime(now.year, now.month, now.day).date()
            return AttendanceRecord.objects.filter(employee=selected_employee, date__range=[start_date, end_date])
