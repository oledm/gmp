from django.test import TestCase
from django.db.utils import IntegrityError
from django.utils import timezone
from django.core.exceptions import ValidationError

from rest_framework.renderers import JSONRenderer
from rest_framework.test import APIClient

from gmp.authentication.models import Employee, Department
from gmp.authentication.serializers import EmployeeSerializer

class EmployeeTest(TestCase):
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

class EmployeeSerializerTest(TestCase):
    def setUp(self):
        self.department = Department.objects.create(name='Тестовый отдел')
        #print('ОТДЕЛ:', str(self.department))
        now = timezone.now()
        self.userdata = dict(
            email='test@mail.ru', username='TestAdmin',
            first_name='Имя', last_name='Фамилия', department=self.department.name,
            phone='79101234567', birth_date=now.date(),
            created_at=now, modified_at=now, is_admin=False
        )
    def test_post(self):
        client = APIClient()
        client.post('/api/user/', self.userdata)
        response = client.get('/api/user/')
        print(response.content)

    #def test_serialize_correctly(self):
    #    Employee.objects.create(**self.userdata)
    #    response = self.client.get('/api/user/')
    #    self.assertEquals(response.status_code, 200)
    #    print(response.content)
    #    serializer = EmployeeSerializer(data=response.content)
    #    serializer.is_valid()
    #    print('SERIALIZED:', serializer.data)
    #    #print('SERIALIZED VALIDATED:', serializer.validated_data)
    #    ##print('SERIALIZED JSON:', JSONRenderer().render(self.userdata))
    #    #print('GENERIC:', self.userdata)

    #    ##self.assertDictEqual(self.userdata, serialized_data.data)
