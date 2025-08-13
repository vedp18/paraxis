from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.

# UserProfile model as custom user model
class UserProfile(models.Model):
    # user object will contains all basic user needed fields like username, name, password
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # DOB - optional and can be null
    date_of_birth = models.DateField(blank=True, null=True)
    # photo - optional
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)

    # posts = models.ManyToManyField(Post, related_name='user', blank=True)

    # str method
    def __str__(self):
        return f'UserProfile of {self.user.username}'
    
    def delete(self, *args, **kwargs):
        self.user.delete()
        super().delete(*args, **kwargs)



# This model is for creating MANY_TO_MANY relationship with User (for follow system)
class Contact(models.Model):
    user_from = models.ForeignKey('auth.User',
                                         related_name='rel_from_set',
                                         on_delete=models.CASCADE)
    user_to = models.ForeignKey("auth.User",
                                            related_name='rel_to_set',
                                            on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['-created']),
        ]
        ordering = ['-created']
    def __str__(self):
        return f'{self.user_from} follows {self.user_to} from {self.created}'
    

# Adding "following" field to auth.User model dynamically
user_model = get_user_model()
user_model.add_to_class('following', models.ManyToManyField('self',
                                                            through=Contact,
                                                            related_name='followers',
                                                            symmetrical=False))