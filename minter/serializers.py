from rest_framework import serializers
from minter.models import Naan


class NaanSerializer(serializers.ModelSerializer):
#class NaanSerializer(CreateReadOnlyModelSerializer):
    id = serializers.IntegerField(read_only=True)
    organization = serializers.CharField(max_length=255)
    abbreviation = serializers.CharField(max_length=5)

    class Meta:
        model = Naan
        fields = ["id", "number", "organization", "abbreviation"]
