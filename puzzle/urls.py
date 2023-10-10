from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path("add_hunt", views.AddHuntView.as_view(), name="add_hunt"),
    path("add_puzzle", views.AddPuzzleView.as_view(), name="add_puzzle")
    # path('accounts/', include('allauth.urls')),
    # path('logout', LogoutView.as_view()),
    # path('accounts/google/login/', views.login, name='account_login'),
]