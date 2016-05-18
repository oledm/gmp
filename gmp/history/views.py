from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Input
from .serializers import InputSerializer

class InputViewset(viewsets.ModelViewSet):
    queryset = Input.objects.all()
    serializer_class = InputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Input.objects.filter(employee=self.request.user).order_by('-date')

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if (serializer.is_valid()):
            #print('Validated data:', serializer.validated_data)
            history = Input.objects.create(obj_model=data['obj_model'],
                employee=self.request.user)
            return Response({'id': history.id},
                status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Invalid data'},
                    status=status.HTTP_403_FORBIDDEN)

    #def update(self, request, pk=None):
    #    print('update history', pk)
    #    print('data', request.data)
    #    return Response('OK',
    #            status=status.HTTP_403_FORBIDDEN)
