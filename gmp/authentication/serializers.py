from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from .models import Employee
from gmp.departments.models import Department
from gmp.departments.serializers import DepartmentSerializer

class EmployeeSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=False)
    department = DepartmentSerializer()
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Employee
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
            'birth_date', 'phone', 'created_at', 'modified_at', 'department',
            'is_admin', 'password', 'confirm_password',
        )

        read_only_fields = ('created_at', 'modified_at', 'username')

    def create(self, validated_data):
        print('Serializer create run')
        #dep_name = validated_data.pop('department')['name']
        #department = Department.objects.get(name=dep_name)
        return Employee.objects.create(**validated_data, department=department)

    def update(self, instance, validated_data):
        #print('UPDATE serializer method')
        #dep_name = validated_data.get('department', instance.department)['name']
        #department = Department.objects.get(name=dep_name)
        #print('NEW DEP:', department)
        instance.email = validated_data.get('email', instance.email)
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        print('validated data from update:', validated_data)
        #instance.department = department
        instance.phone = validated_data.get('phone', instance.phone)

        instance.save()

        password = validated_data.get('password', None)
        confirm_password = validated_data.get('confirm_password', None)

        if password and confirm_password and password == confirm_password:
            instance.set_password(password)
            instance.save()

        update_session_auth_hash(self.context.get('request'), instance)

        return instance
