from django.contrib import admin
from .models import Job, Application
from django.utils.html import format_html


# Registering the Job model
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'location', 'job_type', 'created_at')
    search_fields = ('title', 'company', 'location')
    list_filter = ('job_type', 'created_at')
    
# Registering the Application model
@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job', 'applied_at')
    search_fields = ('name', 'email', 'job__title')
    list_filter = ('applied_at',)

    def resume_link(self, obj):
        if obj.resume:
            # Create a clickable link to the resume file
            return format_html('<a href="{}" target="_blank">Open Resume</a>', obj.resume.url)
        return "No Resume"
    resume_link.short_description = 'Resume'

    