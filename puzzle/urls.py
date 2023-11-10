from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path("<int:hunt_id>/add_temp_hunt", views.add_temp_hunt, name="add_temp_hunt"),
    path("<int:pk>/add_hunt", views.AddHuntView.as_view(), name="add_hunt_view"),
    path("<int:pk>/add_puzzle", views.AddPuzzleView.as_view(), name="add_puzzle_view"),
    path("<int:hunt_id>/submit_puzzle", views.submit_puzzle, name="submit_puzzle"),
    path("<int:puzzle_id>/submit_edited_puzzle", views.submit_edited_puzzle, name="submit_edited_puzzle"),
    # path("<int:pk>/puzzle/<int:puzzle_id>", views.DetailPuzzleView.as_view(), name="detail_puzzle"),
    path("<int:hunt_id>/puzzle/<int:puzzle_id>", views.get_detail_puzzle, name="detail_puzzle"),
    path("<int:hunt_id>/submit_hunt", views.submit_hunt, name="submit_hunt"),
    path("<int:hunt_id>/hunt", views.view_hunt, name="view_hunt"),
    # path("<int:pk>/add_hint/<int:puzzle_id>", views.AddHintView.as_view(), name="add_hint_view"),
    # path("<int:pk>/puzzle/<int:puzzle_id>/submit_hint", viewSs.submit_hint, name="submit_hint"),
    path("<int:hunt_id>/approve/hunt", views.approve_hunt, name="approve_hunt"),
    path("<int:hunt_id>/view/deny", views.view_deny, name="view_deny"),
    path("<int:hunt_id>/deny/hunt", views.deny_hunt, name="deny_hunt"),
    path("<int:hunt_id>/play_hunt", views.play_hunt, name="play_hunt"),
    path("<int:hunt_id>/reset", views.reset_session, name="reset_session"),
    path("<int:hunt_id>/play/<int:session_id>", views.play_puzzle, name="play_puzzle"),
    path("<int:hunt_id>/play/<int:session_id>/request_hint", views.request_hint, name="request_hint"),
    path("<int:hunt_id>/play/<int:session_id>/results", views.get_puzzle_result, name="get_puzzle_result"),
    path("<int:hunt_id>/play/<int:session_id>/next", views.go_next_puzzle, name="get_next_puzzle"),
    path("admin_settings/", views.admin_view, name="admin_settings"),
    path("admin_settings/set_admin", views.set_admin, name="set_admin"),
    # path('accounts/', include('allauth.urls')),
    # path('logout', LogoutView.as_view()),
    # path('accounts/google/login/', views.login, name='account_login'),
]