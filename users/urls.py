from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import *

app_name = 'users'

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('profile/<int:pk>', login_required(UserProfileView.as_view()), name='profile'),
    path('logout/', logout, name='logout'),
    path('verify/<str:email>/<uuid:code>/', EmailVerificationView.as_view(), name='email_verification'),

    path('reset/', EmailInputView.as_view(), name='email_input'),
    path('reset/done/', confirming_view, name='email_done'),
    path('reset/<str:email>/<uuid:code>/', PasswordResetView.as_view(), name='reset_password'),
    path('reset/complete/', reset_complete_view, name='reset_complete'),
]
