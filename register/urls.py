from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import PasswordsChangeView

urlpatterns = [
    path("register/", views.register, name="register"),
    path('change-password/', PasswordsChangeView.as_view(template_name="change_password.html"),
         name='password_change'),
    path('password_changed', views.password_changed, name="password_changed"),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"),
         name='password_reset_complete'),
    path("edit_profile/", views.edit_profile, name="edit_profile"),

]
