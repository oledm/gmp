from .permissions import IsEmployeeMatch
from .models import Employee, Department
from .serializers import EmployeeSerializer
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework import status

class EmployeeViewset(viewsets.ModelViewSet):
    lookup_field = 'username'
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return (permissions.AllowAny(),)
        
        if self.request.method == 'POST':
            return (permissions.AllowAny(),)

        return (permissions.IsAuthenticated(), IsEmployeeMatch(),)

    def create(self, request):
        data = request.data
        dep_name = data['department']

        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            #print('Valid data:', serializer.validated_data)
            Employee.objects.create_user(**serializer.validated_data, 
                department=Department.objects.get(name=dep_name)
            )
            return Response(dict(serializer.validated_data, department=dep_name),
                status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Невозможно создать пользователя с указанными данными'
            }, status=status.HTTP_400_BAD_REQUEST)
