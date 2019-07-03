from django.urls import path

from . import views


app_name = "invite"
urlpatterns = [
    path('', views.InviteChallengeView.as_view(), name="invite_challenge"),
    path('generate/', views.send_b64, name='generate')
]
