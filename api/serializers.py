from rest_framework import serializers


# Some fields need to be read and create only.
# I don't currently know how to do this in DRF proper.
#
# User Kangaroux on GitHub suggests something
# like the following:
#
# https://github.com/encode/django-rest-framework/discussions/8606#discussioncomment-3899252
#
# The mixin here may have local modifications.
class UpdateMixin(serializers.ModelSerializer):
    def get_extra_kwargs(self):
        kwargs = super().get_extra_kwargs()
        no_update_fields = getattr(self.Meta, "no_update_fields", None)

        if self.instance and no_update_fields:
            for field in no_update_fields:
                kwargs.setdefault(field, {})
                kwargs[field]["read_only"] = True

        return kwargs
