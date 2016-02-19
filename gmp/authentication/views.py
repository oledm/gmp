import json

from django.contrib.auth import authenticate, login, logout
from rest_framework import permissions, viewsets, generics, views
from rest_framework.response import Response
from rest_framework import status

from .serializers import EmployeeSerializer, DepartmentSerializer
from .permissions import IsEmployeeMatch
from .models import Employee, Department


class LoginView(views.APIView):
    def post(self, request, format=None):
        data = request.data
        email = data.get('email', None)
        password = data.get('password', None)
        account = authenticate(email=email, password=password)

        if account is not None:
            if account.is_active:
                login(request, account)

                serialized = EmployeeSerializer(account)
                return Response(serialized.data)
            else:
                return Response({
                    'status': 'Unauthorized',
                    'message': 'This account is disabled'
                    }, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination incorrect'
                }, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(views.APIView):
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request, format=None):
        logout(request)

        return Response({}, status=status.HTTP_204_NO_CONTENT)

class DepartmentList(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

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
            Employee.objects.create_user(**serializer.validated_data, 
                department=Department.objects.get(name=dep_name)
            )
            return Response(dict(serializer.validated_data, department=dep_name),
                status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Невозможно создать пользователя с указанными данными'
            }, status=status.HTTP_400_BAD_REQUEST)

    #def update(self, request, username, pk=None):
    #    data = request.data
    #    print('updated object is', self.get_object())
    #    data['department'] = 2
    #    print('data is ', data)
    #    serializer = self.serializer_class(data=data)
    #    print('Is data valid?', serializer.is_valid())
    #    serializer.update(self.get_object())
    #    return Response(dict(serializer.validated_data),
    #        status=status.HTTP_200_OK)
