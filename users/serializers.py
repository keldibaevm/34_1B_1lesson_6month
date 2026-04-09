from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate


User = get_user_model()
class RegisterSerializer(serializers.ModelSerializer):
    password =serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'password')
        
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    
    def validate(self, attrs):
        user = authenticate(
            email=attrs['email'],
            password=attrs['password']
        )
        if not user:
            raise serializers.ValidationError('Неверный логин или пароль')
        if not user.is_active:
            raise serializers.ValidationError('Аккаунт деактивирован') 
        data['user'] = user
        return data
    
class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = User
        fields = ('id', 'email', 'full_name', 'created_at')
        read_only_fields = ('id', 'created_at')
    