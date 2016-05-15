from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Input
from .serializers import InputSerializer

class InputViewset(viewsets.ModelViewSet):
    queryset = Input.objects.all()
    serializer_class = InputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Input.objects.filter(employee=self.request.user)

    def create(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        if (serializer.is_valid()):
            #print('Validated data:', serializer.validated_data)
            history = Input.objects.create(obj_model=data['obj_model'],
                employee=self.request.user)
            return Response({
                'message': 'Input history recorded',
                'id': history.id
                },
                status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.validated_data,
                    status=status.HTTP_403_FORBIDDEN)
    #def update(self, request, pk=None):
    #    print('update history', pk)
    #    return Response('OK',
    #            status=status.HTTP_403_FORBIDDEN)

