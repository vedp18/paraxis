from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm, UserEditForm, UserProfileEditForm, SetPasswordForm
from django.contrib.auth import authenticate, login, update_session_auth_hash, get_user_model
from django.contrib.auth.decorators import login_required
from .models import UserProfile
from django.contrib import messages
from django.views import View
from django.contrib.auth import logout as auth_logout
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Contact

import redis
from django.conf import settings
# Connect to redis
r = redis.Redis(host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)



# Create your views here.

# This view is for dashboard after login
@login_required     # adding this helps in protecting pages which required login (it also redirects to login if this views is called and no user is logged in)
def profile(request):
    tab = request.GET.get('tab', 'posts')

    posts = request.user.posts.all()

    keys = [f"post:{post.id}:viewers" for post in posts]
    viewers = r.mget(keys)
    pipe = r.pipeline()
    for post in posts:
        pipe.scard(f"post:{post.id}:viewers")
    
    view_counts = pipe.execute()

    for post, count in zip(posts, view_counts):
        post.total_views = count



    return render(request, 'account/profile.html', {
        'tab' : tab,
        'section': 'profile',
        'posts':posts
    })    


# This view is for User Login
user_model = get_user_model()

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
                user = user_model.objects.get(**{lookup_field : username_or_email})
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
            except user_model.DoesNotExist:
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



# This view is for setting password for only socially signed in with has_usable_password=False users
@login_required
def set_password(request):
    user = request.user
    if user.has_usable_password():
        return redirect('profile')
    
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, user)     # this keeps user logged in even after setting password
            messages.success(request, 'Your password has been set.')
            return redirect('profile')
    else:
        form = SetPasswordForm(user)
    return render(request, 
                  'registration/set_password.html', 
                  {'form':form})



# This view is for providing user_list
@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id).filter(is_active=True, is_superuser=False)
    return render(request, 
                  'account/user/user_list.html', 
                  {'section': 'people',
                    'users': users})

# This view is for user detail view (other users)
@login_required
def user_detail(request, username):
    user = get_object_or_404(User, 
                             username=username, 
                             is_active=True)
    return render(request,
                  'account/user/user_detail.html',
                   {'section': 'people',
                     'user': user})



# This view is for follow or unfollow user
@require_POST
@login_required
def user_follow_unfollow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    print('atleast this was done')
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(
                    user_from=request.user,
                    user_to=user
                )
            else:
                Contact.objects.filter(
                    user_from=request.user,
                    user_to=user
                ).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 
                                 'error': User.DoesNotExist})
    return JsonResponse({'status': 'error',
                         'error': 'Invalid user_id or action'})










# This is custom csrf failure view which just redirect to account/
def custom_csrf_failure_view(request, reason=""):
    return redirect('profile')