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