from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.urls import reverse_lazy
from django.views.generic import UpdateView

from .forms import SignupForm


# Create your views here.
def signup(request):
    form = SignupForm
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user=user)
            return redirect('home')

    return render(request, 'accounts/signup.html', {'form': form})


class UserUpdateView(UpdateView):
    model = User
    template_name = 'accounts/my_account.html'
    fields = ('first_name', 'last_name', 'username', 'email')
    success_url = reverse_lazy('my_account')

    def get_object(self):
        return self.request.user

