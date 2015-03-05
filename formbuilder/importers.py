from django.db import transaction
from bs4 import BeautifulSoup
from formbuilder import models


@transaction.atomic
def parse_google_form(html):
    soup = BeautifulSoup(html)

    form = models.Form(name=soup.find("h1").text)

    for i, question in enumerate(soup.select("div.ss-form-entry")):
        label = ''

        match = question.select('label.ss-q-item-label')
        if match:
            label = match[0].text

        required = question.select('.ss-required-asterisk') is not None

        form.field_set.create(
            order=i,
            required=required,
            label=label
        )

    return form
