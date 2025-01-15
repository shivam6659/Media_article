from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import path, include

urlpatterns = [
    
    # path('', views.dashboard, name='dashboard'),
    path('', views.login_view, name='login'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    
    path('pass_reset_form/', views.pass_reset_form, name='pass_reset_form'),
    path('article_list/', views.article_list, name='article_list'),
    path('enter_otp/', views.enter_otp, name='enter_otp'),  # This view will handle OTP entry
    path('auth/', include('django.contrib.auth.urls')),
    # path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('pass_reset/', views.pass_reset, name='pass_reset'),
    path('pass_change/', views.change_password, name='pass_change'),


    # User Authentication
    # path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Password Reset Flow
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='pass_reset'),
    path('pass_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='pass_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='pass_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='pass_reset_complete'),

    # OTP Verification
    # path('enter_otp/', views.enter_otp, name='enter_otp'),  # This view will handle OTP entry
    # path('verify-otp/', views.verify_otp, name='verify_otp'),  # OTP verification

    path('default_dashboard/', views.default_dashboard, name='default_dashboard'),


    path('dashboard/', views.dashboard, name='dashboard'),

]