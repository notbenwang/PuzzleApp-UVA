from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', TemplateView.as_view(template_name="index.html"), name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path("<int:hunt_id>/add_temp_hunt", views.add_temp_hunt, name="add_temp_hunt"),
    path("<int:pk>/edit_hunt", views.EditHuntView.as_view(), name="edit_hunt_view"),
    path("<int:pk>/add_hunt", views.AddHuntView.as_view(), name="add_hunt_view"),
    path("<int:pk>/add_puzzle", views.AddPuzzleView.as_view(), name="add_puzzle_view"),
    path("<int:pk>/edit_puzzle", views.EditPuzzleView.as_view(), name="edit_puzzle_view"),
    path("<int:hunt_id>/submit_puzzle", views.submit_puzzle, name="submit_puzzle"),
    path("<int:pk>/puzzle/<int:puzzle_id>", views.DetailPuzzleView.as_view(), name="detail_puzzle"),
    path("<int:hunt_id>/submit_hunt", views.submit_hunt, name="submit_hunt"),
    path("<int:hunt_id>/hunt", views.view_hunt, name="view_hunt"),
    path("<int:hunt_id>/approve/hunt", views.approve_hunt, name="approve_hunt"),
    path("<int:hunt_id>/deny/hunt", views.deny_hunt, name="deny_hunt"),
    # path('accounts/', include('allauth.urls')),
    # path('logout', LogoutView.as_view()),
    # path('accounts/google/login/', views.login, name='account_login'),
]