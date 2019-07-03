from django.urls import path

from . import views


app_name = "sec"
urlpatterns = [
    path("two_fa/", views.Two_fa.as_view(), name="two_fa")
]
