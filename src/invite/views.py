from random import choice

from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.views import View

from .forms import InviteChallengeForm


class InviteChallengeView(View):
    B64_ENC = ['UnlkOW1FV0hKQw==', 'SHZRRnRFblRLUQ==', 'Q2Q1eFB6VzlXMg==', 'eTNoOXZZUWpQSw==', 'WUNHMkNpRENjbg==',
    'ZGVmUzMyTDB0MA==', 'bExaR1Rrd3EwZA==', 'UmNYYjBOa2EzdA==', 'Y0dOVGVtT3lMeA==', 'TGgxRFF6R2VMaQ==']
    B64_DEC = ['Ryd9mEWHJC', 'HvQFtEnTKQ', 'Cd5xPzW9W2', 'y3h9vYQjPK', 'YCG2CiDCcn',
    'defS32L0t0', 'lLZGTkwq0d', 'RcXb0Nka3t', 'cGNTemOyLx', 'Lh1DQzGeLi']

    def get(self, request):
        form = InviteChallengeForm
        return render(request, 'invite/challenge.html', {'form': form})
        
    def post(self, request):
        form = InviteChallengeForm(request.POST)
        if form.is_valid():
            code = form.cleaned_data.get('invite_code')
            if self.check_code(code):
                return redirect('accounts:sign_up')
            else:
                form.add_error("invite_code", "Invalid Invite Code. Try again")
                return render(request, 'invite/challenge.html', {'form': form})

    def check_code(self, code):
        if code in self.B64_DEC:
            return True


@csrf_exempt
def send_b64(request):
    if request.method == 'POST':
        r = choice(InviteChallengeView.B64_ENC)
        return JsonResponse({'code': r, 'format': 'encoded'})
    return HttpResponseNotAllowed(['POST'])