from rest_framework import serializers
from minter.models import Naan, Minter


class NaanSerializer(serializers.ModelSerializer):
    organization = serializers.CharField(max_length=255)
    abbreviation = serializers.CharField(max_length=5)

    class Meta:
        model = Naan
        fields = ["id", "number", "organization", "abbreviation"]


class MinterSerializer(serializers.ModelSerializer):
    number = serializers.SlugRelatedField(
        slug_field="number",
        queryset=Naan.objects.all(),
        required=False,
    )

    shoulder = serializers.CharField(max_length=5)
    template = serializers.CharField(max_length=64)
    state = serializers.JSONField(required=False)

    class Meta:
        model = Minter
        fields = ["id", "number", "shoulder", "template", "state"]
        extra_kwargs = {"number": {"required": True}}
