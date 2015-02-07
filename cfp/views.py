from datetime import datetime

from django.contrib.syndication.views import Feed
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.utils.text import slugify

from cfp.models import Call
from cfp.models import Conference


class ConferenceCreate(CreateView):
    model = Conference
    fields = [
        'name',
        'start',
        'end',
        'website_url',
        'conduct_url',
        'tagline',
        'description',
        'twitter_handle',
        'twitter_hashtag',
        'venue',
        'city',
        'state',
        'country',
    ]

    def form_valid(self, form):
        form.instance.slug = slugify(form.cleaned_data['name'])
        return super(ConferenceCreate, self).form_valid(form)


class CallDetail(DetailView):
    model = Call
    context_object_name = 'call'

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
        queryset = queryset.filter(conference__start__year=self.kwargs['year'],
                                   conference__slug=self.kwargs['slug'])
        return queryset.get()


class CallList(ListView):
    model = Call
    context_object_name = 'calls'

    def get_queryset(self):
        qs = super(CallList, self).get_queryset()
        qs = qs.filter(approved=True,
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
        qs = Call.objects.filter(approved=True, start__gte=datetime.utcnow())
        return qs.order_by('-created')[:50]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_pubdate(self, item):
        return item.created
