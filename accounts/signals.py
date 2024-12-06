from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils.timezone import now
import logging

logger = logging.getLogger('django')

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    # Check user type (admin or regular user)
    user_type = 'Admin' if user.is_staff else 'User'
    
    # Get the IP address (optional, if needed for security)
    ip = get_client_ip(request)
    
    # Log the login details
    logger.info(f"User '{user.username}' ({user_type}) logged in at {now()} from IP: {ip}")

def get_client_ip(request):
    """Utility function to get the client's IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
