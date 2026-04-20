from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    
    ROLE_USER = 'user'
    ROLE_JOURNALIST = 'journalist'
    ROLE_ADMIN = 'admin'

    ROLE_CHOICES = [
        (ROLE_USER, 'Foydalanuvchi'),
        (ROLE_JOURNALIST, 'Jurnalist'),
        
        (ROLE_ADMIN, 'Admin'),
    ]

    
    REGISTERABLE_ROLES = [ROLE_USER, ROLE_JOURNALIST]

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_USER,
    )
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

   
    is_blocked = models.BooleanField(default=False)
    blocked_until = models.DateTimeField(blank=True, null=True)
    block_reason = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

  

    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_journalist(self):
        return self.role == self.ROLE_JOURNALIST

    @property
    def is_admin(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser

    def check_block_expired(self):
        
        if self.is_blocked and self.blocked_until and timezone.now() > self.blocked_until:
            self.is_blocked = False
            self.blocked_until = None
            self.block_reason = None
            self.save(update_fields=['is_blocked', 'blocked_until', 'block_reason'])
        return self.is_blocked

    @property
    def is_currently_blocked(self):
        return self.check_block_expired()
