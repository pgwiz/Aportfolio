# authentication/backends.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import exceptions

class DualAuthBackend(JWTAuthentication):
    def authenticate(self, request):
        # Try JWT first
        try:
            return super().authenticate(request)
        except exceptions.AuthenticationFailed:
            # Fall back to quick credentials
            username = request.data.get('username')
            quick_id = request.data.get('quick_id')
            password = request.data.get('password')
            
            try:
                user = PortfolioUser.objects.get(
                    username=username, 
                    quick_id=quick_id
                )
                if user.check_password(password):
                    return (user, None)
            except PortfolioUser.DoesNotExist:
                pass
            
            return None