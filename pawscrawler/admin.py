from django.contrib import admin

from .models import Pet, PollRecord

admin.site.register(Pet)
admin.site.register(PollRecord)