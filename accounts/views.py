from django.contrib.auth.models import User
from django.views.generic.edit import CreateView
#from django.views.generic import RedirectView
from .forms import SignUpForm


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'

    template_name = 'registration/signup.html'

'''class LogOut(RedirectView):
    model = User
    success_url = '/posts'''''