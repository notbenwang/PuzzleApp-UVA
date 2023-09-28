# Benjamin "Ben" Wang @hgf3jq
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]
