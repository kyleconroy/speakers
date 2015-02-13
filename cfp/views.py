from datetime import datetime, timedelta

from django.contrib.auth import authenticate, login
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.text import slugify

from cfp.models import Call, Conference, Track, Talk, Profile
from cfp.forms import UserCreationForm, AuthenticationForm, TalkForm

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


class StaffRequiredMixin(object):

    @classmethod
    def as_view(cls):
        return staff_member_required(super(StaffRequiredMixin, cls).as_view())


class ConferenceCreate(CreateView):
    model = Conference
    fields = CONFERENCE_FIELDS

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['name'])
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


class CallDetail(DetailView):
    model = Call
    context_object_name = 'call'

    def get_context_data(self, **kwargs):
        context = super(CallDetail, self).get_context_data(**kwargs)

        qs = Track.objects.filter(conference=self.object.conference.id)

        form = TalkForm()
        form.fields['track'].queryset = qs

        if qs.count() == 0:
            del form.fields['track']

        if not self.object.needs_audience:
            del form.fields['audience']

        if self.request.user.is_authenticated():
            del form.fields['email_address']
            del form.fields['first_name']
            del form.fields['last_name']

        context['form'] = form
        return context

    def get_object(self, qs=None):
        if qs is None:
            qs = self.get_queryset()
        return get_object_or_404(qs, conference__start__year=self.kwargs['year'],
                                     conference__slug=self.kwargs['slug'])


class TalkCreate(FormView):
    template_name = 'cfp/talk_form.html'
    form_class = TalkForm
    success_url = '/'

    def form_valid(self, form):
        call = get_object_or_404(Call, conference__start__year=self.kwargs['year'],
                                       conference__slug=self.kwargs['slug'])

        if self.request.user.is_authenticated():
            profile = Profile.objects.get_or_create(user=self.request.user)
        else:
            profile = Profile()
            profile.user = self.request.user
            profile.first_name = form.cleaned_data['first_name']
            profile.last_name = form.cleaned_data['last_name']
            profile.email_address = form.cleaned_data['email_address']
            profile.save()

        form.instance.call = call
        form.instance.profile = profile

        if not form.instance.audience:
            form.instance.audience = 1

        form.save()
        return super(TalkCreate, self).form_valid(form)


class CallList(ListView):
    model = Call
    context_object_name = 'calls'

    def get_queryset(self):
        qs = super(CallList, self).get_queryset()
        qs = qs.filter(state='approved',
                       start__lte=datetime.utcnow(),
                       end__gte=datetime.utcnow())
        return qs.order_by('end')


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
