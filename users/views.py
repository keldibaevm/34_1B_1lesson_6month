from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model

from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .permissions import IsOwnerOrAdmin, IsOwner
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .google import get_google_auth_url, exchange_code_for_token, get_google_userinfo
User = get_user_model()



def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        user = self.get_serializer().instance
        tokens = get_tokens_for_user(user)

        return Response({
            "user": UserSerializer(user).data,
            "tokens": tokens
        }, status=status.HTTP_201_CREATED)
    
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        tokens = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "tokens": tokens
        })

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"detail": "Вы успешно вышли из системы"})

        except KeyError:
            return Response(
                {"detail": "Токен не найден"},
                status=status.HTTP_400_BAD_REQUEST
            )

        except Exception:
            return Response(
                {"detail": "Ошибка при выходе"},
                status=status.HTTP_400_BAD_REQUEST
            )

class MeView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    
    def get_object(self):
        return self.request.user

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class DeactivateUserView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def post(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = False
            user.save()
            return Response({"detail": "Пользователь деактивирован"})
        except User.DoesNotExist:
            return Response({"detail": "Пользователь не найден"}, status=status.HTTP_404_NOT_FOUND)

class GoogleOAuthUrlView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        auth_url = get_google_auth_url()
        return Response({"auth_url": auth_url})

class GoogleOAuthCallbackView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        code = request.query_params.get('code')
        if not code:
            return Response({"detail": "Код не найден"}, status=status.HTTP_400_BAD_REQUEST)
        
        token_data = exchange_code_for_token(code)
        if not token_data:
            return Response({"detail": "Ошибка при обмене кода на токен"}, status=status.HTTP_400_BAD_REQUEST)
        
        access_token = token_data.get('access_token')
        if not access_token:
            return Response({"detail": "Токен не найден"}, status=status.HTTP_400_BAD_REQUEST)
        
        userinfo = get_google_userinfo(access_token)
        if not userinfo:
            return Response({"detail": "Ошибка при получении информации о пользователе"}, status=status.HTTP_400_BAD_REQUEST)
        
        email = userinfo.get('email')
        if not email:
            return Response({"detail": "Email не найден"}, status=status.HTTP_400_BAD_REQUEST)
        
        user, created = User.objects.get_or_create(email=email)
        if created:
            user.set_unusable_password()
            user.save()
        
        tokens = get_tokens_for_user(user)
        return Response({
            "user": UserSerializer(user).data,
            "tokens": tokens
        })
