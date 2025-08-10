from django import forms
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth import password_validation, get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

# Login Form
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

# Registration Form
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    # for validating password and password2 are same or not
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match.')
        else:
            email = self.cleaned_data.get('email')
            tmp_user = User(username=cd['username'], first_name=cd['first_name'], last_name=cd['last_name'], email=email)
            try:
                password_validation.validate_password(cd['password2'], user=tmp_user)
            except ValidationError as error:
                raise forms.ValidationError(error)
        return cd['password2']
    
    # for validating email used, is already not existed
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Account with this e-mail already exists, try logging using this email')
        return email
    
    
    

# UserEditForm
class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    # for validating email entered in edit Profile, is already not existed
    def clean_email(self):
        email = self.cleaned_data['email']
        query_set = User.objects.exclude(id=self.instance.id).filter(email=email)
        if query_set.exists():
            raise forms.ValidationError('Email already exists')
        return email


# UserProfileEditForm
class UserProfileEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['date_of_birth', 'photo']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={
                'type':'date',
                'class': 'date-field'
            })
        }