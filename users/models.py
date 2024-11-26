from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Role Name")
    description = models.TextField(blank=True, null=True, verbose_name="Role Description")

    def __str__(self):
        return self.name


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name="Phone Number")
    role = models.ForeignKey(Role, on_delete=models.SET_DEFAULT,default=2, related_name="users")

    def __str__(self):
        return f"{self.username} ({self.role})"
