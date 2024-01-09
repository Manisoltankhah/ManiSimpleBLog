from django.db import models
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class User(AbstractUser):
    profile_picture = models.ImageField(upload_to='static/profile', verbose_name='profile_picture', null=True)
    email_active_code = models.CharField(max_length=100, verbose_name='email_active_code', blank=True, editable=False)
    about_user = models.TextField(null=True, blank=True, verbose_name='about_user')

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        if self.first_name is not '' and self.last_name is not '':
            return self.get_full_name()
        else:
            return self.email
