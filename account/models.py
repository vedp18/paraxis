from django.db import models
from django.conf import settings

# Create your models here.

# UserProfile model as custom user model
class UserProfile(models.Model):
    # user object will contains all basic user needed fields like username, name, password
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # DOB - optional and can be null
    date_of_birth = models.DateField(blank=True, null=True)
    # photo - optional
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    # str method
    def __str__(self):
        return f'UserProfile of {self.user.username}'
