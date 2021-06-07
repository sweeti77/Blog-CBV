from django.contrib import admin
from .models import Blog, Category, Profile


from django.contrib.admin.models import LogEntry

LogEntry.objects.all().delete()


admin.site.site_header = 'BlogAdministration'


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display = ['title', 'slug', 'status', 'posted_date', 'author']
    list_filter = ['posted_date']
    list_editable = ['status']
    search_fields = ['title']
    readonly_fields = ['posted_date', 'updated_date']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}



admin.site.register(Profile)
