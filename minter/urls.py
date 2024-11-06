from django.urls import path
from minter import views

urlpatterns = [
    path("naans/", views.NaanList.as_view(), name="naans"),
    path("naans/<int:number>", views.NaanItem.as_view(), name="view-naan"),
]
