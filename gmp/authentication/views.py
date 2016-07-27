import json

from django.contrib.auth import authenticate, login, logout

from rest_framework import permissions, viewsets, generics, views, status
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings

from .serializers import EmployeeSerializer
from .permissions import IsEmployeeMatch
from .models import Employee
from .forms import ContactForm, DepartmentFormSet
from gmp.departments.models import Department


def get_token(user):
    # Obtaning JWT
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)
    return token

def jwt_payload_handler(user=None):
    #print('jwt_payload_handler for user', user)
    if not user:
        return {}

    user_data = EmployeeSerializer(user).data
    #print('user_data', user_data)
    return {
        'username': user_data.get('email'),
        'user': user_data
    }

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

    def list(self, request, department_pk=None):
        department = Department.objects.get(pk=department_pk)
        employee = self.queryset.filter(department=department)
        serializer = EmployeeSerializer(employee , many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, department_pk=None):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid(raise_exception=True):
            department = Department.objects.get(pk=department_pk)
            user = Employee.objects.create_user(**serializer.validated_data, department=department)
            token = get_token(user)
            return Response({'token': token},
                status=status.HTTP_201_CREATED)

        return Response({
            'status': 'Bad request',
            'message': 'Невозможно создать пользователя с указанными данными'
            }, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, username, pk=None, department_pk=None):
        print('update')
        data = request.data
        serializer = self.serializer_class(data=data, context={'request': request}, partial=True)
        if serializer.is_valid(raise_exception=True):
            #print('Serializer errors', serializer.errors)
            #print('valideted data:', serializer.validated_data)
            user = self.get_object()
            serializer.update(user, serializer.validated_data)
            return Response(dict(serializer.validated_data, full_fio=user.get_full_name()),
                status=status.HTTP_200_OK)
        return Response({
            'status': 'Bad request',
            'message': 'Невозможно обновить данные пользователя'
            }, status=status.HTTP_400_BAD_REQUEST)
