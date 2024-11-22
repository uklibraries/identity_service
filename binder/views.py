from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from binder.models import Role
from binder.serializers import RoleSerializer
from minter.models import Naan


class RoleList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def perform_create(self, serializer):
        naan = Naan.objects.get(number=self.kwargs["number"])
        serializer.save(naan=naan)
