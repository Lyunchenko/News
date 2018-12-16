from django.contrib import admin

from .models import ChoiceIndex, ChoiceType, NewsData, Channels

admin.site.register(ChoiceIndex)
admin.site.register(ChoiceType)
admin.site.register(NewsData)
admin.site.register(Channels)