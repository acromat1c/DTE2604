from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import logout as Logout, login as Login

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
            return redirect("/login")
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



def subjectList(request):
    return render(request, "programmingCourse/subjectList.html")

def subject(request,namesub):
    return render(request, "programmingCourse/subject.html", {"namesub": namesub})

def mission(request,namesub,name):
    return render(request, "programmingCourse/mission.html", {"namesub": namesub, "name": name})



def test(request):
    return render(request, "programmingCourse/test.html")
