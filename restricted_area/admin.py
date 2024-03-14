from django.contrib import admin
from .models import RestrictedAreaData

class RestrictedAreaDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'video_name', 'person_count')

admin.site.register(RestrictedAreaData, RestrictedAreaDataAdmin)
