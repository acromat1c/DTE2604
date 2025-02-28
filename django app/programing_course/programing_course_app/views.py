from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "course/index.html")



def login(request):
    return render(request, "course/login.html")

def signup(request):
    return render(request, "course/signup.html")



def main(request):
    return render(request, "course/main.html")



def user(request):
    return render(request, "course/user.html")

def userSettings(request):
    return render(request, "course/userSettings.html")



def friendList(request):
    return render(request, "course/friendList.html")

def friend(request,name):
    return render(request, "course/friend.html", {"name": name})



def groupList(request):
    return render(request, "course/groupList.html")

def group(request,name):
    return render(request, "course/group.html", {"name": name})



def subjectList(request):
    return render(request, "course/subjectList.html")

def subject(request,namesub):
    return render(request, "course/subject.html", {"namesub": namesub})

def mission(request,namesub,name):
    return render(request, "course/mission.html", {"namesub": namesub, "name": name})