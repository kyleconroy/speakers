from datetime import datetime

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
