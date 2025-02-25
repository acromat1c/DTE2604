from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to MyApp Home Page!")  # ✅ Simple response for testing
