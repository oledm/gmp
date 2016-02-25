import os

from django.conf import settings

from rest_framework import views, viewsets, permissions
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from .models import UploadedFile
from .serializers import FileSerializer
from gmp.authentication.models import Employee

class FileUploadView(views.APIView):
    parser_classes = (FormParser, MultiPartParser, )

    def post(self, request, format=None):
        file_obj = request.data
        up_file = request.FILES['fileupload']
        self.proc_file(up_file)
        self.save_to_db(up_file)
        return Response({
            'status': 'Created', 
            'message': 'File upload success'
            }, status=201)

    def proc_file(self, fname):
        saved_file = os.path.join(settings.MEDIA_ROOT, fname.name)
        with open(saved_file, 'wb+') as dest:
            for chunk in fname.chunks():
                dest.write(chunk)

    def save_to_db(self, fname):
        UploadedFile.objects.create(name=fname, uploader=self.request.user)

class FileViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    queryset = UploadedFile.objects.all()
    serializer_class = FileSerializer
    
    # TODO make helper function common for entire project to follow DRY
    # and used it here instead of permission_classes (and test it)
    #def get_permissions(self):

    def destroy(self, request, pk=None):
        f = UploadedFile.objects.get(pk=pk)
        f.delete()

        msg = 'File successfully removed'
        full_path = os.path.join(settings.MEDIA_ROOT, f.name)
        try:
            os.remove(full_path)
        except FileNotFoundError:
            msg = 'File is not found or already removed'
        return Response({
            'message': msg
            }, 204)
