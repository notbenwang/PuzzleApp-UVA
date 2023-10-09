from django.http import HttpResponse
from django.shortcuts import render
from allauth.socialaccount.models import SocialAccount

from .models import CustomUser


def index(request):
    return HttpResponse("You are at the puzzle index")


def login(request):
    return render(request, "login.html")


def dashboard(request):
    social_id = request.user.id
    
    try:
        custom_user = CustomUser.objects.get(social_id=social_id)
        is_admin = custom_user.is_admin
    except CustomUser.DoesNotExist:
        if social_id:
            custom_user = CustomUser(social_id=social_id, is_admin=False)
            custom_user.save()
            is_admin = False
        else:
            is_admin = False

    return render(request, "dashboard.html", {"is_admin": is_admin})


# Resource
# URL: https://stackoverflow.com/questions/17813919/django-error-matching-query-does-not-exist
# Name: Dracontis
# Date: June 7 2015
# Used to figure out how to handle user not exist exception