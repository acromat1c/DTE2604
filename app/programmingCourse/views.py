from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout as Logout, login as Login
from django.utils.timezone import now
from .models_io import *

# Create your views here.
def index(request):
    return render(request, "programmingCourse/index.html")



def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            Login(request, form.get_user())
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "programmingCourse/login.html", {"form": form})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            Login(request, form.save())
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(request, "programmingCourse/signup.html", {"form": form})

def logout(request):
    Logout(request)
    return redirect("/login")



def main(request):
    if request.user.is_authenticated:
         user = request.user.username
    else:
        user = "Guest"
    return render(request, "programmingCourse/main.html", {"user": user})



def user(request):
    return render(request, "programmingCourse/user.html")

def userSettings(request):
    return render(request, "programmingCourse/userSettings.html")



def friendList(request):
    return render(request, "programmingCourse/friendList.html")

def friend(request,name):
    return render(request, "programmingCourse/friend.html", {"name": name})



def groupList(request):
    return render(request, "programmingCourse/groupList.html")

def group(request,name):
    return render(request, "programmingCourse/group.html", {"name": name})



def overview(request):
    listCourse = get_course_list()
    return render(request, "programmingCourse/overview.html", {"listCourse": listCourse})

def course(request, nameCourse):
    course = get_course(nameCourse)
    listModule = get_module_list(nameCourse)
    return render(request, "programmingCourse/course.html", {"nameCourse": nameCourse, "course": course, "listModule": listModule})

def module(request, nameCourse, nameModule):
    module = get_module(nameCourse, nameModule)
    listMission = get_mission_list(nameCourse, nameModule)
    return render(request, "programmingCourse/module.html", {"nameCourse": nameCourse, "nameModule": nameModule, "module": module, "listMission": listMission})




def mission(request, nameCourse, nameModule, nameMission):
    mission = get_mission(nameCourse, nameModule, nameMission)
    if mission == None: userAnswer = None
    else:
        if request.method == "POST":
            if request.POST["answer"] == mission.answer:
                points = mission.maxPoints
            else: points = 0
            userAnswer, _ = set_mission_completed(mission.id, request.user.id, points, now(), request.POST["answer"])
        else:
            userAnswer = get_mission_completed(mission.id, request.user.id)

    return render(request, "programmingCourse/mission.html", {"nameCourse": nameCourse, "nameModule": nameModule, "nameMission": nameMission, "mission": mission, "userAnswer": userAnswer})




def test(request):
    return render(request, "programmingCourse/test.html")
