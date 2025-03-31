import time
import socket
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin
from ipware import get_client_ip
from .models import Visit 

class TrackMiddleware(MiddlewareMixin):
    """
    Middleware to track website visitor information.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Get configuration from settings or use defaults
        self.tracker_settings = getattr(settings, 'ICSWEBTRACKER_SETTINGS', {})
        self.enabled = self.tracker_settings.get('ENABLED', True)
        self.ignore_paths = self.tracker_settings.get('IGNORE_PATHS', ['/admin/', '/static/', '/media/'])
        self.ignore_ips = self.tracker_settings.get('IGNORE_IPS', [])
        self.track_authenticated = self.tracker_settings.get('TRACK_AUTHENTICATED', True)
        self.track_anonymous = self.tracker_settings.get('TRACK_ANONYMOUS', True)
        self.resolve_country = self.tracker_settings.get('RESOLVE_COUNTRY', False)
        
    def process_request(self, request):
        # Store request start time for response time calculation
        request.start_time = time.time()
        return None
        
    def process_response(self, request, response):
        # Skip tracking if disabled
        if not self.enabled:
            return response
            
        # Skip tracking for ignored paths
        path = request.path
        if any(path.startswith(ignored) for ignored in self.ignore_paths):
            return response
            
        # Get client IP
        client_ip, _ = get_client_ip(request)
        
        # Skip tracking for ignored IPs
        if client_ip in self.ignore_ips:
            return response
            
        # Check if we should track based on authentication status
        is_authenticated = request.user.is_authenticated
        if (is_authenticated and not self.track_authenticated) or (not is_authenticated and not self.track_anonymous):
            return response
            
        # Calculate response time
        response_time = None
        if hasattr(request, 'start_time'):
            response_time = int((time.time() - request.start_time) * 1000)
            
        # Get session key if available
        session_key = None
        if hasattr(request, 'session') and request.session.session_key:
            session_key = request.session.session_key
            
        # Get country if enabled
        country = None
        if self.resolve_country and client_ip:
            country = self._get_country_from_ip(client_ip)
            
        # Extract user language
        language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')[:10] if request.META.get('HTTP_ACCEPT_LANGUAGE') else None
            
        # Create Visit record
        try:
            Visit.objects.create(
                ip_address=client_ip,
                session_key=session_key,
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:1000],
                path=request.path[:255],
                full_url=request.build_absolute_uri()[:500],
                http_method=request.method,
                referrer=request.META.get('HTTP_REFERER', '')[:500],
                timestamp=request.start_time if hasattr(request, 'start_time') else None,
                response_time_ms=response_time,
                status_code=response.status_code,
                response_size=len(response.content) if hasattr(response, 'content') else None,
                language=language,
                country=country,
                is_authenticated=is_authenticated,
                user_id=str(request.user.id) if is_authenticated else None
            )
        except Exception as e:
            # Log error but don't break the response
            if settings.DEBUG:
                print(f"WebTracker error: {e}")
            
        return response
        
    def _get_country_from_ip(self, ip_address):
        """
        Simple IP to country resolution.
        For production use, consider using GeoIP2 or a similar service.
        """
        try:
            # This is a placeholder - for actual implementation,
            # you would use Django GeoIP2 or a third-party service
            return None
        except Exception:
            return None