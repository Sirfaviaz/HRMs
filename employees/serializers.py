from rest_framework import serializers
from employees.models import Employee, EmployeePersonalDetails, EmployeeJobDetails, Document
from accounts.models import User
from accounts.serializers import UserSerializer
from departments.serializers import DepartmentSerializer, PositionSerializer  # Import PositionSerializer
from departments.models import Department, Position


class EmployeePersonalDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePersonalDetails
        exclude = ['employee']

class EmployeeJobDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeJobDetails
        exclude = ['employee']

class EmployeeSerializer(serializers.ModelSerializer):
    # User-related fields
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)
    username = serializers.CharField(write_only=True)

    user = UserSerializer(read_only=True)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all())
    position = serializers.PrimaryKeyRelatedField(queryset=Position.objects.all())

    # Nested serializers
    personal_details = EmployeePersonalDetailsSerializer(required=False)
    job_details = EmployeeJobDetailsSerializer(required=False)

    class Meta:
        model = Employee
        fields = (
            'first_name', 'last_name', 'email', 'username',
            'department', 'position', 'date_joined', 'user',
            'image', 'personal_details', 'job_details',
        )

    def create(self, validated_data):
        # Extract user-related fields
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email')
        username = validated_data.pop('username')

        # Create the User instance
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username
        )

        # Extract nested data
        personal_details_data = validated_data.pop('personal_details', None)
        job_details_data = validated_data.pop('job_details', None)

        # Create the Employee instance
        employee = Employee.objects.create(user=user, **validated_data)

        # Create nested models
        if personal_details_data:
            EmployeePersonalDetails.objects.create(employee=employee, **personal_details_data)
        if job_details_data:
            EmployeeJobDetails.objects.create(employee=employee, **job_details_data)

        return employee

    def update(self, instance, validated_data):
        # Extract user-related fields
        user_data = {}
        user_fields = ['first_name', 'last_name', 'email', 'username']
        for field in user_fields:
            if field in validated_data:
                user_data[field] = validated_data.pop(field)

        # Update User instance
        if user_data:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        # Extract nested data
        personal_details_data = validated_data.pop('personal_details', None)
        job_details_data = validated_data.pop('job_details', None)

        # Update Employee instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update or create nested models
        if personal_details_data:
            EmployeePersonalDetails.objects.update_or_create(
                employee=instance,
                defaults=personal_details_data
            )
        if job_details_data:
            EmployeeJobDetails.objects.update_or_create(
                employee=instance,
                defaults=job_details_data
            )

        return instance



class EmployeeProfileSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(read_only=True)
    position = PositionSerializer(read_only=True)  # Add PositionSerializer for the position field

    class Meta:
        model = Employee
        fields = ('user', 'department', 'position', 'date_joined', 'documents', 'image')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['first_name'] = instance.user.first_name
        representation['last_name'] = instance.user.last_name
        representation['email'] = instance.user.email
        representation['username'] = instance.user.username
        representation['phone'] = instance.user.phone if hasattr(instance.user, 'phone') else 'N/A'
        return representation



class PersonalInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePersonalDetails
        fields = '__all__'

class JobDetailsSerializer(serializers.ModelSerializer):
    position = PositionSerializer(read_only=True)  # Add PositionSerializer for the job position field

    class Meta:
        model = EmployeeJobDetails
        fields = '__all__'


class DocumentUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ['id', 'name', 'file', 'uploaded_at']
