from django.urls import path
from . import views  # ✅ Ensure this matches 'views.py' in 'myapp'

urlpatterns = [
    path('', views.home, name='home'),  # ✅ Ensure 'home' exists in 'views.py'
]
