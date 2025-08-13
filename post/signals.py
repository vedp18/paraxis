from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Post

@receiver(m2m_changed, sender=Post.users_liked.through)
def users_liked_changed(sender, instance, **kwargs):
    instance.likes = instance.users_liked.count()
    instance.save()