from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

from cfp.models import Talk


def parse_handle(handle):
    for r in ["http://", "https://", "www.twitter.com/", "twitter.com/", "@"]:
        handle = handle.replace(r, "")
    return handle


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """
    password1 = forms.CharField(label="Password", min_length=8,
        widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email",)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = user.email
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class AuthenticationForm(forms.Form):
    email = forms.CharField(max_length=254)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': ("Please enter a correct email address and password. "
                          "Note that both fields may be case-sensitive."),
        'inactive': "This account is inactive.",
    }

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            self.user_cache = authenticate(username=email, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            elif not self.user_cache.is_active:
                raise forms.ValidationError(
                    self.error_messages['inactive'],
                    code='inactive',
                )
        return self.cleaned_data


class TalkForm(forms.ModelForm):
    first_name = forms.CharField(max_length=300)
    last_name = forms.CharField(max_length=300)
    email_address = forms.EmailField(max_length=254)

    class Meta:
        model = Talk
        fields = ('title', 'abstract', 'track', 'audience')
