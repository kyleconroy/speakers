from datetime import datetime, timedelta

from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.forms.models import modelform_factory
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect, render
from django.utils.text import slugify
from django.http import HttpResponseRedirect

from django_countries import countries

from cfp.models import Call, Conference, Talk, Profile, token, SavedSearch
from cfp.models import Topic, Interest
from formbuilder.models import Form
from cfp.forms import UserCreationForm, AuthenticationForm, parse_handle
from cfp.forms import ProfileForm, ReadOnlyForm, EmailSubmissionForm
from cfp.forms import SearchForm, SavedSearchForm, SuggestionForm
from cfp import search

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


class SubmissionDetail(StaffRequiredMixin, DetailView):
    model = Talk
    template_name = 'cfp/submission_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SubmissionDetail, self).get_context_data(**kwargs)
        prof = modelform_factory(Profile, form=ReadOnlyForm, exclude=('id',))
        call = modelform_factory(Call, form=ReadOnlyForm, exclude=('id',))
        context['profile'] = self.object.profile
        context['profform'] = prof(instance=self.object.profile)
        context['callform'] = call(instance=self.object.call)
        return context


class SubmissionList(StaffRequiredMixin, ListView):
    model = Talk
    template_name = 'cfp/submission_list.html'

    def get_queryset(self):
        qs = super(SubmissionList, self).get_queryset()
        return qs.filter(state='new')


class SubmissionEmail(StaffRequiredMixin, FormView):
    form_class = EmailSubmissionForm
    template_name = 'cfp/submission_email.html'
    success_url = '/submissions'

    def form_valid(self, form):
        form.send_email()
        return super(SubmissionEmail, self).form_valid(form)


class SuggestionCreate(FormView):
    form_class = SuggestionForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        messages.success(self.request,
                         ('Thanks for the suggestion, it should appear '
                          'on the site in a day or two'))
        return super(SuggestionCreate, self).form_valid(form)


class BetaSignup(CreateView):
    model = Interest
    success_url = '/hosted'
    fields = ('email',)

    def form_valid(self, form):
        messages.success(self.request,
                         ('Thanks for your interest! Expect an email '
                          'from us very soon!'))
        return super(BetaSignup, self).form_valid(form)


class CallCreate(CreateView):
    model = Call
    fields = CALL_FIELDS

    def form_valid(self, form):
        year = self.kwargs['year']
        conf = get_object_or_404(Conference, start__year=year,
                                 slug=self.kwargs['slug'])

        f = Form(name="{} {} CFP".format(conf.name, year))
        f.save()

        form.instance.conference = conf
        form.instance.form = f

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

    def get_context_data(self, **kwargs):
        context = super(ProfileEdit, self).get_context_data(**kwargs)
        context['selected'] = 'profile'
        return context


class CallEdit(StaffRequiredMixin, UpdateView):
    model = Call
    fields = CALL_FIELDS

    def form_valid(self, form):
        if form.instance.notify is None:
            form.instance.notify = form.instance.end + timedelta(days=7)
        return super(CallEdit, self).form_valid(form)

    def get_object(self, qs=None):
        if qs is None:
            qs = self.get_queryset()
        return get_object_or_404(
            qs, conference__start__year=self.kwargs['year'],
            conference__slug=self.kwargs['slug'])


def call_detail_and_form(request, slug, year):
    call = get_object_or_404(Call, conference__start__year=year,
                             conference__slug=slug)
    context = {'call': call}

    if request.user.is_authenticated():
        context['tracking'] = request.user.conference_set.\
            filter(id=call.conference.id).exists()

    if call.form is None or not call.hosted:
        return render(request, 'cfp/call_detail.html', context)

    form_class = call.form.form_class()

    if request.method == 'POST' and not call.is_open():
        messages.error(request, "Talk submission is closed.")
        profile_form = ProfileForm()
        cfp_form = form_class()
    elif request.method == 'POST' and request.user.is_authenticated():
        cfp_form = form_class(request.POST)
        if cfp_form.is_valid():
            with transaction.atomic():
                profile = Profile.generate(request.user)
                profile.save()
                sub = call.form.submit(cfp_form)
                talk = Talk(call=call, profile=profile, submission=sub,
                            token=token(15),
                            title=cfp_form.cleaned_data['title'])
                talk.save()
            messages.success(request, "Talk successfully submitted. You rock!")
            return HttpResponseRedirect(call.get_absolute_url())

    elif request.method == 'POST':
        cfp_form = form_class(request.POST)
        profile_form = ProfileForm(request.POST)
        if cfp_form.is_valid() and profile_form.is_valid():
            with transaction.atomic():
                profile = profile_form.save()
                sub = call.form.submit(cfp_form)
                talk = Talk(call=call, profile=profile, submission=sub,
                            token=token(15),
                            title=cfp_form.cleaned_data['title'])
                talk.save()

            messages.success(request, "Talk successfully submitted. You rock!")
            return HttpResponseRedirect(call.get_absolute_url())

    else:
        profile_form = ProfileForm()
        cfp_form = form_class()

    context = {'call': call}

    if request.user.is_authenticated():
        context['talks'] = Talk.objects.filter(call=call,
                                               profile__owner=request.user)

    if not request.user.is_authenticated():
        context['profile_form'] = profile_form

    context['form'] = cfp_form

    return render(request, 'cfp/call_detail.html', context)


@login_required
def track_conference(request, slug, year):
    conf = get_object_or_404(Conference, slug=slug, start__year=year)

    if not request.user.conference_set.filter(id=conf.id).exists():
        conf.watchers.add(request.user)

    return HttpResponseRedirect(conf.get_absolute_url())


@login_required
def save_search(request):
    if not request.method == 'POST':
        return HttpResponseRedirect('/')

    form = SavedSearchForm(request.POST)
    if form.is_valid():
        topic = Topic.objects.filter(value=form.cleaned_data['topic']).first()
        ss, created = SavedSearch.objects.get_or_create(
            owner=request.user,
            q=form.cleaned_data['q'],
            country=form.cleaned_data['location'].upper(),
            topic=topic,
        )
        if created:
            messages.success(
                request,
                "Search successfully saved. Your future self thanks you.")

        return HttpResponseRedirect(ss.get_absolute_url())
    return HttpResponseRedirect('/')


class CallList(ListView):
    model = Call
    context_object_name = 'calls'

    def get_queryset(self):
        self.saved_search = None
        qs = super(CallList, self).get_queryset()
        qs = Call.open_and_approved(queryset=qs)

        # TODO: Cache these values
        locations = [('', 'Any country')]
        for c in sorted(set(qs.values_list('conference__country', flat=True))):
            locations.append((c.lower(), dict(countries)[c]))

        topics = Topic.objects.values_list('value', 'name')
        topics = sorted(((k, v) for k, v in topics if k is not None),
                        key=lambda x: x[1].lower())
        topics.insert(0, ('', 'Any topic'))

        self.search = SearchForm(self.request.GET)
        self.search.fields['location'].choices = locations
        self.search.fields['topic'].choices = topics

        if not self.search.is_valid():
            return qs.order_by('end')

        location = self.search.cleaned_data['location']
        sort = self.search.cleaned_data['sort']
        topic = self.search.cleaned_data['topic']
        q = self.search.cleaned_data['q']
        found_topic = Topic.objects.filter(value=topic).first()

        qs = search.results(queryset=qs, q=q, location=location, topic=topic)

        if self.request.user.is_authenticated():
            self.saved_search = SavedSearch.objects.filter(
                owner=self.request.user,
                q=q,
                country=location.upper(),
                topic=found_topic,
            ).first()

        if self.saved_search is None:
            self.saved_search = SavedSearch(
                q=q,
                country=location.upper(),
                topic=found_topic,
            )

        if sort == 'newest':
            return qs.order_by('-created')
        else:
            return qs.order_by('end')

    def get_context_data(self, **kwargs):
        context = super(CallList, self).get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q') or ""
        context['search'] = self.search
        context['saved_search'] = self.saved_search
        context['suggestion_box'] = SuggestionForm()
        return context


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

    def get_context_data(self, **kwargs):
        context = super(TalkDetail, self).get_context_data(**kwargs)
        context['selected'] = 'submitted'
        return context


class TalkList(ListView):
    model = Talk
    context_object_name = 'talks'

    def get_queryset(self):
        qs = super(TalkList, self).get_queryset()
        return qs.filter(profile__owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(TalkList, self).get_context_data(**kwargs)
        context['selected'] = 'submitted'
        return context


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


class TrackedConferenceList(LoginRequiredMixin, ListView):
    template_name = 'cfp/tracked_list.html'
    model = Conference
    context_object_name = 'confs'

    def get_queryset(self):
        qs = super(TrackedConferenceList, self).get_queryset()
        return qs.filter(watchers=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(TrackedConferenceList, self).get_context_data(**kwargs)
        context['selected'] = 'tracking'
        return context


class SavedSearchList(LoginRequiredMixin, ListView):
    template_name = 'cfp/search_list.html'
    model = SavedSearch
    context_object_name = 'searches'

    def get_queryset(self):
        qs = super(SavedSearchList, self).get_queryset()
        return qs.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(SavedSearchList, self).get_context_data(**kwargs)
        context['selected'] = 'searches'
        return context
