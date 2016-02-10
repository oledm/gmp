from django.contrib.auth import update_session_auth_hash
from rest_framework import serializers

from .models import Employee, Department

class EmployeeSerializer(serializers.ModelSerializer):
    department = serializers.SlugRelatedField(read_only=True, slug_field='name')
    password = serializers.CharField(write_only=True, required=False)
    confirm_password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = Employee
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
            'birth_date', 'phone', 'created_at', 'modified_at', 'department',
            'password', 'confirm_password',
        )

        read_only_fields = ('created_at', 'modified_at',)

        def create(self, validated_data):
            print('from create:', validated_data)
            return Employee.objects.create(**validated_data)


        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.birth_date = validated_data.get('birth_date', instance.birth_date)
            instance.first_name = validated_data.get('first_name', instance.first_name)
            instance.last_name = validated_data.get('last_name', instance.last_name)

            instance.save()

            password = validated_data.get('password', None)
            confirm_password = validated_data.get('confirm_password', None)

            if password and confirm_password and password == confirm_password:
                instance.set_password(password)
                instance.save()

            update_session_auth_hash(self.context.get('request'), instance)
