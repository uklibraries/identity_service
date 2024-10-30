from django.urls import path
from minter import views

urlpatterns = [
    path("naans/", views.naans, name="naans"),
]
