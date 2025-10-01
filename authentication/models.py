from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import UserManager as BaseUserManager
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('Usuário deve ter um username')
        
        user = self.model(username=username, **extra_fields)
        if password:
            user.set_password(password)  # Isso já faz o hash
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="customuser_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",
        related_query_name="user",
    )
    
    objects = CustomUserManager()
    
    class Meta:
        db_table = 'auth_user'
    
    def __str__(self):
        return f"{self.username}"

class Admin(models.Model):
    admin_name = models.CharField(max_length=10, primary_key=True)
    passwd = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'admins'

class Dealer(models.Model):
    dealer_id = models.CharField(max_length=5, primary_key=True)
    dealer_name = models.CharField(max_length=20)
    dlpasswd = models.CharField(max_length=255)  
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        db_table = 'dealers'