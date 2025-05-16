from django.dispatch import receiver
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout as Logout, login as Login
from django.utils.timezone import now
from .models_io import *
from .models import Mission, MissionCompleted, GroupMember, GroupMessage, GroupJoinRequest, User
from .forms import CodeAnswerForm, GroupCreateForm, GroupEditForm
import keyword


# Create your views here.

def main(request):
    if request.user.is_authenticated:
        friends = get_friends(request.user)
        groups = Group.objects.filter(groupmember__user=request.user)
    else:
        friends = []
        groups = []
    return render(request, "programmingCourse/main.html", {
        "friends": friends,
        "groups": groups
    })

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
            Profile.objects.create(user=request.user)
            add_starter_items(request.user)
            return redirect("/")
    else:
        form = UserCreationForm()
    
    return render(request, "programmingCourse/signup.html", {"form": form})

def logout(request):
    Logout(request)
    return redirect("/login")

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
    friend_status = get_friend_status(sender=request.user,
                                      recipient=get_object_or_404(User, username=username))

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

@login_required(login_url="/login")
def friend_list(request):
    friends = get_friends(request.user)
    request_count = len(FriendRequest.objects.filter(recipient=request.user))
    return render(request, "programmingCourse/friend_list.html", {"friends": friends, "friend_request_count": request_count})

@login_required(login_url="/login")
def friend_requests(request):
    senders = get_friend_request_senders(request.user)
    return render(request, "programmingCourse/friend_requests.html", {"requests": senders})

def get_friends(user):
    friends1 = Friend.objects.filter(user1=user).values_list('user2', flat=True)
    friends2 = Friend.objects.filter(user2=user).values_list('user1', flat=True)
    friend_users = User.objects.filter(id__in=list(friends1) + list(friends2))
    return friend_users

@login_required(login_url="/login")
def friend_search(request):
    search = request.GET.get("q", "")
    if search:
        search_results = search_users(search, request.user)
    else:
        search_results = []
    return render(request, "programmingCourse/friend_search.html", {"search_results": search_results})


@login_required(login_url="/login")
def create_group(request):
    if request.method == "POST":
        form = GroupCreateForm(request.POST, request.FILES)
        if form.is_valid():
            group = form.save(commit=False)
            group.groupOwner = request.user
            group.save()
            # Add owner as member
            GroupMember.objects.create(group=group, user=request.user)
            messages.success(request, "Group created successfully!")
            return redirect('programing_course_app:group', name=group.groupName)
    else:
        form = GroupCreateForm()
    return render(request, "programmingCourse/create_group.html", {"form": form})

@login_required(login_url="/login")
def group_settings(request, name):
    group = get_object_or_404(Group, groupName=name)

    if request.user != group.groupOwner:
        messages.error(request, "You are not authorized to edit this group.")
        return redirect("programing_course_app:group", name=name)

    if request.method == "POST":
        form = GroupEditForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "Group settings updated.")
            return redirect("programing_course_app:group", name=name)
    else:
        form = GroupEditForm(instance=group)

    return render(request, "programmingCourse/group_settings.html", {"form": form, "group": group})


@login_required(login_url="/login")
def groupList(request):
    query = request.GET.get("q", "")
    is_private = request.GET.get("private", "")

    if query or is_private != "":
        # You're searching — show all matches
        groups = Group.objects.all()
        if query:
            groups = groups.filter(groupName__icontains=query)
        if is_private == "true":
            groups = groups.filter(is_private=True)
        elif is_private == "false":
            groups = groups.filter(is_private=False)
    else:
        # No query — show only groups user is in
        groups = Group.objects.filter(groupmember__user=request.user)

    return render(request, "programmingCourse/groupList.html", {
        "groups": groups,
        "query": query,
    })


@login_required(login_url="/login")

def group(request, name):
    group = get_object_or_404(Group, groupName=name)
    is_member = GroupMember.objects.filter(group=group, user=request.user).exists()
    is_owner = request.user == group.groupOwner
    join_requested = GroupJoinRequest.objects.filter(group=group, user=request.user).exists()
    member_record = GroupMember.objects.filter(group=group, user=request.user).first()
    members = GroupMember.objects.filter(group=group).select_related("user")

    if request.method == "POST":
        action = request.POST.get("action")
        target_id = request.POST.get("target_id")

        # Handle group admin actions
        if action in ["kick", "mute", "unmute"] and is_owner and target_id:
            target_user = get_object_or_404(User, id=target_id)
            member_entry = GroupMember.objects.filter(group=group, user=target_user).first()

            if member_entry:
                if action == "kick":
                    if target_user == group.groupOwner:
                        messages.error(request, "You cannot kick the group owner.")
                    else:
                        member_entry.delete()
                        messages.success(request, f"{target_user.username} was removed from the group.")
                elif action == "mute":
                    member_entry.is_muted = True
                    member_entry.save()
                    messages.success(request, f"{target_user.username} has been muted.")
                elif action == "unmute":
                    member_entry.is_muted = False
                    member_entry.save()
                    messages.success(request, f"{target_user.username} has been unmuted.")
            return redirect("programing_course_app:group", name=name)

        # Handle join request or leave
        if action == "join":
            if group.is_private:
                if not join_requested:
                    GroupJoinRequest.objects.create(group=group, user=request.user)
                    messages.success(request, "Join request sent.")
            else:
                GroupMember.objects.get_or_create(group=group, user=request.user)
                messages.success(request, "You have joined the group.")
            return redirect("programing_course_app:group", name=name)

        elif action == "leave":
            if not is_owner:
                GroupMember.objects.filter(group=group, user=request.user).delete()
                messages.success(request, "You left the group.")
                return redirect("programing_course_app:groupList")

        # Handle sending a chat message
        if not action and is_member and member_record and not member_record.is_muted:
            content = request.POST.get("message", "").strip()
            if content:
                GroupMessage.objects.create(group=group, user=request.user, message=content)
                return redirect("programing_course_app:group", name=name)

    messages_ = GroupMessage.objects.filter(group=group).order_by("created_at")
    leaderboard = get_group_leaderboard(group)  # henter intern rangering
    top_10 = leaderboard[:10]  # kun de 10 beste
    user_entry = next((i + 1 for i, entry in enumerate(leaderboard) if entry["user"] == request.user), None) 

    return render(request, "programmingCourse/group.html", {
        "group": group,
        "is_member": is_member,
        "is_owner": is_owner,
        "join_requested": join_requested,
        "chat_messages": messages_,
        "members": members,
        "top_10": top_10,                   
        "user_position": user_entry, 
    })

@login_required
def manage_group_requests(request, name):
    group = get_object_or_404(Group, groupName=name)

    if request.user != group.groupOwner:
        messages.error(request, "You are not authorized to manage this group.")
        return redirect("programing_course_app:group", name=name)

    pending_requests = GroupJoinRequest.objects.filter(group=group)

    if request.method == "POST":
        action = request.POST.get("action")
        user_id = request.POST.get("user_id")

        if action and user_id:
            user = get_object_or_404(User, id=user_id)

            if action == "approve":
                GroupMember.objects.get_or_create(group=group, user=user)
                GroupJoinRequest.objects.filter(group=group, user=user).delete()
                messages.success(request, f"Approved {user.username}")

            elif action == "reject":
                GroupJoinRequest.objects.filter(group=group, user=user).delete()
                messages.success(request, f"Rejected {user.username}")

        return redirect("programing_course_app:manage_group_requests", name=name)

    return render(request, "programmingCourse/manage_group_requests.html", {
        "group": group,
        "requests": pending_requests
    })


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
    if mission is None:
        userAnswer = None
    else:
        if not request.user.is_authenticated: userAnswer = None
        else:
            if request.method != "POST":
                userAnswer = get_mission_completed(request.user, mission)
            else:
                userAnswer = set_mission_completed(request.user, mission, request.POST["answer"])
    return render(request, "programmingCourse/mission.html",
                  {"nameCourse": nameCourse, "nameModule": nameModule, "nameMission": nameMission,
                   "mission": mission, "userAnswer": userAnswer})

def shop(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            purchase_item(request.user,request.POST["purchase"])
        userBalance = get_user_balance(request.user)
        catalogue = get_shop_items(request.user)
    else: 
        userBalance = None
        catalogue = get_shop_items(None)
    return render(request, "programmingCourse/shop.html", {"userBalance": userBalance, "catalogue": catalogue})

@login_required(login_url="/login")
def inventory(request):
    if request.method == "POST":
        equip_item(request.user, request.POST["selectedItem"])
    userInventory = get_inventory_items(request.user)
    print(userInventory)
    return render(request, "programmingCourse/inventory.html", {"userInventory": userInventory})

@login_required(login_url="/login")
def gatcha(request):
    price = 3
    if request.user.is_authenticated:
        if request.method == "POST":
            prize = play_gatcha(request.user,price)
        else:
            prize = None
        userBalance = get_user_balance(request.user)
        gatcha_items = get_gatcha_items(request.user)
    else: 
        userBalance = None
        catalogue = get_gatcha_items(None)
    return render(request, "programmingCourse/gatcha.html", {"userBalance": userBalance, "gatcha_items": gatcha_items, "prize":prize, "price": price})

