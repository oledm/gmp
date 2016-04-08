import os
from shutil import copyfile

from django.conf import settings
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Storage
from gmp.authentication.models import Employee
from gmp.departments.models import Department

class FileAPI(APITestCase):
    def setUp(self):
        self.testfile = os.path.join(settings.MEDIA_ROOT, 'mail.txt')
        copyfile('mail.txt', self.testfile)
        self.create_url = reverse('storage-list')
        self.user = Employee.objects.create_user(
            email='test@mail.ru',
            password='123',
            department=Department.objects.create(name='Отдел')
        )

    def create_file(self):
        with open(self.testfile) as f:
            response = self.client.post(self.create_url, {
                'uploader': self.user.id,
                'fileupload': f
            })
        return response

    #def test_file_create(self):
    #    uploaded = Storage.objects.create(fileupload='test.jpg',
    #        uploader=self.user)
    #    self.assertEqual(Storage.objects.count(), 1)

    def test_file_create_success_API(self):
        self.client.force_authenticate(user=self.user)
        response = self.create_file()
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Storage.objects.count(), 1)

    #def test_file_create_forbidden_API(self):
    #    response = self.create_file()
    #    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    #    self.assertEqual(Storage.objects.count(), 0)

    #def test_file_create_failed_API(self):
    #    self.client.force_authenticate(user=self.user)
    #    response = self.client.post(self.create_url, {})
    #    self.assertEqual(len(response.data), 2)
    #    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #    self.assertEqual(response.data['uploader'], ['Это поле обязательно.'])
    #    self.assertEqual(response.data['name'], ['Это поле обязательно.'])
    #    self.assertEqual(Storage.objects.count(), 0)

    #def test_file_delete_success_API(self):
    #    self.client.force_authenticate(user=self.user)
    #    response = self.create_file()
    #    fileid = response.data['id']
    #    self.assertEqual(Storage.objects.count(), 1)

    #    response = self.client.delete('{}{}/'.format(self.create_url, fileid))
    #    self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #    self.assertEqual(Storage.objects.count(), 0)

    #    with self.assertRaises(FileNotFoundError):
    #        os.stat(self.testfile)

    #def test_file_delete_failed_API(self):
    #    self.client.force_authenticate(user=self.user)
    #    response = self.create_file()
    #    fileid = response.data['id']
    #    self.client.logout()
    #    response = self.client.delete('{}{}/'.format(self.create_url, fileid))
    #    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #def test_read_file_list_access_denied_API(self):
    #    response = self.client.get(self.create_url)
    #    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #def test_read_file_list_success_API(self):
    #    self.client.force_authenticate(user=self.user)
    #    response = self.client.get(self.create_url)
    #    self.assertEqual(response.status_code, status.HTTP_200_OK)
    #    self.assertEqual(response.data, [])
    #    self.create_file()
    #    self.create_file()
    #    response = self.client.get(self.create_url)
    #    self.assertEqual(response.status_code, status.HTTP_200_OK)
    #    self.assertEqual(len(response.data), 2)
