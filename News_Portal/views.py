from django.contrib.auth import LoginView

class LogIn (LoginView):
    template_name = 'registration/login.html'