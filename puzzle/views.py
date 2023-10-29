from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from allauth.socialaccount.models import SocialAccount
from .models import Puzzle, Hunt, Hint
import math

from .models import CustomUser

class AddHuntView(generic.DetailView):
    model = Hunt
    template_name = "puzzle/add_hunt.html"
    
class AddPuzzleView(generic.DetailView):
    model = Hunt
    template_name = "puzzle/add_puzzle.html"

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


def submit_puzzle(request, hunt_id):
    r = request.POST.get("radius")
    latLng = request.POST.get("latLng")
    arr = latLng[1:-1].split(", ")

    h = Hunt.objects.get(pk=hunt_id)
    # Should change "test" to some Post object
    size = len(Puzzle.objects.filter(hunt_id=hunt_id))
    
    p = Puzzle(prompt_text="test",hunt_id=h, radius=r,long=float(arr[1]), lat=float(arr[0]), order=size)
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

    return render(request, "dashboard.html", {"is_admin": is_admin, "hunts": hunts})

def play_hunt(request, hunt_id):
    return HttpResponseRedirect(reverse("play_puzzle", kwargs={"hunt_id" : hunt_id, "order" : 0, "hint_amount" : 0}))

def play_puzzle(request, hunt_id, order, hint_amount):
    h = Hunt.objects.get(pk=hunt_id)
    p = Puzzle.objects.filter(order = order, hunt_id = h)
    hints = Hint.objects.filter(puzzle_id = p.first())
    return render(request, "play_puzzle.html", {"puzzles": p, 
                                                "prompt":hints.first, 
                                                "hints":hints[1:hint_amount+1], 
                                                "hint_amount":hint_amount, 
                                                "order":order, "hunt":h})

def request_hint(request, hunt_id, order, hint_amount):
    h = Hunt.objects.get(pk=hunt_id)
    p = Puzzle.objects.filter(order = order, hunt_id = h)
    hints = Hint.objects.filter(puzzle_id = p.first())
    if hint_amount+1 < len(hints):
        hint_amount+=1
    return HttpResponseRedirect(reverse("play_puzzle", kwargs={"hunt_id" : hunt_id, "order" : order, "hint_amount": hint_amount}))

def get_puzzle_result(request, hunt_id, order):
    hunt = Hunt.objects.get(pk=hunt_id)
    puzzle = Puzzle.objects.filter(order = order, hunt_id = hunt).first()
    latLng = request.POST.get("latLng")
    arr = latLng[1:-1].split(", ")
    guess_lat = float(arr[0])
    guess_lng = float(arr[1])
    lat = puzzle.lat
    lng = puzzle.long
    radius = puzzle.radius

    diff_lat = guess_lat - lat
    diff_lng = guess_lng - lng
    distance = math.sqrt(pow(diff_lat,2) + pow(diff_lng,2)) * 364000 
    miles = distance / 5280
    return render(request, "play_puzzle_result.html", {"distance":round(distance, 4), "miles":round(miles, 4), 
                                                       "hunt_id" : hunt_id, "order" : order,
                                                       "lat": lat, "lng": lng, "guess_lat":guess_lat, "guess_lng":guess_lng})



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