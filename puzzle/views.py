from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from allauth.socialaccount.models import SocialAccount
from .models import Puzzle, Hunt, Hint
import json

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
class AddHintView(generic.DetailView):
    model = Hunt
    template_name = "add_hint.html"
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['context_id'] = self.kwargs['puzzle_id']
        return data
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
def submit_hint(request, hunt_id, puzzle_id):
    p = Puzzle.objects.get(pk=hunt_id)
    if request.method == "POST":
        hint_texts = [request.POST.get('hint1'), request.POST.get('hint2'), request.POST.get('hint3')]
        for hint_text in hint_texts:
            if hint_text:
                hint = Hint(hint_string=hint_text, puzzle_id=puzzle_id)
                hint.save()
        return HttpResponseRedirect(reverse("detail_puzzle", args=(hunt_id,puzzle_id)))
    return HttpResponseRedirect(reverse("detail_puzzle", args=(hunt_id,puzzle_id)))

def submit_puzzle(request, hunt_id):
    r = request.POST.get("radius")
    latLng = request.POST.get("latLng")
    prompt = request.POST.get("prompt")
    hints = []
    for i in range(1,5):
        text = request.POST.get(f"hint{i}")
        if text is not None:
            hints.append(text)
    h = Hunt.objects.get(pk=hunt_id)
    arr = latLng[1:-1].split(", ")
    p = Puzzle(prompt_text=prompt,hunt_id=h, radius=r,long=float(arr[1]), lat=float(arr[0]))
    p.save()
    for hint_text in hints:
        hint = Hint(hint_string=hint_text, puzzle_id=p)
        hint.save()
    return HttpResponseRedirect(reverse("add_temp_hunt", args=(h.id,)))

def submit_hunt(request, hunt_id):
    h = Hunt.objects.get(pk=hunt_id)
    title = request.POST.get("title")
    summary = request.POST.get("summary")
    h.submitted = True
    h.title = title
    h.summary = summary
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