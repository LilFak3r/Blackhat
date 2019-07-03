from django.shortcuts import render
from django.views.generic import View

from accounts.models import User
from labs.models import Challenge


class HomeView(View):
    def get(self, request):
        users = User.objects.all().count
        challenges = Challenge.objects.all().count
        context = {
            'users': users,
            'challenges': challenges
        }
        return render(request, 'base/index.html', context)
