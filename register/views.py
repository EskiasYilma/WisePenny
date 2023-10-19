from django.shortcuts import render, redirect
# Import a prebuilt login and registration forms
from django.contrib.auth.forms import PasswordChangeForm
from .forms import RegisterForm, EditProfileForm
from django.contrib import messages
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy


def register(response):
    if response.method == "POST":
        form = RegisterForm(response.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password1']
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(response, new_user)
            messages.success(
                response, f"Registeration Successful! Welcome to your Dashboard, Dear {new_user}")
            return redirect("/dashboard")
            # TODO: redirect to profile page
    else:
        form = RegisterForm()

    return render(response, "register/register.html", {"form": form})


@login_required(login_url='/login/')
def edit_profile(response):
    user_profile = User.objects.get(id=response.user.id)
    form = EditProfileForm(response.POST or None, instance=user_profile)
    if form.is_valid():
        form.save()
        username = form.cleaned_data['username'],
        email = form.cleaned_data['email']
        # update_user = authenticate(username=form.cleaned_data['username'],
        #                         password=form.cleaned_data['password1'],
        #                         )
        # login(response, new_user)
        messages.success(
            response, f"Update Successful!")
        return redirect("/dashboard")
        # TODO: redirect to profile page

    return render(response, "registration/edit_profile.html", {"form": form})


class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_changed')


def password_changed(response):
    messages.success(
        response, f"Password Changed Successfully!")
    return render(response, 'registration/password_changed.html')
