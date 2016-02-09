from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.db import models


class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Введите корректный email.')

        if not kwargs.get('username'):
            raise ValueError('Введите корректное имя пользователя')

        employee = self.model(
            email=self.normalize_email(email),
            username=kwargs.get('username'),
            department_id=kwargs.get('department')
        )

        employee.set_password(password)
        employee.save()

        return employee

    def create_superuser(self, email, password=None, **kwargs):
        employee = self.create_user(email, password, **kwargs)

        employee.is_admin = True
        employee.save()

        return employee


class Department(models.Model):

    name = models.CharField(max_length=100, unique=True)


class Employee(AbstractBaseUser):

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=40, unique=True)

    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)

    department = models.ForeignKey('Department')
    phone = models.CharField(max_length=10, blank=True)
    birth_date = models.DateField(null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    is_admin = models.BooleanField(default=False)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'department']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.last_name, self.first_name])

    def get_short_name(self):
        return self.first_name
