from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth.models import UserManager as BaseUserManager
from django.utils import timezone
from .utils import hash_password, is_valid_bcrypt_hash 

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
    
    def save(self, *args, **kwargs):
        # Se a senha foi modificada e não está criptografada, criptografar
        if self.passwd and not is_valid_bcrypt_hash(self.passwd):
            self.passwd = hash_password(self.passwd)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.admin_name}"

class Dealer(models.Model):
    dealer_id = models.CharField(max_length=5, primary_key=True)
    dealer_name = models.CharField(max_length=20)
    dlpasswd = models.CharField(max_length=255)  
    created_at = models.DateTimeField(default=timezone.now)
    # NOVO CAMPO - Para dealers que aparecem publicamente
    is_public = models.BooleanField(
        default=False, 
        verbose_name='Disponível Publicamente',
        help_text='Se este dealer aparece na lista pública para clientes'
    )
    
    class Meta:
        db_table = 'dealers'
    
    def save(self, *args, **kwargs):
        # Se a senha foi modificada e não está criptografada, criptografar
        if self.dlpasswd and not is_valid_bcrypt_hash(self.dlpasswd):
            self.dlpasswd = hash_password(self.dlpasswd)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.dealer_name} ({self.dealer_id})"

class Vehicle(models.Model):
    BODY_TYPE_CHOICES = [
        ('SUV', 'SUV'),
        ('SEDAN', 'Sedan'),
        ('HATCHBACK', 'Hatchback'),
    ]
    
    BRAND_CHOICES = [
        ('TOYOTA', 'Toyota'),
        ('BYD', 'BYD'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Nome do Veículo')
    brand = models.CharField(max_length=20, choices=BRAND_CHOICES, verbose_name='Marca')
    body_type = models.CharField(max_length=20, choices=BODY_TYPE_CHOICES, verbose_name='Tipo de Carroceria')
    quantity_available = models.PositiveIntegerField(default=0, verbose_name='Quantidade Disponível')
    # NOVO CAMPO PARA IMAGEM
    image = models.ImageField(
        upload_to='vehicles/',
        verbose_name='Imagem do Veículo',
        blank=True,
        null=True,
        help_text='Imagem do veículo (formatos: JPG, PNG, etc.)'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'vehicles'
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'
    
    def __str__(self):
        return f"{self.name} ({self.brand})"

# NOVO MODELO PARA REGISTRAR COMPRAS
class Purchase(models.Model):
    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('N', 'Prefiro não informar'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name='Veículo Comprado')
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, verbose_name='Concessionária')
    customer_name = models.CharField(max_length=100, verbose_name='Nome Completo')
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Gênero')
    email = models.EmailField(verbose_name='E-mail')
    phone = models.CharField(max_length=20, verbose_name='Número de Telefone')
    monthly_salary = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name='Salário Mensal'
    )
    purchase_date = models.DateTimeField(auto_now_add=True, verbose_name='Data da Compra')
    purchase_code = models.CharField(max_length=10, unique=True, verbose_name='Código da Compra')
    
    class Meta:
        db_table = 'purchases'
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        ordering = ['-purchase_date']
    
    def __str__(self):
        return f"Compra {self.purchase_code} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.purchase_code:
            # Gerar código único para a compra
            import random
            import string
            self.purchase_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        super().save(*args, **kwargs)