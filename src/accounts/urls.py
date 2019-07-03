from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "accounts"
urlpatterns = [
    path("sign_up/", views.SignupView.as_view(), name="sign_up"),
    path(
        "activate/<str:uidb64>/<str:token>/", views.SignupView.activate, name="activate"
    ),
    path("log_in/", views.LoginView.as_view(), name="log_in"),
    path("log_out/", views.LogoutView.as_view(), name="log_out"),
    path("profile/<int:pk>", views.ProfileView.as_view(), name="profile"),
    path("profile/<int:pk>/edit", views.EditProfile.as_view(), name="edit_profile"),
    path("users_details/", views.Users_Details.as_view(), name="users_details"),
    path("hof/", views.Rankings.hof, name="hof"),
    path("map/", views.Map.as_view(), name="map")
]
