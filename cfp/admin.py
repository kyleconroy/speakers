from django.contrib import admin

from cfp.models import Call
from cfp.models import Conference


class CallInline(admin.StackedInline):
    model = Call
    extra = 0
    readonly_fields = ('state',)


def make_approved(modeladmin, request, queryset):
    for conf in queryset.all():
        conf.call.approve()
        conf.call.save()
make_approved.short_description = "Mark selected calls as approved"


def make_rejected(modeladmin, request, queryset):
    for conf in queryset.all():
        conf.call.reject()
        conf.call.save()
make_rejected.short_description = "Mark selected calls as rejected"


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    inlines = [
        CallInline,
    ]
    list_filter = ('call__state',)
    list_display = ('name', 'start', 'end')
    actions = [make_approved, make_rejected]


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('conference', 'start', 'end', 'state')
    readonly_fields = ('state',)
