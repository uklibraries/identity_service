from django.urls import path
from binder import views

urlpatterns = [
    path("roles/", views.RoleList.as_view(), name="roles"),
    path("roles/<int:number>/", views.RoleList.as_view(), name="roles"),
    path("arks/<path:identifier>/", views.ArkList.as_view(), name="arks"),
]
