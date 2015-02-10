from datetime import datetime, timedelta

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils.text import slugify

from cfp.models import Call
from cfp.models import Conference

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

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(start__year=self.kwargs['year'],
                                   slug=self.kwargs['slug'])
        return queryset.get()


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
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(conference__start__year=self.kwargs['year'],
                                   conference__slug=self.kwargs['slug'])
        return queryset[0]


class CallDetail(DetailView):
    model = Call
    context_object_name = 'call'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(conference__start__year=self.kwargs['year'],
                                   conference__slug=self.kwargs['slug'])
        return queryset[0]


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
