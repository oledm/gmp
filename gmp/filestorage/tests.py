from rest_framework.test import APITestCase
from .models import UploadedFile
from gmp.authentication.models import Employee, Department

class FileAPI(APITestCase):
    def setUp(self):
        self.testfile = './mail.txt'
        self.user = Employee.objects.create(
            email='masdar@list.ru',
            password='123',
            department=Department.objects.create(name='Отдел')
        )

    def test_file_create(self):
        uploaded = UploadedFile.objects.create(name='test.jpg',
            uploader=self.user)
        self.assertEqual(UploadedFile.objects.count(), 1)

    def test_file_create_API(self):
        with open(self.testfile) as f:
            self.client.post('/api/file/', {'fileupload':f})
        self.assertEqual(UploadedFile.objects.count(), 1)
