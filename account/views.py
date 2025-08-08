from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm, UserEditForm, UserProfileEditForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib import messages
from django.views import View
from django.contrib.auth import logout as auth_logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError



# Create your views here.

# This view is for dashboard after login
@login_required     # adding this helps in protecting pages which required login (it also redirects to login if this views is called and no user is logged in)
def profile(request):
    tab = request.GET.get('tab', 'posts')
    
    dummy_posts = [
        {'image': 'images/post1.jpg', 'created': '2025-08-01'},
        {'image': 'images/post2.jpg', 'created': '2025-08-02'},
        {'image': 'images/post3.jpg', 'created': '2025-08-03'},
        {'image': 'images/post4.jpg', 'created': '2025-08-01'},
        {'image': 'images/post5.jpg', 'created': '2025-08-02'},
        {'image': 'images/post6.jpg', 'created': '2025-08-03'},
        {'image': 'images/post7.jpg', 'created': '2025-08-01'},
        {'image': 'images/post8.jpg', 'created': '2025-08-02'},
        {'image': 'images/post9.jpg', 'created': '2025-08-03'},
        {'image': 'images/post10.jpg', 'created': '2025-08-01'},
        {'image': 'images/post11.jpg', 'created': '2025-08-02'},
        {'image': 'images/post12.jpg', 'created': '2025-08-03'},
    ]

    dummy_followers = [
        {'username': 'john_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'jane_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'john_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'jane_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'john_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'jane_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'john_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'jane_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'john_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'jane_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'john_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'jane_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'john_doe', 'photo': 'images/default_user_profile.webp'},
        {'username': 'jane_doe', 'photo': 'images/default_user_profile.webp'},
    ]

    dummy_following = [
        {'username': 'alex_smith', 'photo': 'images/default_user_profile.webp'},
        {'username': 'emma_jones', 'photo': 'images/default_user_profile.webp'},
        {'username': 'alex_smith', 'photo': 'images/default_user_profile.webp'},
        {'username': 'emma_jones', 'photo': 'images/default_user_profile.webp'},
        {'username': 'alex_smith', 'photo': 'images/default_user_profile.webp'},
        {'username': 'emma_jones', 'photo': 'images/default_user_profile.webp'},
        {'username': 'alex_smith', 'photo': 'images/default_user_profile.webp'},
        {'username': 'emma_jones', 'photo': 'images/default_user_profile.webp'},
        {'username': 'alex_smith', 'photo': 'images/default_user_profile.webp'},
        {'username': 'emma_jones', 'photo': 'images/default_user_profile.webp'},
        {'username': 'alex_smith', 'photo': 'images/default_user_profile.webp'},
        {'username': 'emma_jones', 'photo': 'images/default_user_profile.webp'},
        {'username': 'alex_smith', 'photo': 'images/default_user_profile.webp'},
        {'username': 'emma_jones', 'photo': 'images/default_user_profile.webp'},
        {'username': 'alex_smith', 'photo': 'images/default_user_profile.webp'},
        {'username': 'emma_jones', 'photo': 'images/default_user_profile.webp'},
        {'username': 'alex_smith', 'photo': 'images/default_user_profile.webp'},
        {'username': 'emma_jones', 'photo': 'images/default_user_profile.webp'},
    ]

    return render(request, 'account/profile.html', {
        'tab': tab,
        'posts': dummy_posts,
        'followers': dummy_followers,
        'following': dummy_following,
        'posts_count': len(dummy_posts),
        'followers_count': len(dummy_followers),
        'following_count': len(dummy_following),
    })
    # return render(request,'account/profile.html', {'section': 'profile'})



# This view is for User Login
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

User = get_user_model()

def user_login(request):
    if request.user.is_authenticated:
        return redirect('profile')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username_or_email = cd['username']
            try:
                validate_email(username_or_email)
                lookup_field = 'email'
            except:
                lookup_field = 'username'
                
            try:
                user = User.objects.get(**{lookup_field : username_or_email})
                if not user.is_active:
                    form.add_error(None, "Your account is inactive. Please contact admin.")
                else:
                    user = authenticate(request,
                                        username=cd['username'],
                                        password=cd['password'])
                    if user is not None:
                        login(request, user)
                        return redirect('profile')
                    else:
                        form.add_error(None, "Invalid password.")
            except User.DoesNotExist:
                form.add_error(None, "Invalid username.")
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})



# This view is for logging out user
class UserLogoutView(View):
    # GET
    def get(self, request, *args, **kwargs):
        # if user is already logged out or logged in, for get method just redirect it to account
        return redirect('profile')

    def post(self, request, *args, **kwargs):
        # logout the logged in user
        auth_logout(request)
        
        # for post method just render logged out template
        return render(request, 'registration/logged_out.html')




# This view is for registering new user
def register(request):
    if request.user is not None and request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        registration_form = RegistrationForm(request.POST)
        print(registration_form.errors)
        if registration_form.is_valid():
            # create new User object but avoid saving it
            new_user = registration_form.save(commit=False)
            # Set the choosen password
            new_user.set_password(registration_form.cleaned_data['password'])
            # save the user object
            new_user.save()         
            # create the user profile
            UserProfile.objects.create(user=new_user)
            # render registration_done.html page with new new_user
            return render(request, 'account/registration_done.html', {'new_user': new_user})
        else:
            return render(request, 'account/registration.html', {'registration_form': registration_form})
    else:
        registration_form = RegistrationForm()
        return render(request, 'account/registration.html', {'registration_form': registration_form})


# This view is for editing UserProfile
@login_required
def edit(request):
    if request.method == 'POST':
        user_edit_form = UserEditForm(instance=request.user, 
                                      data=request.POST)
        
        user_profile_edit_form = UserProfileEditForm(instance=request.user.userprofile, 
                                                     data=request.POST, 
                                                     files=request.FILES)

        if user_edit_form.is_valid() and user_profile_edit_form.is_valid():
            user_edit_form.save()
            user_profile_edit_form.save()
            messages.success(request,'Profile updated successfully')
    else:
        user_edit_form = UserEditForm(instance=request.user)
        user_profile_edit_form = UserProfileEditForm(instance=request.user.userprofile)
    
    return render(request, 'account/edit.html', 
                  {'user_edit_form': user_edit_form,
                    'user_profile_edit_form':user_profile_edit_form})


# This is custom csrf failure view which just redirect to account/
def custom_csrf_failure_view(request, reason=""):
    return redirect('profile')