from django.db import transaction
from bs4 import BeautifulSoup

from formbuilder.models import Form, Field


def create(**kwargs):
    print(kwargs)


@transaction.atomic
def parse_google_form(html):
    soup = BeautifulSoup(html)

    form = Form(name=soup.find("h1").text)
    form.save()

    for i, question in enumerate(soup.select("div.ss-form-entry")):
        label = ''
        name = ''
        help_text = ''
        kind = Field.CHAR
        widget = 0

        match = question.select('label.ss-q-item-label')
        if match:
            name = match[0]['for']
        else:
            continue

        match = question.select('div.ss-q-title')
        if match:
            label = match[0].text.replace("*", "").strip()

        match = question.select('div.ss-q-help')
        if match:
            help_text = match[0].text.strip()

        if question.find('textarea'):
            widget = Field.TEXTAREA

        if question.find('select'):
            kind = Field.CHOICE

        if question.find('ul'):
            kind = Field.CHOICE
            widget = Field.RADIOSELECT

        required = len(question.select('.ss-required-asterisk')) > 0

        field = form.field_set.create(
            order=i,
            required=required,
            label=label[:255],
            name=name[:255],
            help_text=help_text[:255],
            widget=widget,
            kind=kind,
        )

        if question.find('select'):
            select = question.find('select')
            field.options = [o.text.strip() for o in select.find_all('option')]

        if question.find('ul'):
            ul = question.find('ul')
            field.options = [o.text.strip() for o in ul.find_all('li')]

    return form
