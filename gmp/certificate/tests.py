from datetime import date
from rest_framework.test import APITestCase
from rest_framework import status

from gmp.authentication.models import Employee
from gmp.departments.models import Department
from .models import Certificate

class CertificateSerializerTest(APITestCase):

    def createCert(self):
        self.certificate = Certificate.objects.create(
            employee=self.user,
            received_at=date.today(),
            expired_at=date.today(),
            control='ВИК',
            degree=1,
            group=3
        )

    def setUp(self):
        self.user = Employee.objects.create_user(
            email='test@mail.ru',
            password='123',
            department=Department.objects.create(name='Отдел')
        )

    def test_read_certificates(self):
        response = self.client.get('/api/user/{}/certificates/'.format(
            self.user.username
        ))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

        self.createCert()

        response = self.client.get('/api/user/{}/certificates/'.format(
            self.user.username
        ))
        self.assertEqual(len(response.data), 1)
