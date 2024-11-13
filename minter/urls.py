from django.urls import path
from minter import views

urlpatterns = [
    path("naans/", views.NaanList.as_view(), name="naans"),
    path("naans/<int:number>", views.NaanItem.as_view(), name="view-naan"),
    path("minters/<int:number>/", views.MinterList.as_view(), name="minters"),
    path("minters/<int:number>/<str:shoulder>", views.MinterItem.as_view(), name="view-minter"),
]
