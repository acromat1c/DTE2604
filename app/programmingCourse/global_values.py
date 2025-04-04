from .models_io import *

def global_variables(request):
    if request.user.is_authenticated:
        userTheme = get_user_theme(request.user)
    else:
        userTheme = None
    return {
        "userTheme": userTheme,
        }