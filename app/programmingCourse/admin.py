from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Friend)
admin.site.register(FriendRequest)
admin.site.register(Group)
admin.site.register(GroupMember)
admin.site.register(GroupMessage)
admin.site.register(Course)
admin.site.register(Module)
admin.site.register(Mission)
admin.site.register(MissionCompleted)
admin.site.register(Achievement)
admin.site.register(UserAchievement)
admin.site.register(Profile)
