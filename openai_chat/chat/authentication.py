from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import ClientAPIKey

class APIKeyAuthentication(BaseAuthentication):
    keyword = 'Api-Key'

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            raise AuthenticationFailed('Authorization header is missing.')

        try:
            prefix, key = auth_header.split()
        except ValueError:
            raise AuthenticationFailed('Invalid Authorization header format. Use: Api-Key <your_api_key>')

        if prefix != self.keyword:
            raise AuthenticationFailed('Authorization header must start with "Api-Key".')

        try:
            api_key = ClientAPIKey.objects.get(key=key, is_active=True)
        except ClientAPIKey.DoesNotExist:
            raise AuthenticationFailed('Invalid or inactive API key.')

        return (api_key, None)
