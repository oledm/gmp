import environ
import os
import mimetypes

from django.conf import settings
from django.http import HttpResponse
from django.db import DataError

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
    response['Content-Type'] = 'image/jpeg'

    #verbose_name = request.GET.get('name')
    #if verbose_name:
    #    response['Content-Disposition'] = 'filename="%s"' % verbose_name
    #    type_, encoding = mimetypes.guess_type(verbose_name)
    #    response['Content-Type'] = type_
    #    response['Content-Encoding'] = encoding
    #else:
    #    #response['Content-Disposition'] = 'attachment'
    #    response['Content-Type'] = 'application/octet-stream'
    return response


class FileUploadView(views.APIView):
    parser_classes = (FormParser, MultiPartParser, )

    def post(self, request, format=None):
        file_obj = request.data
        print('Загружается файл', file_obj)
        up_file = request.FILES['fileupload']
        file_ = self.save_to_db(request, up_file)
        if file_:
            return Response({
                'status': 'Created', 
                'message': 'File upload success',
                'id': file_['id'],
                'url': file_['fileupload']
                }, status=status.HTTP_201_CREATED
            )
        else:
            return Response({
                'status': 'Error', 
                'message': 'Слишком длинное имя файла: <small>&laquo;{}&raquo;<small>'.format(up_file)
                }, status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )

    def save_to_db(self, request, fname):
        try:
            f = FileStorage.objects.create(fileupload=fname, uploader=self.request.user)
            files_serialized = FileSerializer(f, context={'request': request})
            return files_serialized.data
        except DataError:
            return None

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

    #def destroy(self, request, pk=None):
    #    pass
        #f = FileStorage.objects.get(pk=pk)
        #f.delete()
        #return Response({
        #    'message': 'File deleted successfully'
        #    }, status.HTTP_204_NO_CONTENT)

        ## Until leave all files on disk - delete only database entry.
        ##
        ##msg = 'File successfully removed'
        ##full_path = os.path.join(settings.MEDIA_ROOT, f.fileupload.name)
        ##print('remove file', full_path)
        ##try:
        ##    os.remove(full_path)
        ##except FileNotFoundError:
        ##    msg = 'File is not found or already removed'
        ##return Response({
        ##    'message': msg
        ##    }, status.HTTP_204_NO_CONTENT)
