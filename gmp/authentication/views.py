from .permissions import IsEmployeeIdent
from .models import Employee
from .serializers import EmployeeSerializer
from rest_framework import permissions, viewsets

class EmployeeViewset(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsEmployeeIdent(),)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            Employee.objects.create_user(**serializer.validated_data)

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Невозможно создать пользователя с указанными данными'
            }, status=status.HTTP_400_BAD_REQUEST)
