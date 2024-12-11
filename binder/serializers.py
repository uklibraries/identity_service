from rest_framework import serializers
from minter.models import Naan
from binder.models import Ark, Role


class RoleSerializer(serializers.ModelSerializer):
    number = serializers.SlugRelatedField(
        slug_field = "number",
        queryset = Naan.objects.all(),
        required = False,
    )

    name = serializers.CharField(max_length=255)

    class Meta:
        model = Role
        fields = ["number", "name"]
        extra_kwargs = {"number": {"required": True}}


class ArkSerializer(serializers.ModelSerializer):
    role = RoleSerializer(many=False, read_only=True)
    identifier = serializers.CharField(max_length=255, default="unidentified")

    class Meta:
        model = Ark
        fields = ["identifier", "role"]
