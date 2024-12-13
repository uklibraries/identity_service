from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from minter.models import Naan, Minter
from minter.serializers import NaanSerializer, MinterSerializer


class NaanList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Naan.objects.all()
    serializer_class = NaanSerializer

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        response.data = {
            "links": {
                "self": request.path,
            },
            "data": response.data,
        }
        return response

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        response.data = {
            "links": {
                "self": request.path,
            },
            "data": response.data,
        }
        return response


class NaanItem(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Naan.objects.all()
    serializer_class = NaanSerializer
    lookup_field = "number"

    def get(self, request, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        response.data = {
            "links": {
                "self": request.path,
            },
            "data": response.data,
        }
        return response

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        response.data = {
            "links": {
                "self": request.path,
            },
            "data": response.data,
        }
        return response

    def delete(self, request, *args, **kwargs):
        response = self.destroy(request, *args, **kwargs)
        response.data = {
            "links": {
                "self": request.path,
            },
            "data": response.data,
        }
        return response


class MinterList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Minter.objects.all()
    serializer_class = MinterSerializer

    def perform_create(self, serializer):
        naan = Naan.objects.get(number=self.kwargs["number"])
        serializer.save(naan=naan)

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        response.data = {
            "links": {
                "self": request.path,
            },
            "data": response.data,
        }
        return response


class MinterItem(generics.RetrieveUpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Minter.objects.all()
    serializer_class = MinterSerializer
    lookup_field = "shoulder"

    def get(self, request, *args, **kwargs):
        response = self.retrieve(request, *args, **kwargs)
        response.data.pop("state", None)
        response.data = {
            "links": {
                "self": request.path,
            },
            "data": response.data,
        }
        return response

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        ark = instance.mint()
        serializer = self.get_serializer(
            instance, data={"state": instance.state}, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = serializer.data
        data.pop("state", None)
        data["ark"] = ark
        return Response(
            {
                "links": {
                    "self": request.path,
                },
                "data": data,
            },
            status=status.HTTP_201_CREATED,
        )
