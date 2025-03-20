from .models import *

def get_course_list():
    try:
        return Course.objects.values_list("name", "description")
    except:
        return None

def get_course(nameCourse):
    try:
        return Course.objects.get(name=nameCourse)
    except:
        return None

def get_module_list(nameCourse):
    try:
        return Module.objects.filter(course__name=nameCourse).values_list("name", "description")
    except:
        return None

def get_module(nameCourse, nameModule):
    try:
        return Module.objects.get(name=nameModule, course__name=nameCourse)
    except:
        return None

def get_mission_list(nameCourse, nameModule):
    try:
        return Mission.objects.filter(module=Module.objects.get(name=nameModule, course__name=nameCourse).id).values_list("name", "description")
    except:
        return None

def get_mission(nameCourse, nameModule, nameMission):
    try:
        return Mission.objects.get(name=nameMission, module=Module.objects.get(name=nameModule, course__name=nameCourse).id)
    except:
        return None

def get_mission_completed(missionId, user):
    try:
        return MissionCompleted.objects.get(user=user, mission=missionId)
    except:
        return None

def set_mission_completed(missionId, user, points, time, answer):
    mission_completed, created = MissionCompleted.objects.update_or_create(
        mission=Mission.objects.get(id=missionId),
        user=User.objects.get(id=user),
        defaults={
            "points": points,
            "completionTime": time,
            "answer": answer,
        }
    )
    return mission_completed, created

def friend_request(sender, recipient):
    try:
        r = FriendRequest(sender = sender, recipient = recipient)
        r.save()
        return True
    except :
        return False

def undo_friend_request(sender, recipient):
    try:
        r = FriendRequest.objects.get(sender=sender, recipient=recipient)
        r.delete()
        return True
    except:
        return False

def accept_friend_request(sender, recipient):
    try:
        r = FriendRequest.objects.get(sender=sender, recipient=recipient)
        r.delete()
        return True
    except:
        return False

def get_friend_status(sender, recipient) -> int:
    NOT_FRIEND = 0
    SENT_REQUEST = 1
    RECIEVED_REQUEST = 2
    IS_FRIEND = 4
    try:
        try:
            FriendRequest.objects.get(sender=recipient, recipient=sender)
            return RECIEVED_REQUEST
        except:
            FriendRequest.objects.get(sender=sender, recipient=recipient)
            return SENT_REQUEST
    except:
        return NOT_FRIEND
