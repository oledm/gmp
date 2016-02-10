from .permissions import IsEmployeeMatch
from .models import Employee, Department
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

        return (permissions.IsAuthenticated(), IsEmployeeMatch(),)

    def create(self, request):
        data = request.data
        print('Unvalidated data:', data)

        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            print('Valid data:', serializer.validated_data)
            Employee.objects.create_user(**serializer.validated_data)
            print(len(Employee.objects.all()))

            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)


        return Response({
            'status': 'Bad request',
            'message': 'Невозможно создать пользователя с указанными данными'
            }, status=status.HTTP_400_BAD_REQUEST)
