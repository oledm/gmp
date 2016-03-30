from datetime import date
from rest_framework.test import APITestCase
from rest_framework import status

from gmp.authentication.models import Employee
from gmp.departments.models import Department
from .models import Certificate, ControlType
from .serializers import CertificateSerializer

class CertificateSerializerTest(APITestCase):

    def createCert(self):
        self.control_type = ControlType.objects.create(
            name='ВИК',
            full_name='Визуально измерительный контроль')
        self.certificate = Certificate.objects.create(
            employee=self.user,
            received_at_year=2001,
            received_at_month=9,
            expired_at_year=2006,
            expired_at_month=9,
            serial_number='321-AAA-67',
            degree=1
        )
        self.certificate.save()
        self.certificate.control_types.add(self.control_type)

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
        print('data:', response.data)
        serializer = CertificateSerializer(data=response.data, many=True)
        print('is valid:', serializer.is_valid())
        print('validated data:', serializer.validated_data)
