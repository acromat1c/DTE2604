from django.urls import path

from . import views

app_name = "programing_course_app"
urlpatterns = [
    path("index",views.index, name="index"),
    path("",views.main, name="main"),
    path("login",views.login, name="login"),
    path("signup",views.signup, name="signup"),
    path("logout",views.logout, name="logout"),
    path("user",views.user, name="user"),
    path("user/settings",views.userSettings, name="userSettings"),
    path("groups",views.groupList, name="groupList"),
    path("groups/<str:name>",views.group, name="group"),
    path("friends/<str:name>",views.friend, name="friend"),
    path("friends",views.friendList, name="friendList"),
    path("subjects",views.subjectList, name="subjectList"),
    path("subjects/<str:namesub>",views.subject, name="subject"),
    path("subjects/<str:namesub>/<str:name>",views.mission, name="mission"),
    path("test",views.test, name="test"),
    ]