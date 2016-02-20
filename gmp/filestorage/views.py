import os

from django.conf import settings

from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.views import APIView
from rest_framework.response import Response

class FileUploadView(APIView):
    parser_classes = (FormParser, MultiPartParser, )

    def post(self, request, format=None):
        file_obj = request.data
        up_file = request.FILES['fileupload']
        print('Received file', up_file)
        self.procFile(up_file)
        return Response(status=201)

    def procFile(self, fname):
        saved_file = os.path.join(settings.MEDIA_ROOT, fname.name)
        with open(saved_file, 'wb+') as dest:
            for chunk in fname.chunks():
                dest.write(chunk)

