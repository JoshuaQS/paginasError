from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now

# Manager personalizado para CustomUser
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

# Modelo de usuario personalizado
class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    token = models.CharField(max_length=100, blank=True)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    control_number = models.CharField(max_length=20, unique=True)
    
    # Campos adicionales (si los necesitas)
    age = models.PositiveIntegerField(blank=True, null=True)  # Agrega este campo si es necesario
    tel = models.CharField(max_length=15, blank=True, null=True)  # Agrega este campo si es necesario

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname', 'control_number']  # Solo incluye campos que estén en el modelo

    def __str__(self):
        return self.email