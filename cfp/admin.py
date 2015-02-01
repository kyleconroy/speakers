from django.contrib import admin

from cfp.models import Call
from cfp.models import Conference


@admin.register(Conference)
class ConferenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'start', 'end')


@admin.register(Call)
class CallAdmin(admin.ModelAdmin):
    list_display = ('conference', 'start', 'end')
