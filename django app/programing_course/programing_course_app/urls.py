from django.urls import path

from . import views

app_name = "programing_course_app"
urlpatterns = [
    path("",views.index, name="index"),
    ]