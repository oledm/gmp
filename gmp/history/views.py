from rest_framework import viewsets, permissions
from .models import Input
from .serializers import InputSerializer

class InputViewset(viewsets.ModelViewSet):
    queryset = Input.objects.all()
    serializer_class = InputSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Input.objects.filter(employee=self.request.user)
