from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html")),
    # path('accounts/', include('allauth.urls')),
    path('dashboard/', views.dashboard, name="dashboard")
    # path('logout', LogoutView.as_view()),
    # path('accounts/google/login/', views.login, name='account_login'),
]