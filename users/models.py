from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):

    class Role(models.TextChoices):
        ADMIN = "admin", "Админ"
        MODERATOR = "moderator", "Модератор"
        USER = "user", "Пользователь"

    email = models.EmailField(unique=True, verbose_name='email')
    first_name = models.CharField(max_length=50, blank=True, verbose_name='имя')
    last_name = models.CharField(max_length=50, blank=True, verbose_name='фамилия')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='телефон')
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER, verbose_name='роль')
    is_active =models.BooleanField(default=True, verbose_name='активный')
    is_staff = models.BooleanField(default=False, verbose_name='статус персонала')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.email

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'.strip()
    
    