from django.urls import reverse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.
@api_view(["GET"])
def root(request):
    if request.method == "GET":
        data = {
            "links": {
                "naans": reverse("naans"),
            },
        }
        return Response(data, status=status.HTTP_200_OK)
