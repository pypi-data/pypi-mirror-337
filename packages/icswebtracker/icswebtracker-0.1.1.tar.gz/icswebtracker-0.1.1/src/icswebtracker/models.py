from django.db import models
from django.utils import timezone
import uuid

class Visit(models.Model):
    """
    Model to store website visitor information.
    """
    # Unique identifiers
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    session_key = models.CharField(max_length=40, blank=True, null=True)
    
    # Request information
    ip_address = models.GenericIPAddressField(help_text="Visitor's IP address")
    user_agent = models.TextField(blank=True, null=True, help_text="Browser and device information")
    path = models.CharField(max_length=255, help_text="URL path visited")
    full_url = models.URLField(max_length=500, help_text="Complete URL with query parameters")
    http_method = models.CharField(max_length=10, help_text="HTTP method (GET, POST, etc.)")
    referrer = models.URLField(max_length=500, blank=True, null=True, help_text="Referring URL")
    
    # Time information
    timestamp = models.DateTimeField(default=timezone.now, help_text="When the visit occurred")
    response_time_ms = models.PositiveIntegerField(null=True, blank=True, help_text="Server response time in milliseconds")
    
    # Response details
    status_code = models.PositiveSmallIntegerField(help_text="HTTP status code returned")
    response_size = models.PositiveIntegerField(null=True, blank=True, help_text="Size of response in bytes")
    
    # User context
    language = models.CharField(max_length=10, blank=True, null=True, help_text="Visitor's language preference")
    country = models.CharField(max_length=50, blank=True, null=True, help_text="Country based on IP")
    is_authenticated = models.BooleanField(default=False, help_text="Whether the visitor was logged in")
    user_id = models.CharField(max_length=50, blank=True, null=True, help_text="ID of authenticated user")
    
    class Meta:
        indexes = [
            models.Index(fields=['ip_address']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['path']),
            models.Index(fields=['status_code']),
            models.Index(fields=['country']),
        ]
        ordering = ['-timestamp']
        verbose_name = 'Visit'
        verbose_name_plural = 'Visits'
    
    def __str__(self):
        return f"{self.ip_address} - {self.path} ({self.timestamp.strftime('%Y-%m-%d %H:%M:%S')})"