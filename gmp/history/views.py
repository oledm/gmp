from django.forms.models import model_to_dict
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from .models import Input
from .serializers import InputSerializer
from gmp.departments.models import Department

class InputViewset(viewsets.ModelViewSet):
    queryset = Input.objects.all()
    serializer_class = InputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        report_types = Department.objects.get(employee__email=self.request.user).report_types
        report_urls = tuple(map(lambda x: x.get('url'), report_types.values()))

        return Input.objects.filter(
            employee=self.request.user,
            obj_model__has_key='type',
            obj_model__type__in=report_urls
        ).order_by('-date')

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if (serializer.is_valid()):
            history = Input.objects.create(obj_model=data['obj_model'],
                employee=self.request.user)
            return Response({'id': history.id},
                status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Invalid data'},
                    status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, pk=None):
        try:
            id_ = int(pk)
            history = Input.objects.get(
                pk=id_,
                employee=self.request.user,
                obj_model__has_key='type'
            )
            return Response(model_to_dict(history),
                status=status.HTTP_200_OK)
        except (ValueError, ObjectDoesNotExist):
            return Response(
                {'message': 'Отсутствуют данные об отчете с id ' + pk},
                status=status.HTTP_404_NOT_FOUND)
        return Response(
                {'message': 'Нет данных'},
            status=status.HTTP_404_NOT_FOUND)

    #def list(self, request):
    #    print('list')
    #    #serializer = self.serializer_class(self.get_queryset()[0])
    #    for res in self.get_queryset():
    #        print(res.id)
    #        print(self.serializer_class(res).data)
    #    #data = map(lambda x: self.serializer_class(x).data, )
    #    #print(list(data))

    #def update(self, request, pk=None):
    #    print('update history', pk)
    #    print('data', request.data)
    #    return Response('OK',
    #            status=status.HTTP_403_FORBIDDEN)
