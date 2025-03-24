from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout as Logout, login as Login
from django.utils.timezone import now
from .models_io import *
from .models import Mission, MissionCompleted
from .forms import CodeAnswerForm
import keyword
import datetime


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
    return render(request, "programmingCourse/main.html")


@login_required(login_url="/login")


@login_required(login_url="/login")
def userSettings(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    password_form = PasswordChangeForm(request.user, request.POST or None)  # Allow empty form
    updated = False  # Track if any changes were made

    if request.method == "POST":
        # Update username if provided
        new_username = request.POST.get("username")
        if new_username and new_username != request.user.username:
            request.user.username = new_username
            request.user.save()
            messages.success(request, "Username updated successfully!")
            updated = True

        # Update profile picture if uploaded
        if 'profile_image' in request.FILES:
            profile.image = request.FILES['profile_image']
            profile.save()
            messages.success(request, "Profile picture updated successfully!")
            updated = True

        # Change password only if all fields are filled and valid
        if request.POST.get("old_password") or request.POST.get(
                "new_password1") or request.POST.get("new_password2"):
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request,
                                         user)  # Keep user logged in after password change
                messages.success(request, "Password updated successfully!")
                updated = True
            else:
                messages.error(request, "Error updating password. Please check your input.")

        # Redirect only if a change was made
        if updated:
            return redirect("programing_course_app:userSettings")

    return render(request, "programmingCourse/userSettings.html", {
        "password_form": password_form,
        "profile": profile
    })


@login_required(login_url="/login")
def user(request, username):

    user_profile = get_object_or_404(User, username=username)
    friend_status = get_friend_status(sender=request.user, recipient=get_object_or_404(User, username=username))

    return render(request, "programmingCourse/user.html", 
                  {
                  "user_profile": user_profile,
                  "friend_status": friend_status
                  }
                  )

@login_required(login_url="/login")
def add_friend(request, username):
    sender = request.user
    recipient = get_object_or_404(User, username=username)

    if request.method == "POST" and request.POST.get("friendaction") == "add":
        if friend_request(sender=sender, recipient=recipient):
            messages.success(request, "Friend request sent")
        else:
            messages.error(request, "Failed to send a friend request")

    elif request.method == "POST" and request.POST.get("friendaction") == "undo":
        if undo_friend_request(sender=sender, recipient=recipient):
            messages.success(request, "Friend request deleted")
        else:
            messages.error(request, "Failed to delete friend request")

    elif request.method == "POST" and request.POST.get("friendaction") == "accept":
        if accept_friend_request(accepter=sender, sender=recipient):
            messages.success(request, "Friend request accepted")
        else:
            messages.error(request, "Failed to accept friend request")

    elif request.method == "POST" and request.POST.get("friendaction") == "decline":
        if decline_friend_request(recipient=sender, sender=recipient):
            messages.success(request, "Friend request declined")
        else:
            messages.error(request, "Failed to decline friend request")

    elif request.method == "POST" and request.POST.get("friendaction") == "remove":
        if remove_friend(remover=sender, friend=recipient):
            messages.success(request, "Friend removed")
        else:
            messages.error(request, "Failed to remove friend")

    return redirect("programing_course_app:user", username=username)


def friendList(request):
    friends = get_friends(request.user)
    return render(request, "programmingCourse/friendList.html", {"friends": friends})


def friend(request, name):
    return render(request, "programmingCourse/friend.html", {"name": name})


def groupList(request):
    return render(request, "programmingCourse/groupList.html")


def group(request, name):
    return render(request, "programmingCourse/group.html", {"name": name})


def overview(request):
    listCourse = get_course_list()
    return render(request, "programmingCourse/overview.html", {"listCourse": listCourse})


def course(request, nameCourse):
    course = get_course(nameCourse)
    listModule = get_module_list(nameCourse)
    return render(request, "programmingCourse/course.html",
                  {"nameCourse": nameCourse, "course": course, "listModule": listModule})


def module(request, nameCourse, nameModule):
    module = get_module(nameCourse, nameModule)
    listMission = get_mission_list(nameCourse, nameModule)
    return render(request, "programmingCourse/module.html",
                  {"nameCourse": nameCourse, "nameModule": nameModule, "module": module,
                   "listMission": listMission})


def mission(request, nameCourse, nameModule, nameMission):
    mission = get_mission(nameCourse, nameModule, nameMission)
    if mission == None:
        userAnswer = None
    else:
        if request.method == "POST":
            if request.POST["answer"] == mission.answer:
                points = mission.maxPoints
            else:
                points = 0
            userAnswer, _ = set_mission_completed(mission.id, request.user.id, points, now(),
                                                  request.POST["answer"])
        else:
            userAnswer = get_mission_completed(mission.id, request.user.id)

    return render(request, "programmingCourse/mission.html",
                  {"nameCourse": nameCourse, "nameModule": nameModule, "nameMission": nameMission,
                   "mission": mission, "userAnswer": userAnswer})


def test(request):
    return render(request, "programmingCourse/test.html")


def validate_answer(mission, user_input):
    if "3.4.4" in mission.module.name:
        parts = user_input.split("=")
        if len(parts) == 2:
            var = parts[0].strip()
            return var.isidentifier() and not keyword.iskeyword(var)
        return False
    return user_input.strip() == mission.answer.strip()
