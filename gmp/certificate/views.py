from rest_framework import viewsets, status
from rest_framework.response import Response

from .serializers import CertificateSerializer
from .models import Certificate
from gmp.authentication.models import Employee


class CertificateViewset(viewsets.ViewSet):
    queryset = Certificate.objects.all()
    serializer_class = CertificateSerializer

    def list(self, request, user_username=None):
        employee = Employee.objects.get(username=user_username)
        certificates = self.queryset.filter(employee=employee)
        serializer = CertificateSerializer(certificates, many=True)
        #print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
