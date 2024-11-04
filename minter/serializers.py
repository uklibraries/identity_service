from rest_framework import serializers
from minter.models import Naan


class NaanSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    organization = serializers.CharField(max_length=255)
    abbreviation = serializers.CharField(max_length=5)

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
