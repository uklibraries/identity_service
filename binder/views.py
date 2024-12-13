from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from binder.models import Ark, Role
from binder.serializers import ArkSerializer, RoleSerializer
from minter.models import Naan


class RoleList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def perform_create(self, serializer):
        naan = Naan.objects.get(number=self.kwargs["number"])
        serializer.save(naan=naan)


class ArkList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Ark.objects.all()
    serializer_class = ArkSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        data["identifier"] = kwargs.pop("identifier", "unidentified")
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
