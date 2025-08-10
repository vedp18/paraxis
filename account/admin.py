from django.contrib import admin
from .models import UserProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from post.models import Post  # no circular import issue here

# Register your models here.
@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'date_of_birth', 'photo']
    raw_id_fields = ['user']




User = get_user_model()

class PostInline(admin.TabularInline):  # You can use admin.StackedInline if you prefer
    model = Post
    extra = 0  # don't show extra empty forms unless adding
    fields = ('title', 'slug', 'url', 'image', 'description', 'created')
    readonly_fields = ('created',)

class CustomUserAdmin(BaseUserAdmin):
    inlines = [PostInline]
    list_display = ('username', 'email', 'post_count')

    def post_count(self, obj):
        return obj.posts.count()
    post_count.short_description = 'Number of Posts'

# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
