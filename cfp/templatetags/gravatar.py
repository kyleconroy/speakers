import hashlib
import urllib.parse

from django import template


register = template.Library()


@register.filter
def gravatarize(value):
    h = hashlib.md5(value.lower().encode('utf-8')).hexdigest()
    gravatar_url = "https://www.gravatar.com/avatar/" + h + "?"
    return gravatar_url + urllib.parse.urlencode({
        'd': 'avatar@calltospeakers.com',
        's': 50,
    })
