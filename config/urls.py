from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.views import LoginView
from users.views import GoogleOAuthUrlView, GoogleOAuthCallbackView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include("users.urls")),
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/google/', GoogleOAuthUrlView.as_view(), name='google_oauth_url'),
    path('api/auth/google/callback/', GoogleOAuthCallbackView.as_view(), name='google_oauth_callback'),
]
