from rest_framework.test import APITestCase
from rest_framework import status

from .models import UploadedFile
from gmp.authentication.models import Employee, Department

class FileAPI(APITestCase):
    def setUp(self):
        self.testfile = 'mail.txt'
        self.api_endpoint = '/api/file/'
        self.user = Employee.objects.create_user(
            email='test@mail.ru',
            password='123',
            department=Department.objects.create(name='Отдел')
        )

    def create_file(self):
        with open(self.testfile) as f:
            response = self.client.post(self.api_endpoint, {
                'fileupload': f, 
                'uploader': self.user.id,
                'name': 'name'
            })
        return response

    def test_file_create(self):
        uploaded = UploadedFile.objects.create(name='test.jpg',
            uploader=self.user)
        self.assertEqual(UploadedFile.objects.count(), 1)

    def test_file_create_success_API(self):
        self.client.force_authenticate(user=self.user)
        response = self.create_file()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(UploadedFile.objects.count(), 1)

    def test_file_create_forbidden_API(self):
        response = self.create_file()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(UploadedFile.objects.count(), 0)

    def test_file_create_failed_API(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.api_endpoint, {})
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['uploader'], ['This field is required.'])
        self.assertEqual(response.data['name'], ['This field is required.'])
        self.assertEqual(UploadedFile.objects.count(), 0)

    def test_file_delete_success_API(self):
        self.client.force_authenticate(user=self.user)
        response = self.create_file()
        fileid = response.data['id']
        response = self.client.delete('{}{}/'.format(self.api_endpoint, fileid))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_file_delete_failed_API(self):
        self.client.force_authenticate(user=self.user)
        response = self.create_file()
        fileid = response.data['id']
        self.client.logout()
        response = self.client.delete('{}{}/'.format(self.api_endpoint, fileid))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
