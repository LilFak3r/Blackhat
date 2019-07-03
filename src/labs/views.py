from django.shortcuts import render, HttpResponse
from django.views.generic import View, ListView
from django.core.exceptions import ObjectDoesNotExist

from accounts.models import User
from .models import Challenge
from .forms import ChallengePostForm


class ChallengeView(View):
    def get(self, request, category):
        form = ChallengePostForm
        challeges = Challenge.objects.filter(category=category)
        return render(request, 'labs/home.html', {'form': form, 'challenges': challeges})

    def post(self, request, category):
        form = ChallengePostForm(request.POST)
        if form.is_valid():
            flag = form.cleaned_data.get('flag')
            ch_id = int(form.cleaned_data.get('challenge_id'))
            user = self.request.user
            challeges = Challenge.objects.all()
            try:
                challenge = Challenge.objects.get(id=ch_id)
            except Challenge.ObjectDoesNotExist:
                form.add_error(
                    None, "Challenge does not exist")
                return render(request, 'labs/home.html', {'form': form, 'challenges': challeges})

            if challenge.check_flag(flag, user):
                return render(request, 'base/mess.html', {'mess': 'Challenge solved'})
            else:
                form.add_error(
                    None, "Incorrect flag")
                return render(request, 'labs/home.html', {'form': form, 'challenges': challeges})


class SortByCategoryView(View):
    def get(self, request):
        context = {
            'GS': Challenge.objects.filter(category='GS').count,
            'CR': Challenge.objects.filter(category='CR').count,
            'ST': Challenge.objects.filter(category='ST').count,
            'BE': Challenge.objects.filter(category='BE').count,
            'WE': Challenge.objects.filter(category='WE').count,
            'FR': Challenge.objects.filter(category='FR').count,
            'RV': Challenge.objects.filter(category='RV').count
        }
        return render(request, 'labs/category.html', context)
