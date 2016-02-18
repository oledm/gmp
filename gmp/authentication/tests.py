from django.db.utils import IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError

from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from rest_framework import status

from gmp.authentication.models import Employee, Department
from gmp.authentication.serializers import EmployeeSerializer

class EmployeeTest(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Тестовый отдел')
        self.email = 'test@mail.ru'
        self.email2 = self.email + '2'
        self.username = 'TestAdmin'
        self.username2 = self.username + '2'

    def test_create_one_employee(self):
        employee = Employee.objects.create(
            email=self.email,
            username=self.username,
            department=self.department
        )
        self.assertEquals(employee.email, self.email)
        self.assertEquals(employee.username, self.username)
        self.assertEquals(str(employee.department), self.department.name)

    def test_create_duplicate_employee(self):
        with self.assertRaisesRegex(IntegrityError,
                'authentication_employee_email_key'):
            employee1 = Employee.objects.create(
                email=self.email,
                username=self.username,
                department=self.department
            )
            employee2 = Employee.objects.create(
                email=self.email,
                username=self.username,
                department=self.department
            )

    def test_create_one_employee_omitting_department(self):
        with self.assertRaisesRegex(IntegrityError,
                    'нулевое значение в колонке "department_id"'):
            employee = Employee.objects.create(
                email=self.email,
                username=self.username,
            )

    def test_create_one_employee_omitting_email(self):
        with self.assertRaises(ValidationError):
            employee = Employee.objects.create(
                username=self.username,
                department=self.department
            )

    def test_create_two_employees(self):
        employee1 = Employee.objects.create(
            email=self.email,
            username=self.username,
            department=self.department
        )
        employee2 = Employee.objects.create(
            email=self.email2,
            username=self.username2,
            department=Department.objects.create(name='Второй отдел')
        )
        self.assertEquals(len(Employee.objects.all()), 2)

    def test_cascade_delete_department_deletes_employees(self):
        employee = Employee.objects.create(
            email=self.email,
            username=self.username,
            department=self.department
        )
        self.assertEquals(len(Employee.objects.all()), 1)
        self.department.delete()
        self.assertEquals(len(Employee.objects.all()), 0)

    def test_update_employee(self):
        employee = Employee.objects.create(
            email=self.email,
            username=self.username,
            department=self.department
        )
        employee.username = 'new nick!'
        employee.first_name = 'Новое имя'
        employee.last_name = 'Новая фамилия'
        employee.save()

        with self.assertRaises(IntegrityError):
            employee2 = Employee.objects.create(
                email=self.email2,
                username=self.username2,
                department=Department.objects.create(name='Второй отдел')
            )
            employee.email = self.email2
            employee.save()

class EmployeeCreateTest(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Тестовый отдел')
        self.email = 'test@mail.ru'
        self.username = self.email.split('@')[0]
        now = timezone.now()
        self.full_user_data = dict(
            email=self.email, first_name='Имя', last_name='Фамилия',
            department=self.department.name, phone='79101234567',
            birth_date=now.date(), is_admin=False
        )
        self.required_user_data = dict(
            email='test@mail.ru', department=self.department.name,
            is_admin=False # это необязательно. Но т.к. у is_admin есть
            # default-значение, то, пропустив данный ключ, словари с
            # исходными данными и с ответом не совпадут.
        )

    def test_post_all_user_data(self):
        response = self.client.post('/api/user/', self.full_user_data)
        self.assertEqual(dict(response.data), self.full_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_required_user_data(self):
        response = self.client.post('/api/user/', self.required_user_data)
        self.assertEqual(dict(response.data), self.required_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auto_generate_username(self):
        self.client.post('/api/user/', self.required_user_data)
        user_url = '/api/user/{}/'.format(self.username)
        response = self.client.get(user_url)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data.get('username'), self.username)

    def test_post_admin_data(self):
        self.required_user_data.update({'is_admin': True})
        response = self.client.post('/api/user/', self.required_user_data)
        self.assertEqual(dict(response.data), self.required_user_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

class EmployeeUpdateTest(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Тестовый отдел')
        self.email = 'test@mail.ru'
        self.username = self.email.split('@')[0]
        self.required_user_data = dict(
            email=self.email, department=self.department.name,
            password='123', is_admin=False
        )

    def test_update_user_data(self):
        self.client.post('/api/user/', self.required_user_data)
        user_url = '/api/user/{}/'.format(self.username)
        response = self.client.get(user_url)
        self.assertEquals(response.data['first_name'], '')

        self.client.login(username='test@mail.ru', password='123')
        self.required_user_data['first_name'] = 'Tester'
        response = self.client.put(user_url, self.required_user_data)
        self.assertEquals(response.data['first_name'], 'Tester')
