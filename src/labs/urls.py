from django.urls import path

from . import views

app_name = "labs"
urlpatterns = [
    path("<category>/", views.ChallengeView.as_view(), name="labs_by_category"),
    path("", views.SortByCategoryView.as_view(), name="category")
]
