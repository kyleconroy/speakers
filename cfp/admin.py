from django.contrib import admin

from cfp.models import Call
from cfp.models import Conference


class CallInline(admin.StackedInline):
    model = Call
    extra = 0
    readonly_fields = ('state',)


def make_all_approved(modeladmin, request, queryset):
    for conf in queryset.all():
        for call in conf.call_set.all():
            call.approve()
            call.save()
make_all_approved.short_description = "Mark selected calls as approved"


def make_all_rejected(modeladmin, request, queryset):
    for conf in queryset.all():
        for call in conf.call_set.all():
            call.reject()
            call.save()
make_all_rejected.short_description = "Mark selected calls as rejected"


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    inlines = [
        CallInline,
    ]
    list_filter = ('call__state', 'created')
    list_display = ('name', 'start', 'end')
    readonly_fields = ('maps_url',)
    actions = [make_all_approved, make_all_rejected]


def make_approved(modeladmin, request, queryset):
    for call in queryset.all():
        call.approve()
        call.save()
make_approved.short_description = "Mark selected calls as approved"


def make_spam(modeladmin, request, queryset):
    for call in queryset.all():
        call.quarantine()
        call.save()
make_approved.short_description = "Mark selected calls as spam"


def make_rejected(modeladmin, request, queryset):
    for call in queryset.all():
        call.reject()
        call.save()
make_rejected.short_description = "Mark selected calls as rejected"


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('conference', 'start', 'end', 'state')
    list_filter = ('state', 'created')
    readonly_fields = ('state',)
    actions = [make_approved, make_rejected, make_spam]
