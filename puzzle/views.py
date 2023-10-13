from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from allauth.socialaccount.models import SocialAccount
from .models import Puzzle, Hunt

from .models import CustomUser

class AddHuntView(generic.DetailView):
    model = Hunt
    template_name = "puzzle/add_hunt.html"
    
class AddPuzzleView(generic.DetailView):
    model = Hunt
    template_name = "puzzle/add_puzzle.html"
    

def index(request):
    return HttpResponse("You are at the puzzle index")

def add_temp_hunt(request, hunt_id):
    try:
        p = Hunt.objects.get(pk=hunt_id)
        return HttpResponseRedirect(reverse("add_hunt_view", args=(p.id,)))
    except Hunt.DoesNotExist:
        p = Hunt(title="",summary="",approved=False)
        p.save()
        return HttpResponseRedirect(reverse("add_hunt_view",args=(p.id,)))
    
def remove_temp_hunt(request, hunt_id):
    Hunt.objects.filter(id=hunt_id).delete()
    return HttpResponseRedirect(reverse("index"))

def submit_hunt(request, hunt_id):
    return 

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