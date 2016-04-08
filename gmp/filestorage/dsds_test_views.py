import os
from shutil import copyfile

from django.conf import settings
from django.core.urlresolvers import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import Storage
from gmp.authentication.models import Employee
from gmp.departments.models import Department

class FileHashing(APITestCase):
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
                'fileupload': f, 
                'uploader': self.user.id,
                'name': self.testfile
            })
        return response

    def test_file_create(self):
        uploaded = Storage.objects.create(name='test.jpg', uploader=self.user)
        self.assertEqual(Storage.objects.count(), 1)

