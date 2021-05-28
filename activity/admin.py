from django.contrib import admin
from .models import *


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('date_time', 'category_id', 'intensity', 'steps', 'heart_rate')
    list_display_links = ('date_time',)
    search_fields = ('category', 'heart_rate')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title', )
    search_fields = ('category', )


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'wakeup_time', 'repeat')
    list_display_links = ('title', 'wakeup_time')
    search_fields = ('title', 'wakeup_time')


class ArticlesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('title', )
    search_fields = ('title', )


admin.site.register(Activity, ActivityAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Alarm, AlarmAdmin)
admin.site.register(Articles, ArticlesAdmin)
