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
    path("overview",views.overview, name="overview"),
    path("overview/<str:nameCourse>",views.course, name="course"),
    path("overview/<str:nameCourse>/<str:nameModule>",views.module, name="module"),
    path("overview/<str:nameCourse>/<str:nameModule>/<str:nameMission>",views.mission, name="mission"),
    path("test",views.test, name="test"),
    ]