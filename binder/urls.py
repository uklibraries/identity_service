from django.urls import path, register_converter
from binder import converters, views

register_converter(converters.ArkConverter, "ark")

urlpatterns = [
    path("roles/", views.RoleList.as_view(), name="roles"),
    path("roles/<int:number>/", views.RoleList.as_view(), name="roles"),
    path("arks/<ark:identifier>/", views.ArkList.as_view(), name="arks"),
    path(
        "arks/<ark:identifier>/metadata/",
        views.ArkBinding.as_view(),
        name="ark-bind-metadata",
    ),
    path(
        "arks/<ark:identifier>/<path:key>", views.ArkBinding.as_view(), name="ark-bind"
    ),
]
