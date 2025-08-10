from django.urls import include, path
# from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.generic import RedirectView
from . import views 


urlpatterns =[
    # previous Login url
    # path('login/', views.user_login, name='login'),

    # django.contrib.auth urls
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    # path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # path('password-change/',auth_views.PasswordChangeView.as_view(),name='password_change'),
    # path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    # path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    # instead of adding auth_urls manually we can include its urlpatters
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('login/', views.user_login, name='login'),
    path('set-password/', views.set_password, name='set_password'),
    path('', include('django.contrib.auth.urls')),

    path('', login_required(RedirectView.as_view(url='me/', permanent=False))),
    path('me/', views.profile, name='profile'),

    path('register/', views.register, name='register'),
    path('edit/', views.edit, name='edit'),
]