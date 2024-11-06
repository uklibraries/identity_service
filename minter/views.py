from rest_framework import generics, serializers, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from minter.models import Naan
from minter.serializers import NaanSerializer


class NaanList(generics.ListCreateAPIView):
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
