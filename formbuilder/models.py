from collections import OrderedDict
from django.db import transaction
from django.db import models
from django import forms


class Form(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def form_class(self):
        fields = OrderedDict()

        for field in self.field_set.order_by('order'):
            fields[field.name] = field.form_field()

        return type('BuiltForm', (forms.BaseForm,), {
            'base_fields': fields
        })

    def submit(self, form):
        sub = Submission(form=self)
        entries = []

        for k, v in form.cleaned_data.items():
            field = form.fields[k].field
            choices = dict(field.choices())

            entries.append(Entry(
                submission=sub,
                field=form.fields[k].field,
                value=str(choices.get(v, v)),
            ))

        with transaction.atomic():
            sub.save()
            sub.entry_set = entries

        return sub


class Field(models.Model):
    BOOLEAN = 1
    CHAR = 2
    CHOICE = 3
    TYPEDCHOICE = 4
    DATE = 5
    DATETIME = 6
    DECIMAL = 7
    EMAIL = 8
    FILE = 9
    FILEPATH = 10
    FLOAT = 11
    IMAGE = 12
    INTEGER = 13
    IPADDRESS = 14
    GENERICIPADDRESS = 15
    MULTIPLECHOICE = 16
    TYPEDMULTIPLECHOICE = 17
    NULLBOOLEAN = 18
    REGEX = 19
    SLUG = 20
    TIME = 21
    URL = 22
    FIELDS = (
        (BOOLEAN, 'BooleanField'),
        (CHAR,  'CharField'),
        (CHOICE, 'ChoiceField'),
        (TYPEDCHOICE, 'TypedChoiceField'),
        (DATE, 'DateField'),
        (DATETIME, 'DateTimeField'),
        (DECIMAL, 'DecimalField'),
        (EMAIL, 'EmailField'),
        (FILE, 'FileField'),
        (FILEPATH, 'FilePathField'),
        (FLOAT, 'FloatField'),
        (IMAGE, 'ImageField'),
        (INTEGER, 'IntegerField'),
        (IPADDRESS, 'IPAddressField'),
        (GENERICIPADDRESS, 'GenericIPAddressField'),
        (MULTIPLECHOICE, 'MultipleChoiceField'),
        (TYPEDMULTIPLECHOICE, 'TypedChoiceField'),
        (NULLBOOLEAN, 'NullBooleanField'),
        (REGEX, 'RegexField'),
        (SLUG, 'SlugField'),
        (TIME, 'TimeField'),
        (URL, 'URLField'),
    )
    TEXTAREA = 1
    NUMBER_INPUT = 2
    EMAIL_INPUT = 3
    URL_INPUT = 4
    HIDDEN_INPUT = 5
    DATE_INPUT = 6
    DATE_TIME_INPUT = 7
    TIME_INPUT = 8
    RADIOSELECT = 9
    CHECKBOX_SELECT_MULTIPLE = 10
    WIDGETS = (
        (0, 'Default widget'),
        (TEXTAREA, 'Textarea'),
        (NUMBER_INPUT, 'NumberInput'),
        (EMAIL_INPUT, 'EmailInput'),
        (URL_INPUT, 'URLInput'),
        (HIDDEN_INPUT, 'HiddenInput'),
        (DATE_INPUT, 'DateInput'),
        (DATE_TIME_INPUT, 'DateTimeInput'),
        (TIME_INPUT, 'TimeInput'),
        (RADIOSELECT, 'RadioSelect'),
        (CHECKBOX_SELECT_MULTIPLE, 'CheckboxSelectMultiple'),
    )

    form = models.ForeignKey(Form)
    name = models.CharField(max_length=255)
    label = models.CharField(max_length=255, default='', blank=True)
    required = models.BooleanField(default=False, blank=True)
    initial = models.CharField(max_length=255, default='', blank=True)
    kind = models.SmallIntegerField(choices=FIELDS, default=CHAR, blank=True)
    widget = models.SmallIntegerField(choices=WIDGETS, default=0, blank=True)
    help_text = models.CharField(max_length=255, default='', blank=True)
    order = models.SmallIntegerField(default=0, blank=True)

    def __str__(self):
        return self.label or self.name

    def get_field_class(self):
        # Default to CharField
        return getattr(forms, dict(self.FIELDS).get(self.kind))

    def get_widget_class(self):
        # Default to CharField
        if self.widget == 0:
            return None
        return getattr(forms, dict(self.WIDGETS).get(self.widget))

    def choices(self):
        if self.kind in set([self.CHOICE, self.MULTIPLECHOICE]):
            return [(str(i), v) for i, v in
                    self.option_set.values_list('id', 'value')]
        else:
            return []

    def form_field(self):
        field_class = self.get_field_class()
        field = field_class(
            required=self.required,
            widget=self.get_widget_class(),
            help_text=self.help_text,
            label=self.label or None,
        )
        field.choices = self.choices()
        field.field = self
        return field

    def pretty_name(self):
        return self.label or self.name.replace('_', ' ').capitalize()

    class Meta:
        unique_together = ("form", "name")


class Option(models.Model):
    field = models.ForeignKey(Field)
    value = models.CharField(max_length=255)

    def __str__(self):
        return self.value


class Submission(models.Model):
    form = models.ForeignKey(Form)

    def __str__(self):
        return "Submission #{}".format(self.id)


class Entry(models.Model):
    submission = models.ForeignKey(Submission)
    field = models.ForeignKey(Field)
    value = models.TextField()
