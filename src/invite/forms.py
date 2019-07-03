from django import forms


class InviteChallengeForm(forms.Form):
    invite_code = forms.CharField(widget=forms.TextInput(
        attrs={
            "id": "codeInput",
            "class": "form-control shadow-none rounded-0",
            "placeholder": "Invite Code"
        }
    )) 