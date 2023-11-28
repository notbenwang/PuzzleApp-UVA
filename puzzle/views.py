from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from .models import Puzzle, Hunt, Hint, Session, Guess
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
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['hints'] = Hint.objects.filter(puzzle_id = self.kwargs['puzzle_id'])
        return data

def get_detail_puzzle(request, hunt_id, puzzle_id):
    p = Puzzle.objects.get(pk=puzzle_id)
    hints = Hint.objects.filter(puzzle_id=p)
    hint_array = [0] * 4
    i = 0
    for hint in hints:
        hint_array[i] = hint
        i+=1
    return render(request, "detail_puzzle.html", {"puzzle": p, "hints": hints, 
                                                  "hint1" : hint_array[0],
                                                  "hint2" : hint_array[1],
                                                  "hint3" : hint_array[2],
                                                  "hint4" : hint_array[3],})

def create_custom_user(request):
    social_id = request.user.id

    try:
        custom_user = CustomUser.objects.get(social_id=social_id)
    except CustomUser.DoesNotExist:
        if social_id:
            custom_user = CustomUser(social_id=social_id, is_admin=False)
            custom_user.save()
            is_admin = False
    return custom_user


def index(request):
    if request.user.id:
        return HttpResponseRedirect(reverse("dashboard"))
    else:
        return HttpResponseRedirect("accounts/google/login")


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
        
def submit_edited_puzzle(request, puzzle_id):
    r = request.POST.get("radius")
    latLng = request.POST.get("latLng")
    p = Puzzle.objects.get(pk=puzzle_id)
    if latLng:
        arr = latLng[1:-1].split(", ")
        p.lat = float(arr[0])
        p.long = float(arr[1])
    prompt = request.POST.get("prompt")
    
    hint_texts = []
    if request.method == "POST":
        for i in range(1,5):
            text = request.POST.get(f"hint{i}")
            if text is not None:
                hint_texts.append(text)
        hints = Hint.objects.filter(puzzle_id=p)
        
        i = 0
        for hint in hints:
            if i < len(hint_texts):
                if hint_texts[i]:
                    hint.hint_string = hint_texts[i]
                    hint.save()
            else:
                hint.delete()
            i += 1

        while i < len(hint_texts):
            if hint_texts[i]:
                hint = Hint(hint_string=hint_texts[i], puzzle_id=p)
                hint.save()
                i+=1

    p.prompt_text = prompt
    p.radius = r
    p.save()
    return HttpResponseRedirect(reverse("add_temp_hunt", args=(p.hunt_id.id,)))

def delete_puzzle(request, hunt_id, puzzle_id):
    hunt = Hunt.objects.get(pk=hunt_id)
    puzzles = Puzzle.objects.filter(hunt_id = hunt)
    p = Puzzle.objects.get(pk=puzzle_id)
    p_order = p.order

    found = False
    for puzzle in puzzles:
        order = puzzle.order
        if found:
            puzzle.order -= 1
            puzzle.save()
        elif order == p_order:
            found = True
            p.delete()
    return HttpResponseRedirect(reverse("add_temp_hunt", args=(p.hunt_id.id,)))
    
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
    size = len(Puzzle.objects.filter(hunt_id=hunt_id))
    p = Puzzle(prompt_text=prompt,hunt_id=h, radius=r,long=float(arr[1]), lat=float(arr[0]), order=size)
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
    if not social_id:
        return HttpResponseRedirect(reverse("index"))

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
                return SocialAccount.objects.get(pk=custom_user.id)
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
    social_id = request.user.id
    custom_user = CustomUser.objects.get(social_id=social_id)
    is_admin = custom_user.is_admin

    if is_admin:
        hunt = Hunt.objects.get(pk=hunt_id)
        hunt.submitted = False
        hunt.comments = request.POST.get("comments")
        hunt.save()

    return HttpResponseRedirect(reverse("dashboard"))

def view_deny(request, hunt_id):
    social_id = request.user.id
    custom_user = CustomUser.objects.get(social_id=social_id)
    is_admin = custom_user.is_admin

    if is_admin:
        hunt = Hunt.objects.get(pk=hunt_id)
        return render(request, "deny_hunt.html", {"hunt": hunt})
    else:
        return HttpResponseRedirect(reverse("dashboard"))

def get_session(request, hunt_id):
    user = create_custom_user(request)
    h = Hunt.objects.get(pk=hunt_id)
    try:
        session = Session.objects.get(player=user, hunt_id = h)
    except Session.DoesNotExist:
        session = Session(player=user, hunt=h)
        session.save()
    return session

def play_hunt(request, hunt_id):
    session = get_session(request, hunt_id)
    if session.completed:
        order = session.current_puzzle
        return render(request, "hunt_results.html", {"hunt_id":hunt_id, "score":session.total_score, 
                                                     "hints":session.total_hints_used, "possible_score":(order-1)*5000})
    elif session.finished_puzzle:
        return HttpResponseRedirect(reverse("get_puzzle_result", kwargs={"hunt_id":hunt_id, "session_id":session.id}))
    else:
        return HttpResponseRedirect(reverse("play_puzzle", kwargs={"hunt_id":hunt_id, "session_id" : session.id}))

def reset_session(request, hunt_id):
    session = get_session(request=request, hunt_id=hunt_id)
    if session.completed:
        session.delete()
        return HttpResponseRedirect(reverse("play_hunt", kwargs={"hunt_id":hunt_id}))
    

def play_puzzle(request, hunt_id, session_id):
    session = Session.objects.get(pk=session_id)
    h = Hunt.objects.get(pk=hunt_id)
    order = session.current_puzzle
    session.finished_puzzle = False
    session.save()
    hint_amount = session.current_hints_used
    p = Puzzle.objects.filter(order = order, hunt_id = h)
    hints = Hint.objects.filter(puzzle_id = p.first())
    return render(request, "play_puzzle.html", {"puzzles": p, 
                                                "prompt": p.first().prompt_text, 
                                                "hints":hints[0:hint_amount], 
                                                "hint_amount":hint_amount, 
                                                "order":order, "hunt":h,
                                                "session_id":session.id })

def request_hint(request, hunt_id, session_id):
    session = Session.objects.get(pk=session_id)
    h = Hunt.objects.get(pk=hunt_id)
    order = session.current_puzzle
    hint_amount = session.current_hints_used
    p = Puzzle.objects.filter(order = order, hunt_id = h)
    hints = Hint.objects.filter(puzzle_id = p.first())
    if hint_amount < len(hints):
        session.current_hints_used += 1
        session.total_hints_used += 1
        session.save()
    return HttpResponseRedirect(reverse("play_puzzle", kwargs={"hunt_id":hunt_id, "session_id" : session.id}))

def get_puzzle_result(request, hunt_id, session_id):
    session = Session.objects.get(pk=session_id)
    order = session.current_puzzle
    hint_amount = session.current_hints_used
    hunt = Hunt.objects.get(pk=hunt_id)
    
    if session.finished_puzzle:
        puzzle = Puzzle.objects.filter(order = order-1, hunt_id = hunt).first()
        guesses = Guess.objects.filter(session = session, order = order-1)
    else:
        puzzle = Puzzle.objects.filter(order = order, hunt_id = hunt).first()
        guesses = Guess.objects.filter(session = session, order = order)
    
    if len(guesses) > 0:
        guess = guesses.first()
        guess_lat = guess.lat
        guess_lng = guess.long
    else:
        latLng = request.POST.get("latLng")
        arr = latLng[1:-1].split(", ")
        guess_lat = float(arr[0])
        guess_lng = float(arr[1])
        guess = Guess(session=session, order=order, lat = guess_lat, long =guess_lng)
        guess.save()

    lat = puzzle.lat
    lng = puzzle.long
    radius = puzzle.radius
    radius_feet = radius * 4.07585 # Magic number

    diff_lat = guess_lat - lat
    diff_lng = guess_lng - lng
    distance = math.sqrt(pow(diff_lat,2) + pow(diff_lng,2)) * 364000 # Magic numbers
    if distance < radius_feet:
        distance = 0
    else:
        distance -= radius_feet
    miles = distance / 5280
    score = 5000 - (10*distance) - 500 * (hint_amount)
    score = int(round(score/50, 0) * 50)
    if score <= 0:
        score = 0
   
    if not session.finished_puzzle:
        session.total_score += score
        session.current_hints_used = 0
        session.current_puzzle += 1
    session.finished_puzzle = True
    session.save()
    return render(request, "play_puzzle_result.html", {"distance":round(distance, 4), "miles":round(miles, 4), 
                                                       "hunt_id" : hunt_id, "order" : order,
                                                       "lat": lat, "lng": lng, "guess_lat":guess_lat, "guess_lng":guess_lng, "radius":radius,
                                                       "session_id" : session_id, "score": score})

def go_next_puzzle(request, hunt_id, session_id):
    hunt = Hunt.objects.get(pk=hunt_id)
    session = Session.objects.get(pk=session_id)
    order = session.current_puzzle
    puzzles = Puzzle.objects.filter(hunt_id=hunt)
    if (order < len(puzzles)):
        return HttpResponseRedirect(reverse("play_puzzle", kwargs={"hunt_id":hunt_id, "session_id" : session.id}))
    else:
        session.completed = True
        session.save()
        return render(request, "hunt_results.html", {"hunt_id":hunt_id, "score":session.total_score, 
                                                     "hints":session.total_hints_used, "possible_score":(order)*5000})


def get_social_user(custom_user):
    try:
        social_user = User.objects.get(pk=custom_user.social_id)
        return social_user
    except User.DoesNotExist:
        return None

def admin_view(request):
    social_id = request.user.id
    custom_user = CustomUser.objects.get(social_id=social_id)
    is_admin = custom_user.is_admin

    users = CustomUser.objects.all()

    social_users = list(map(get_social_user, users))
    user_zip = zip(users, social_users)
    user_zip = list(filter(lambda x: x[1] and x[1].email, user_zip))

    return render(request, "admin.html", {"is_admin": is_admin, "user_zip": user_zip})



def set_admin(request):
    users = CustomUser.objects.all()

    for user in users:
        should_be_admin = request.POST.get("admin_" + str(user.social_id)) != None
        setattr(user, 'is_admin', should_be_admin)
        user.save()

    return HttpResponseRedirect(reverse("admin_settings"))


def my_hunts(request):
    creator = CustomUser.objects.get(social_id=request.user.id)
    hunts = Hunt.objects.filter(creator=creator)

    return render(request, "my_hunts.html", {"hunts": hunts})


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

# Resource
# URL: https://stackoverflow.com/questions/1545645/how-to-set-django-model-field-by-name
# Name: Paul McMillan
# Date: 0ct 9 2009
# Used to learn how to set attributes in model

