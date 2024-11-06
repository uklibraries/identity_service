from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from minter.models import Naan
from minter.serializers import NaanSerializer


@api_view(["GET", "POST"])
def naans(request):
    partial_response = {
        "links": {
            "self": request.path,
        },
    }
    if request.method == "GET":
        naans = Naan.objects.all()
        serializer = NaanSerializer(naans, many=True)
        return Response(
            {
                **partial_response,
                **{
                    "data": serializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = NaanSerializer(data=data)
        if serializer.is_valid():
            serializer.create(data)
            return Response(
                {
                    **partial_response,
                    **{
                        "data": serializer.data,
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PATCH", "DELETE"])
def view_naan(request, naan_id):
    try:
        the_naan = Naan.objects.get(id=naan_id)
        partial_response = {
            "links": {
                "self": request.path,
            },
        }
    except Naan.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = NaanSerializer(the_naan)
        return Response(
            {
                **partial_response,
                **{
                    "data": serializer.data,
                },
            },
            status=status.HTTP_200_OK,
        )

    elif request.method == "PATCH":
        update_data = JSONParser().parse(request)
        serializer = NaanSerializer(the_naan, data=update_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    **partial_response,
                    **{
                        "data": serializer.data,
                    },
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {
                **partial_response,
                **{
                    "errors": serializer.errors,
                },
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    elif request.method == "DELETE":
        the_naan.delete()
        return Response(
            {
                "links": {
                    "self": request.path,
                },
            },
            status=status.HTTP_204_NO_CONTENT,
        )
