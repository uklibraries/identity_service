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

    def get(self, request, *args, **kwargs):
        response = self.list(request, *args, **kwargs)
        response.data = {
            "links": {
                "self": request.path,
            },
            "data": response.data,
        }
        return response

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
        short_id = data["identifier"].split("/")[1]
        data.setdefault("metadata", {})
        data["metadata"]["id"] = data["identifier"]
        data["metadata"]["short_id"] = short_id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {
                "links": {
                    "self": request.path,
                },
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class ArkBinding(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Ark.objects.all()
    serializer_class = ArkSerializer
    lookup_field = "identifier"

    def patch(self, request, *args, **kwargs):
        kwargs["partial"] = True
        instance = self.get_object()

        key = kwargs.get("key")
        if key is not None:
            value = request.data.get("value")
            instance.metadata[key] = value
        else:
            for key in request.data.keys():
                instance.metadata[key] = request.data.get(key)

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            instance._prefetched_objects_cache = {}

        return Response(
            {
                "links": {
                    "self": request.path,
                },
                "data": serializer.data,
            }
        )
