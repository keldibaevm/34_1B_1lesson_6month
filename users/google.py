import requests
from django.conf import settings

GOOGLE_AUTH_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
GOOGLE_TOKEN_URL = 'https://oauth2.googleapis.com/token'
GOOGLE_USERINFO_URL = 'https://www.googleapis.com/oauth2/v2/userinfo'

def get_google_auth_url():
    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'redirect_uri': settings.GOOGLE_REDIRECT_URL,
        'response_type': 'code',
        'scope': 'openid email profile',
        'access_type': 'offline',
    }
    query_string = "&".join([f"{key}={value}" for key, value in params.items()])
    return f"{GOOGLE_AUTH_URL}?{query_string}"

def exchange_code_for_token(code):
    params = {
        'client_id': settings.GOOGLE_CLIENT_ID,
        'client_secret': settings.GOOGLE_CLIENT_SECRET,
        'code': code,
        'redirect_uri': settings.GOOGLE_REDIRECT_URL,
        'grant_type': 'authorization_code',
    }
    return response.json()

def get_google_userinfo(access_token):
    response = requests.get(
        GOOGLE_USERINFO_URL,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    return response.json()