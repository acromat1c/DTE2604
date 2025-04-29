from django.urls import path

from . import views

app_name = "programing_course_app"
urlpatterns = [
    path("index",views.index, name="index"),
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
    path("friends",views.friendList, name="friendList"),
    path("friends/search",views.friend_search, name="friend_search"),
    path("addfriend/<str:username>",views.add_friend, name="addfriend"),
    path("overview",views.overview, name="overview"),
    path("overview/<str:nameCourse>",views.course, name="course"),
    path("overview/<str:nameCourse>/<str:nameModule>",views.module, name="module"),
    path("overview/<str:nameCourse>/<str:nameModule>/<str:nameMission>",views.mission, name="mission"),
    path("test",views.test, name="test"),
    path("shop",views.shop, name="shop"),
    path("inventory",views.inventory, name="inventory"),
    path("gatcha",views.gatcha, name="gatcha"),
    ]
