from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

class EmployeeManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('Введите корректный email.')
        if not kwargs.get('username'):
            kwargs['username'] = email.split('@')[0]
        if not kwargs.get('department'):
            raise ValueError('Введите название отдела')

        employee = self.model(email=self.normalize_email(email), **kwargs)
        employee.set_password(password)
        employee.save()

        return employee

    def create_superuser(self, email, password=None, **kwargs):
        employee = self.create_user(email, password, **kwargs)

        employee.is_admin = True
        employee.save()

        return employee

    def get_by_full_name(self, full_name):
        last_name, first_name, middle_name = full_name.split()
        return super(EmployeeManager, self).get(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name
        )

class Employee(AbstractBaseUser):

    email = models.EmailField('Электронная почта', blank=True, unique=True)
    username = models.CharField('Имя пользователя', max_length=40, unique=True)

    last_name = models.CharField('Фамилия', max_length=40, blank=True)
    first_name = models.CharField('Имя', max_length=40, blank=True)
    middle_name = models.CharField('Отчество', max_length=40, blank=True)

    department = models.ForeignKey(
        'departments.Department', 
        on_delete=models.CASCADE,
        verbose_name='Отдел'
    )
    phone = models.CharField('Номер телефона', max_length=11, blank=True)
    birth_date = models.DateField('День рождения', blank=True)

    created_at = models.DateTimeField('Дата создания учетной записи', auto_now_add=True)
    modified_at = models.DateTimeField('Дата изменения учетной записи', auto_now=True)

    is_admin = models.BooleanField('Является администратором', default=True)

    objects = EmployeeManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'department']

    class Meta:
        ordering = ['last_name', 'first_name', 'middle_name']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email

    def get_full_name(self):
        return ' '.join([self.last_name, self.first_name, self.middle_name])
    get_full_name.short_description = 'Фамилия И.О.'

    def fio(self):
        return '{} {}.{}.'.format(self.last_name, self.first_name[0], self.middle_name[0])

    def get_short_name(self):
        return self.first_name

    @property
    def is_superuser(self):
        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    def save(self, *args, **kwargs):
        self.email = self.email.lower().strip()
        if self.email != "": 
            validate_email(self.email)
        else:
            raise ValidationError('Введите корректный email.') 
        super(Employee, self).save(*args, **kwargs)

    def get_certs_by_abbr(self, name):
        return self.certificate_set.filter(control_types__name=name)

    def get_cert_details(self, name):
        return self.certificate_set.get(control_types__name=name).verbose_info2(name)
