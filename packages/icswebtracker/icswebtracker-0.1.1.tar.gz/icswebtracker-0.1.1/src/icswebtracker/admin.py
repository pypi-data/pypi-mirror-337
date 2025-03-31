from django.contrib import admin
from django.db.models import Count
from django.utils.html import format_html
from .models import Visit


class VisitAdmin(admin.ModelAdmin):
    list_display = ('ip_address', 'path', 'formatted_timestamp', 'status_code', 
                   'country', 'response_time_ms', 'is_authenticated')
    list_filter = ('timestamp', 'status_code', 'http_method', 'is_authenticated', 'country')
    search_fields = ('ip_address', 'path', 'user_agent', 'referrer')
    readonly_fields = ('id', 'timestamp', 'ip_address', 'full_url', 'user_agent',
                      'path', 'http_method', 'referrer', 'response_time_ms',
                      'status_code', 'response_size', 'language', 'country',
                      'is_authenticated', 'user_id', 'session_key')
    date_hierarchy = 'timestamp'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('ip_address', 'path', 'full_url', 'timestamp', 'status_code')
        }),
        ('User Information', {
            'fields': ('user_agent', 'language', 'country', 'is_authenticated', 'user_id', 'session_key')
        }),
        ('Request Details', {
            'fields': ('http_method', 'referrer', 'response_time_ms', 'response_size')
        }),
    )
    
    def formatted_timestamp(self, obj):
        return obj.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    formatted_timestamp.short_description = 'Timestamp'
    
    def has_add_permission(self, request):
        # Visits should only be added by the middleware
        return False
    
    def has_change_permission(self, request, obj=None):
        # Visits should not be modified
        return False


# Register custom admin views
admin.site.register(Visit, VisitAdmin)


# Add an admin site section for WebTracker stats
class WebTrackerAdminSite(admin.AdminSite):
    site_header = 'WebTracker Administration'
    site_title = 'WebTracker Admin'
    index_title = 'WebTracker Management'


# You can uncomment these lines if you want a separate admin site just for WebTracker
# tracker_admin_site = WebTrackerAdminSite(name='webtracker_admin')
# tracker_admin_site.register(Visit, VisitAdmin)