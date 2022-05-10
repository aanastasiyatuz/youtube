from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.crypto import get_random_string
from app.utils import crop_img

class MyUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **extra_fields):
        if not email: raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.create_activation_code()
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email: raise ValueError('email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)        
        user.is_superuser = True
        user.is_staff = True
        user.is_active = True
        user.save(using=self._db)
        return user
    
class MyUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=False)
    activation_code = models.CharField(max_length=20, blank=True)
    image = models.ImageField(upload_to='user')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ()

    objects = MyUserManager()

    def create_activation_code(self):
        self.activation_code = get_random_string(18)
        self.save()
    
    def save(self, *a, **k):
        obj = super().save(*a, **k)
        if self.image:
            crop_img(self.image.path)
        return obj

    def __str__(self):
        return self.email


class Follower(models.Model):
    user = models.ForeignKey(MyUser, related_name='followers', on_delete=models.SET_NULL, null=True)
    follow = models.ForeignKey(MyUser, related_name='follows', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.user} -> {self.follow}'