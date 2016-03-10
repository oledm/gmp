from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Organization, LPU
from .serializers import OrganizationSerializer, LPUSerializer

class OrganizationViewset(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

class LPUViewset(viewsets.ViewSet):
    queryset = LPU.objects.all()
    serializer_class = LPUSerializer

    def list(self, request, organization_pk=None):
        lpus = self.queryset.filter(organization=organization_pk)
        return Response(self.serializer_class(lpus, many=True).data,
            status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None, domain_pk=None):
        print('LPU retrieve', pk, domain_pk)
        nameservers = self.queryset.get(pk=pk, domain=domain_pk)
        return Response(serializer.data)
