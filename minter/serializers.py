from rest_framework import serializers
from minter.models import Naan
from api.serializers import UpdateMixin
from api.exceptions import ValidateFieldsMixin


class NaanSerializer(ValidateFieldsMixin, UpdateMixin, serializers.ModelSerializer):
    id = serializers.IntegerField()
    organization = serializers.CharField(max_length=255)
    abbreviation = serializers.CharField(max_length=5)

    class Meta:
        model = Naan
        fields = ["id", "organization", "abbreviation"]
        no_update_fields = ["id"]

    def create(self, validated_data):
        return Naan.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.organization = validated_data.get(
            "organization", instance.organization
        )
        instance.abbreviation = validated_data.get(
            "abbreviation", instance.abbreviation
        )
        instance.save()
        return instance
