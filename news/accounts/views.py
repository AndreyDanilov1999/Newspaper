from django.contrib.auth.models import User
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from .forms import SignUpForm


class SignUp(CreateView):
    model = User
    form_class = SignUpForm
    success_url = '/accounts/login'

    template_name = 'registration/signup.html'


class Profile(ListView):
    model = User
    template_name = 'Users/profile.html'
    context_object_name = 'profile'


