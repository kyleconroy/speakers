import markdown2
import requests

from django import forms
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.forms.widgets import Select

from cfp.models import Profile


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


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('owner',)
        labels = {
            'twitter_handle': 'Twitter',
            'github_handle': 'GitHub',
            'linkedin': 'LinkedIn',
        }


class ReadOnlyForm(forms.ModelForm):
    """Base class for making a form readonly."""
    def __init__(self, *args, **kwargs):
        super(ReadOnlyForm, self).__init__(*args, **kwargs)
        for f in self.fields:
            self.fields[f].label = self.fields[f].label
            if isinstance(self.fields[f].widget, Select):
                self.fields[f].widget.attrs['disabled'] = 'disabled'
            else:
                self.fields[f].widget.attrs['readonly'] = 'readonly'


class EmailSubmissionForm(forms.Form):
    conference_email = forms.EmailField()
    presenter_name = forms.CharField()
    presenter_email = forms.EmailField()
    subject = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        resp = requests.post(
            "https://api.mailgun.net/v2/calltospeakers.com/messages",
            auth=("api", settings.MAILGUN_KEY),
            data={
                "from": "{} <robot@calltospeakers.com>".format(
                    self.cleaned_data['presenter_name']),
                "to": [self.cleaned_data['conference_email']],
                "subject": self.cleaned_data['subject'],
                "text": self.cleaned_data['body'],
                "html": markdown2.markdown(self.cleaned_data['body']),
                "h:Reply-To": self.cleaned_data['presenter_email'],
            })
        resp.raise_for_status()


class SearchForm(forms.Form):
    q = forms.CharField(max_length=254, required=False, label='')
    location = forms.ChoiceField(choices=(
        ('', 'Any'),
    ), required=False, label='')
    topic = forms.ChoiceField(choices=(
        ('', 'Any'),
    ), required=False, label='')
    sort = forms.ChoiceField(choices=(
        ('closing', 'By closing'),
        ('newest', 'By newest'),
    ), required=False, label='')


class SavedSearchForm(forms.Form):
    q = forms.CharField(max_length=254, required=False)
    location = forms.CharField(max_length=100, required=False)
    topic = forms.CharField(max_length=100, required=False)

    def clean(self):
        cd = super(SavedSearchForm, self).clean()
        if not any([cd.get("q"), cd.get("location"), cd.get("topic")]):
            raise forms.ValidationError("Query, location, or topic required")
        return cd
