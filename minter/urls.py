from django.urls import path
from minter import views

urlpatterns = [
    path("naans/", views.naans, name="naans"),
    path("naans/<int:naan_id>", views.view_naan, name="view-naan"),
]
