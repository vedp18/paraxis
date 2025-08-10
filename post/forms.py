from django import forms
from django.utils.text import slugify
from .models import Post
from django.core.files.base import ContentFile
import requests

class PostCreateForm(forms.ModelForm):
    image_upload = forms.ImageField(required=False)
    class Meta:
        model = Post
        fields = ['title', 'url', 'description', 'image_upload']
        widgets = {
            'url': forms.HiddenInput(),
        }

    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        if url:
            extension = url.rsplit('.', 1)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url
    
    def save(self,force_insert=False, force_update=False, commit=True):
        post = super().save(commit=False)
        image_file = self.cleaned_data.get('image_upload')
        image_url = self.cleaned_data['url']

        if image_url:
            name = slugify(post.title)
            extension = image_url.rsplit('.', 1)[1].lower()
            image_name = f'{name}.{extension}'
            response = requests.get(image_url)
            post.image.save(image_name, ContentFile(response.content),save=False)
        elif image_file:
            post.image.save(image_file.name, image_file, save=False)

        if commit:
            post.save()
        return post