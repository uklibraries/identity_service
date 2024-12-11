from django.urls import path
from binder import views

urlpatterns = [
    path("roles/<int:number>/", views.RoleList.as_view(), name="roles"),
    path("arks/<int:number>/<str:identifier>/<int:role>/", views.ArkList.as_view(), name="arks"),
]
