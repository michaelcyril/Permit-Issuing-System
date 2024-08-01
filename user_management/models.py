from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class User(AbstractUser):
    STATUS = (
        ("DELETED", "User deleted"),
        ("ACTIVE", "Active user"),
        ("INACTIVE", "Inactive user"),
    )
    USERTYPE = (
        ("ADMIN", "Admin"),
        ("PERMIT", "Permit Officer"),
        ("AGENT", "Agent"),
        ("NORMAL", "Normal"),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    nida_no = models.CharField(max_length=100, unique=True,null=True,default="nida no",blank=True)
    phone = models.CharField(max_length=12, unique=True)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    status = models.CharField(choices=STATUS, default='INACTIVE', max_length=20)
    usertype = models.CharField(choices=USERTYPE, max_length=20, null=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'

