from django.contrib import admin
from django.utils.safestring import mark_safe
from django.core.urlresolvers import reverse

from formbuilder import models


class EditLinkToInlineObject(object):
    def edit_link(self, instance):
        url = reverse('admin:%s_%s_change' % (
            instance._meta.app_label,
            instance._meta.module_name),
            args=[instance.pk])
        if instance.pk:
            return mark_safe(u'<a href="{u}">edit</a>'.format(u=url))
        else:
            return ''


class FieldInline(EditLinkToInlineObject, admin.StackedInline):
    model = models.Field
    readonly_fields = ('edit_link',)

    def get_queryset(self, request):
        qs = super(FieldInline, self).get_queryset(request)
        return qs.order_by('order')


@admin.register(models.Form)
class ConferenceAdmin(admin.ModelAdmin):
    inlines = [FieldInline]


class OptionInline(admin.StackedInline):
    model = models.Option


@admin.register(models.Field)
class FieldAdmin(admin.ModelAdmin):
    inlines = [OptionInline]


class EntryInline(admin.TabularInline):
    model = models.Entry
    readonly_fields = ('field', 'value',)
    extra = 0


@admin.register(models.Submission)
class SubmissionAdmin(admin.ModelAdmin):
    readonly_fields = ('form',)
    inlines = [EntryInline]


@admin.register(models.Entry)
class EntryAdmin(admin.ModelAdmin):
    readonly_fields = ('field',)
    pass
