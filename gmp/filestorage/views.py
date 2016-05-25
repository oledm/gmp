import environ
import os
import mimetypes

from django.conf import settings
from django.http import HttpResponse

from rest_framework import views, viewsets, permissions, status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import FileStorage
from .serializers import FileSerializer
from gmp.authentication.models import Employee


def file_response(request):
    dir_ = str(environ.Path(settings.MEDIA_ROOT) - 1)
    full_filename = os.path.join(dir_, request.path[1:])
    file_ = open(full_filename, 'rb')
    response = HttpResponse(file_.read())

    verbose_name = request.GET.get('name')
    if verbose_name:
        response['Content-Disposition'] = 'filename="%s"' % verbose_name
        type_, encoding = mimetypes.guess_type(verbose_name)
        response['Content-Type'] = type_
        response['Content-Encoding'] = encoding
    else:
        #response['Content-Disposition'] = 'attachment'
        response['Content-Type'] = 'application/octet-stream'
    return response


class FileUploadView(views.APIView):
    parser_classes = (FormParser, MultiPartParser, )

    def post(self, request, format=None):
        file_obj = request.data
        print('file_obj', file_obj)
        up_file = request.FILES['fileupload']
        #self.proc_file(up_file)
        file_ = self.save_to_db(request, up_file)
        return Response({
            'status': 'Created', 
            'message': 'File upload success',
            'id': file_['id'],
            'url': file_['fileupload']
            }, status=status.HTTP_201_CREATED)

    def proc_file(self, fname):
        saved_file = os.path.join(settings.MEDIA_ROOT, fname.name)
        with open(saved_file, 'wb+') as dest:
            for chunk in fname.chunks():
                dest.write(chunk)

    def save_to_db(self, request, fname):
        f = FileStorage.objects.create(fileupload=fname, uploader=self.request.user)
        files_serialized = FileSerializer(f, context={'request': request})
        return files_serialized.data

class FileViewset(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated,)

    queryset = FileStorage.objects.all()
    serializer_class = FileSerializer
    
    # TODO make helper function common for entire project to follow DRY
    # and used it here instead of permission_classes (and test it)
    #def get_permissions(self):

    def list(self, request):
        user = Employee.objects.get(email=self.request.user)
        files = FileStorage.objects.filter(uploader=user)
        files_serialized = FileSerializer(files, context={'request': request}, many=True)
        return Response(files_serialized.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        print('destroy file')
        f = FileStorage.objects.get(pk=pk)
        f.delete()
        return Response({
            'message': 'File deleted successfully'
            }, status.HTTP_204_NO_CONTENT)

        # Until leave all files on disk - delete only database entry.
        #
        #msg = 'File successfully removed'
        #full_path = os.path.join(settings.MEDIA_ROOT, f.fileupload.name)
        #print('remove file', full_path)
        #try:
        #    os.remove(full_path)
        #except FileNotFoundError:
        #    msg = 'File is not found or already removed'
        #return Response({
        #    'message': msg
        #    }, status.HTTP_204_NO_CONTENT)
