from datetime import datetime, timedelta

from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.http import HttpResponseRedirect

from cfp.models import Call, Conference, Track, Talk, Profile, token
from cfp.forms import UserCreationForm, AuthenticationForm, parse_handle
from cfp.forms import TalkForm, ProfileForm

CONFERENCE_FIELDS = (
    'name',
    'start',
    'end',
    'website_url',
    'conduct_url',
    'tagline',
    'description',
    'twitter_handle',
    'twitter_hashtag',
    'venue_name',
    'venue_address',
    'programming_language',
    'city',
    'state',
    'country',
)

CALL_FIELDS = (
    'description',
    'start',
    'end',
    'notify',
    'application_url',
)


def legacy(r, year, slug):
    legacy = "{}-{}".format(year, slug)
    return redirect(get_object_or_404(Conference, legacy_slug=legacy),
                    permanent=True)


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())


class StaffRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return staff_member_required(super(StaffRequiredMixin, cls).as_view())


class ConferenceCreate(CreateView):
    model = Conference
    fields = CONFERENCE_FIELDS

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['name'])
        form.instance.twitter_hashtag = \
            form.cleaned_data['twitter_hashtag'].replace("#", "")
        form.instance.twitter_handle = \
            parse_handle(form.cleaned_data['twitter_handle'])
        return super(ConferenceCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('call_create',
                       args=[self.object.slug, self.object.start.year])


class ConferenceEdit(StaffRequiredMixin, UpdateView):
    model = Conference
    fields = CONFERENCE_FIELDS

    def get_success_url(self):
        return reverse('call_read',
                       args=[self.object.slug, self.object.start.year])

    def get_object(self, qs=None):
        if qs is None:
            qs = self.get_queryset()
        return get_object_or_404(qs, start__year=self.kwargs['year'],
                                     slug=self.kwargs['slug'])


class CallCreate(CreateView):
    model = Call
    fields = CALL_FIELDS

    def form_valid(self, form):
        conf = get_object_or_404(Conference, start__year=self.kwargs['year'],
                                 slug=self.kwargs['slug'])
        form.instance.conference = conf

        if form.instance.notify is None:
            form.instance.notify = form.instance.end + timedelta(days=7)

        return super(CallCreate, self).form_valid(form)


class ProfileEdit(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    success_url = "/profile"

    def get_object(self, queryset=None):
        profile = Profile.generate(self.request.user)
        if not profile.pk:
            profile.save()
        return profile


class CallEdit(StaffRequiredMixin, UpdateView):
    model = Call
    fields = CALL_FIELDS

    def form_valid(self, form):
        if form.instance.notify is None:
            form.instance.notify = form.instance.end + timedelta(days=7)
        return super(CallEdit, self).form_valid(form)

    def get_object(self, queryset=None):
        if qs is None:
            qs = self.get_queryset()
        return get_object_or_404(qs, conference__start__year=self.kwargs['year'],
                                     conference__slug=self.kwargs['slug'])


def call_detail_and_form(request, slug, year):
    call = get_object_or_404(Call, conference__start__year=year,
                                   conference__slug=slug)

    if request.method == 'POST' and not call.is_open():
        messages.error(request, "Talk submission is closed.")
        profile_form = ProfileForm()
        form = TalkForm()
    elif request.method == 'POST' and request.user.is_authenticated():
        form = TalkForm(request.POST)
        if form.is_valid():
            if not form.instance.audience:
                form.instance.audience = 1
            with transaction.atomic():
                profile = Profile.generate(request.user)
                profile.save()
                form.instance.token = token(15)
                form.instance.call = call
                form.instance.profile = profile
                form.save()
            messages.success(request, "Talk successfully submitted. High five!")
            return HttpResponseRedirect(call.get_absolute_url())

    elif request.method == 'POST':
        form = TalkForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            if not form.instance.audience:
                form.instance.audience = 1
            with transaction.atomic():
                form.instance.call = call
                form.instance.profile = profile_form.save()
                form.save()
            messages.success(request, "Talk successfully submitted. High five!")
            return HttpResponseRedirect(call.get_absolute_url())

    else:
        profile_form = ProfileForm()
        form = TalkForm()

    context = {'call': call}

    if request.user.is_authenticated():
        context['talks'] = Talk.objects.filter(call=call,
                                               profile__owner=request.user)

    if not request.user.is_authenticated():
        context['profile_form'] = profile_form

    form.fields['track'].queryset = \
        Track.objects.filter(conference=call.conference.id)

    if form.fields['track'].queryset.count() == 0:
        del form.fields['track']

    if not call.needs_audience:
        del form.fields['audience']

    context['form'] = form

    return render(request, 'cfp/call_detail.html', context)


class CallList(ListView):
    model = Call
    context_object_name = 'calls'

    def get_queryset(self):
        qs = super(CallList, self).get_queryset()
        qs = qs.filter(state='approved',
                       start__lte=datetime.utcnow(),
                       end__gte=datetime.utcnow())
        return qs.order_by('end')


class TalkDetail(LoginRequiredMixin, DetailView):
    model = Talk
    context_object_name = 'talk'

    def get_object(self):
        obj = super(TalkDetail, self).get_object()
        if not obj.profile.owner:
            raise PermissionDenied()
        if obj.profile.owner.id != self.request.user.id:
            raise PermissionDenied()
        return obj


class LatestCallsFeed(Feed):
    title = "Call to Speakers - Find Your Voice"
    link = "https://calltospeakers.com/feed"
    description = ("Start speaking at conferences today. Call to Speakers"
                   "helps you find conferences that are actively looking for"
                   "speakers")

    def items(self):
        return Call.objects.\
            filter(state='approved', start__lte=datetime.utcnow()).\
            order_by('-created')[:50]

    def item_title(self, item):
        return item.conference.name

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.created


class SignupView(FormView):
    template_name = 'registration/signup.html'
    form_class = UserCreationForm
    success_url = '/'

    def form_valid(self, form):
        u = form.save()
        user = authenticate(username=u.username,
                            password=form.cleaned_data['password1'])
        login(self.request, user)
        return super(SignupView, self).form_valid(form)


class LoginView(FormView):
    template_name = 'registration/login.html'
    form_class = AuthenticationForm
    success_url = '/'

    def form_valid(self, form):
        login(self.request, form.user_cache)
        return super(LoginView, self).form_valid(form)
