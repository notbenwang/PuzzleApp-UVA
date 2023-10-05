from django.http import HttpResponse


def index(request):
    return HttpResponse("You are at the puzzle index")

def login(request):
    return HttpResponse("Login")