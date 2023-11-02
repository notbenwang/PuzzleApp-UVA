from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from allauth.socialaccount.models import SocialAccount
from .models import Puzzle, Hunt
import json

from .models import CustomUser

class AddHuntView(generic.DetailView):
    model = Hunt
    template_name = "puzzle/add_hunt.html"

class EditHuntView(generic.DetailView):
    model = Hunt
    template_name = "puzzle/edit_hunt.html"
    
class AddPuzzleView(generic.DetailView):
    model = Hunt
    template_name = "puzzle/add_puzzle.html"

class EditPuzzleView(generic.DetailView):
    model = Hunt
    template_name = "puzzle/edit_puzzle.html"

class DetailPuzzleView(generic.DetailView):
    model = Puzzle
    template_name = "detail_puzzle.html"

def create_custom_user(request):
    social_id = request.user.id

    try:
        custom_user = CustomUser.objects.get(social_id=social_id)
    except CustomUser.DoesNotExist:
        if social_id:
            custom_user = CustomUser(social_id=social_id, is_admin=False)
            custom_user.save()
            is_admin = False

def index(request):
    return HttpResponse("You are at the puzzle index")

def add_temp_hunt(request, hunt_id):
    create_custom_user(request)
    try:
        p = Hunt.objects.get(pk=hunt_id)
        return HttpResponseRedirect(reverse("add_hunt_view", args=(p.id,)))
    except Hunt.DoesNotExist:
        try:
            #First check to see if last hunt was not submitted. If so, use that hunt
            creator = CustomUser.objects.get(social_id=request.user.id)
            most_recent_hunt = Hunt.objects.filter(creator=creator).latest("pk")
            if not most_recent_hunt.submitted:
                p = most_recent_hunt
            else:
                creator = CustomUser.objects.get(social_id=request.user.id)
                p = Hunt(title="",summary="",approved=False, creator=creator)
                p.save()

            return HttpResponseRedirect(reverse("add_hunt_view",args=(p.id,)))

        except Hunt.DoesNotExist:
            creator = CustomUser.objects.get(social_id=request.user.id)
            p = Hunt(title="", summary="", approved=False, creator=creator)
            p.save()

            return HttpResponseRedirect(reverse("add_hunt_view",args=(p.id,)))
        
def edit_hunt(request, hunt_id):
    create_custom_user(request)
    try:
        p = Hunt.objects.get(pk=hunt_id)
        return HttpResponseRedirect(reverse("edit_hunt_view", args=(p.id,)))
    except Hunt.DoesNotExist:
        try:
            #First check to see if last hunt was not submitted. If so, use that hunt
            creator = CustomUser.objects.get(social_id=request.user.id)
            most_recent_hunt = Hunt.objects.filter(creator=creator).latest("pk")
            if not most_recent_hunt.submitted:
                p = most_recent_hunt
            else:
                creator = CustomUser.objects.get(social_id=request.user.id)
                p = Hunt(title="",summary="",approved=False, creator=creator)
                p.save()

            return HttpResponseRedirect(reverse("edit_hunt_view",args=(p.id,)))

        except Hunt.DoesNotExist:
            creator = CustomUser.objects.get(social_id=request.user.id)
            p = Hunt(title="", summary="", approved=False, creator=creator)
            p.save()

            return HttpResponseRedirect(reverse("edit_hunt_view",args=(p.id,)))


def submit_puzzle(request, hunt_id):
    r = request.POST.get("radius")
    latLng = request.POST.get("latLng")
    arr = latLng[1:-1].split(", ")

    h = Hunt.objects.get(pk=hunt_id)
    # Should change "test" to some Post object
    p = Puzzle(prompt_text="test",hunt_id=h, radius=r,long=float(arr[1]), lat=float(arr[0]))
    p.save()
    return HttpResponseRedirect(reverse("add_temp_hunt", args=(h.id,)))

def submit_hunt(request, hunt_id):
    h = Hunt.objects.get(pk=hunt_id)
    h.submitted = True
    h.save()
    return HttpResponseRedirect(reverse("dashboard"))

def view_hunt(request, hunt_id):
    hunt = Hunt.objects.get(pk=hunt_id)
    return render(request, "detail_hunt.html", {"hunt": hunt})

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

    hunts = Hunt.objects.filter(approved=True)
    authors = list(map(lambda x: x.creator, hunts))

    def get_user(custom_user):
        try:
            if custom_user:
                return SocialAccount.objects.get(pk=custom_user.social_id)
            else:
                return None
        except SocialAccount.DoesNotExist:
            return None

    authors = list(map(get_user, authors))
    zipped_hunts = zip(hunts, authors)
    zipped_admin = None

    if is_admin:
        admin_queue = Hunt.objects.filter(approved=False, submitted=True)
        admin_authors = list(map(lambda x: x.creator, admin_queue))
        admin_authors = list(map(get_user, admin_authors))
        zipped_admin = zip(admin_queue, admin_authors)

    return render(request, "dashboard.html", {"is_admin": is_admin, "zipped_hunts": zipped_hunts, "zipped_admin": zipped_admin})

def approve_hunt(request, hunt_id):
    hunt = Hunt.objects.get(pk=hunt_id)
    hunt.approved = True
    hunt.save()

    return HttpResponseRedirect(reverse("dashboard"))

def deny_hunt(request, hunt_id):
    hunt = Hunt.objects.get(pk=hunt_id)
    hunt.delete()

    return HttpResponseRedirect(reverse("dashboard"))

# Resource
# URL: https://stackoverflow.com/questions/17813919/django-error-matching-query-does-not-exist
# Name: Dracontis
# Date: June 7 2015
# Used to figure out how to handle user not exist exception

#Resource
# URL: https://stackoverflow.com/questions/39944474/django-get-the-max-pk
# Name: CodeTherapy
# Date: Oct 31 2021
# Used to figure out how to get latest obejct by pk

#Resource
# URL: https://stackoverflow.com/questions/2415865/iterating-through-two-lists-in-django-templates
# Name: Mermoz
# Date: Nov 21 2010
# Used to learn to zip lists to deliver mappings to view

