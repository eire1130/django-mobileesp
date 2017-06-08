from django.conf import settings
from django.utils.functional import SimpleLazyObject
try:
    from django.utils.deprecation import MiddlewareMixin
except:
    class MiddlewareMixin(object):
        pass

DETECT_USER_AGENTS = getattr(settings, 'DETECT_USER_AGENTS', {})

def lazy_detection(request, key):
    detector = DETECT_USER_AGENTS[key]
    return SimpleLazyObject( lambda: detector(request) )


class UserAgentDetectionMiddleware(MiddlewareMixin):
    """
    Middleware to detect request's user agent
    """
    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_request(self, request):
        for each in DETECT_USER_AGENTS:
            setattr( request, each, lazy_detection(request, each) )

