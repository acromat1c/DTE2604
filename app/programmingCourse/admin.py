from django.contrib import admin
from .models import *


class MissionAdmin(admin.ModelAdmin):
    fields = (
        'type', 'name', 'description', 'text', 'answer',
        'choices', 'evaluation_pattern', 'maxPoints',
        'module', 'reward'
    )

    class Media:
        js = ['programmingCourse/admin/mission_dynamic.js']


# Register your models here.
admin.site.register(Friend)
admin.site.register(FriendRequest)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(GroupMessage)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Mission, MissionAdmin)
admin.site.register(MissionCompleted)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
admin.site.register(Profile)
admin.site.register(UserBalance)
admin.site.register(Item)
admin.site.register(UserInventory)
