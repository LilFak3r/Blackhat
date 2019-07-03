import requests
import pyotp
import json

from django.shortcuts import render, redirect, reverse, HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth import login, authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView as inV, LogoutView as outV
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import View, DetailView, UpdateView, ListView
from django.utils.html import mark_safe, escapejs

from django.conf import settings

from .forms import SignupForm, LoginForm, SearchForm
from .models import User, UserProfile
from .email_token import account_activation_token
from sec.models import AuthKey

# email import
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, send_mail
from django.template import loader


class SignupView(View):
    def get(self, request):
        form = SignupForm
        return render(request, "accounts/sign_up.html", {"form": form})

    def post(self, request):
        form = SignupForm(request.POST)
        if form.is_valid():

            # start reCAPTCHA validation
            recaptcha_response = request.POST.get("g-recaptcha-response")
            data = {
                "secret": settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                "response": recaptcha_response,
            }
            r = requests.post(
                "https://www.google.com/recaptcha/api/siteverify", data=data
            )
            result = r.json()

            if result["success"]:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                mail_subject = "Activate your account."
                message = render_to_string(
                    "accounts/activate_email.html",
                    {
                        "user": user,
                        "domain": current_site.domain,
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "token": account_activation_token.make_token(user),
                    },
                )
                to_email = form.cleaned_data.get("email")
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()
                post_mess = (
                    "Please confirm your email address to complete the registration."
                )
                post_mess2 = "You can now close this tab."
                return render(
                    request, "base/mess.html", {"mess": post_mess,
                                                "mess2": post_mess2}
                )

            else:
                return render(request, 'accounts/sign_up.html', {'form': form})
        else:
            return render(request, 'accounts/sign_up.html', {'form': form})

    def activate(request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return redirect("sec:two_fa")
        else:
            return HttpResponse("Activation link is invalid!")


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "accounts/log_in.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            provided_auth_key = form.cleaned_data.get("two_fa")
            user = authenticate(username=username, password=password)
            if user is not None:
                if hasattr(user, "two_fa"):
                    totp = pyotp.TOTP(user.two_fa.auth_key)
                    user_auth_key = totp.now()
                    if user_auth_key == provided_auth_key:
                        login(request, user)
                        return redirect("home")
                    else:
                        form.add_error("two_fa", "Invalid 2FA Code")
                        return render(request, "accounts/log_in.html", {'form': form})
                else:
                    form.add_error(
                        None, "You should enable 2FA first. Press \"Reset 2FA Code\" button below")
                    return render(request, "accounts/log_in.html", {'form': form})
            else:
                form.add_error(
                    None, "Invalid login credentials / user doesn't exist")
                return render(request, "accounts/log_in.html", {'form': form})
        else:
            form.add_error(None, "Invalid login credentials")
            return render(request, "accounts/log_in.html", {'form': form})


class LogoutView(outV):
    pass


class ProfileView(DetailView):
    model = User
    template_name = "accounts/profile.html"

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.id)
        else:
            return User.objects.none()


class EditProfile(UpdateView):
    model = User
    fields = ['username', 'email', 'country']
    template_name_suffix = '_update_form'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return User.objects.filter(pk=self.request.user.id)
        else:
            return User.objects.none()

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'pk': self.request.user.id})


class Users_Details(View):
    def get(self, request):
        meth = 'GET'
        form = SearchForm
        return render(request, 'accounts/users_details.html', {'form': form, 'meth': meth})

    def post(self, request):
        meth = 'POST'
        form = SearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            country = form.cleaned_data.get('country')

            if username:
                if country:
                    r = User.objects.filter(
                        username__contains=username, country=country)
                else:
                    r = User.objects.filter(username__contains=username)
            else:
                if country:
                    r = User.objects.filter(country=country)
                else:
                    form.add_error(
                        'username', 'Enter username or choose country')
                    return render(request, 'accounts/users_details.html', {'meth': meth, 'form': form})

            return render(request, 'accounts/users_details.html', {'res': r, 'pattern_u': username, 'pattern_c': country, 'meth': meth, 'form': form})


class Rankings(View):
    def hof(request):
        queryset = UserProfile.objects.order_by('-points')[:100]
        return render(request, 'rankings/hof.html', {'data': queryset})


class Map(View):
    def get(self, request):
        countries = self.get_countries_dict()
        countries = json.dumps(countries)
        return render(request, 'accounts/map.html', {'data': mark_safe(escapejs(countries))})

    def get_countries_dict(self):
        users = User.objects.all()
        countries = {}

        for user in users:
            country = user.country
            if country not in countries.keys():
                countries[country] = 1
            else:
                countries[country] += 1
        return countries
