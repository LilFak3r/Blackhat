from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    ReadOnlyPasswordHashField,
)

User = get_user_model()


class ChallengePostForm(forms.Form):
    flag = forms.CharField(
        max_length=40,
        widget=forms.TextInput(
            attrs={
                "id": "flagInput",
                "class": "form-control shadow-none rounded-0",
            }
        )
    )
    challenge_id = forms.CharField(
        max_length=40,
        widget=forms.HiddenInput(
            attrs={
                "id": "ch_id",
                "class": "form-control shadow-none rounded-0",
            }
        ),
        required=False
    )
