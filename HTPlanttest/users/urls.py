from django.urls import path
from django.views.generic import TemplateView

from users import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.UserList.as_view(), name='main_page'),
    path('login/', views.UserListLoginView.as_view(), name='login'),
    path('logout/', views.UserListLogoutView.as_view(), name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('edit_profile', views.UpdateProfileView.as_view(), name='edit_profile'),
    path('send-email-verify', views.SendVerifyView.as_view(), name='send_email_verify'),
    path('verify-email/<uidb64>/<token>/', views.EmailVerifyView.as_view(), name='verify_email'),
    path('change-email/<uidb64>/<token>/', views.EmailChange.as_view(), name='change_email'),
    path('invalid-verify', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'),
    path('confirm-email/', TemplateView.as_view(template_name='users/confirm_email.html'), name='confirm_email'),
    path('change-email/', views.EmailChangeView.as_view(), name='email_change'),
    path('change-password/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('change-password/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('reset-password/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]
