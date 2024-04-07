from django.contrib.auth import logout
from django.urls import reverse
from django.shortcuts import redirect
from django.utils import timezone, dateparse

class AdminSessionTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the current path is under the admin URL
        if request.path.startswith(reverse('admin:index')):
            # Check if the user is authenticated and is an admin
            if request.user.is_authenticated and request.user.is_staff:
                current_time = timezone.now()
                
                # Retrieve the last activity time from the session
                last_activity_str = request.session.get('last_admin_activity')
                if last_activity_str:
                    last_activity = dateparse.parse_datetime(last_activity_str)
                    
                    # If the time difference is greater than the timeout period, log out the user
                    if (current_time - last_activity).total_seconds() > 600:  # 10 minutes timeout
                        logout(request)
                        # Optionally, redirect to the admin login page
                        return redirect(reverse('admin:login') + '?next=' + request.path)
                # Update the last activity time in the session
                request.session['last_admin_activity'] = current_time.isoformat()
        
        # For all other requests, just call the next middleware or view
        response = self.get_response(request)
        return response
