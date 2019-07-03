import pyotp

from django.shortcuts import render, redirect, reverse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import AuthKey


class Two_fa(LoginRequiredMixin, View):
    def get(self, request):
        meth = "GET"
        auth_key = pyotp.random_base32()
        QR = f'https://chart.googleapis.com/chart?chs=200x200&chld=M|0&cht=qr&chl= \
            {pyotp.totp.TOTP(auth_key).provisioning_uri(self.request.user.username, issuer_name="Blackhat")}'
        context = {"meth": meth, "KEY": auth_key, "QR": QR}
        return render(request, "sec/two_fa.html", context)

    def post(self, request):
        user = self.request.user
        NewKey = AuthKey()
        NewKey.user = user
        NewKey.auth_key = request.POST.get("key")
        NewKey.enabled = True
        NewKey.save()
        return redirect(reverse("accounts:profile", kwargs={"pk": user.id}))