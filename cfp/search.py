import re
import itertools

from cfp.models import Call, Conference


def tokenize_query(search):
    groups = re.findall('([\'"].*?[\'"])|([\w:]+)', search)
    return [x.replace("'", "").replace('"', "").strip() for x
            in list(itertools.chain(*groups)) if x]


def sanitize_query(search):
    search = search.strip()
    search = re.sub('[\?\|!\*]', '', search)
    tokens = tokenize_query(search)
    return '&'.join(["'{}'".format(x) for x in tokens if ':' not in x])


def filters(search):
    search = search.strip()
    search = re.sub('[\?\|!\*]', '', search)
    return [t.split(':') for t in tokenize_query(search) if ':' in t]


def results(queryset=None, q='', location='', topic=''):
    qs = queryset
    if qs is None:
        qs = Call.open_and_approved()

    q = sanitize_query(q)
    if q:
        sql = "cfp_conference.fts_document @@ to_tsquery('simple', %s)"
        ids = Conference.objects.values_list('id', flat=True).extra(
            where=[sql], params=[q],
        )
        qs = qs.filter(conference__in=set(ids))

    if location:
        qs = qs.filter(conference__country=location.upper())

    if topic:
        qs = qs.filter(conference__topics__value=topic.lower())

    return qs
