from django.urls import path
from django.contrib import admin


from . import views

app_name = "programing_course_app"
urlpatterns = [
    path("",views.main, name="main"),
    path("login",views.login, name="login"),
    path("signup",views.signup, name="signup"),
    path("logout",views.logout, name="logout"),
    path("user/settings",views.userSettings, name="userSettings"),
    path("user/<str:username>/", views.user, name="user"),
    path("groups/create/", views.create_group, name="create_group"),
    path("groups/<str:name>/settings", views.group_settings, name="group_settings"),
    path("groups/<str:name>", views.group, name="group"), 
    path("groups", views.groupList, name="groupList"), 
    path("groups/<str:name>/requests", views.manage_group_requests, name="manage_group_requests"),
    path("friends",views.friend_list, name="friendList"),
    path("friends/search",views.friend_search, name="friend_search"),
    path("friends/requests",views.friend_requests, name="friend_requests"),
    path("addfriend/<str:username>",views.add_friend, name="addfriend"),
    path("courses",views.courses, name="courses"),
    path("courses/<str:nameCourse>",views.course, name="course"),
    path("courses/<str:nameCourse>/<str:nameModule>",views.module, name="module"),
    path("courses/<str:nameCourse>/<str:nameModule>/<str:nameMission>",views.mission, name="mission"),
    path("shop",views.shop, name="shop"),
    path("inventory",views.inventory, name="inventory"),
    path("gacha",views.gatcha, name="gacha"),
    ]
