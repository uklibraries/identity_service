from rest_framework import serializers
from minter.models import Naan
from binder.models import Role


class RoleSerializer(serializers.ModelSerializer):
    number = serializers.SlugRelatedField(
        slug_field = "number",
        queryset = Naan.objects.all(),
        required=False,
    )

    name = serializers.CharField(max_length=255)

    class Meta:
        model = Role
        fields = ["number", "name"]
        extra_kwargs = {"number": {"required": True}}
