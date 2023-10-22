from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.timezone import now

from common.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User, PasswordReset

from datetime import timedelta
import uuid


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Login'


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Вы успешно зареганы'
    title = 'Store - Registration'


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form = UserProfileForm
    form_class = UserProfileForm
    template_name = 'users/profile.html'
    title = 'Store = Profile'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Store - Подтверждение электронной почты'
    template_name = 'users/email_verification.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        user = User.objects.get(email=kwargs['email'])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))


class EmailInputView(View):
    def get(self, request):
        return render(request, 'users/email_input_form.html')

    def post(self, request):
        form_data = request.POST
        email = form_data.get('email')

        try:
            user = User.objects.get(email=email)
            if not user.is_verified_email:
                raise PermissionDenied
            expiration = now() + timedelta(hours=48)
            record = PasswordReset.objects.create(code=uuid.uuid4(), expiration=expiration, email=email)
            record.send_verification_email()
        except ObjectDoesNotExist:
            error_message = "Email не найден"
            return render(request, 'users/email_input_form.html', {'error_message': error_message})
        except:
            error_message = "Email не подтвержден"
            return render(request, 'users/email_input_form.html', {'error_message': error_message})

        return redirect('users:email_done')


class PasswordResetView(TemplateView):
    template_name = 'users/password_reset_form.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']

        email = kwargs['email']
        email_verifications = PasswordReset.objects.filter(code=code, email=email)
        if email_verifications.exists() and not email_verifications.first().is_expired():
            return super(PasswordResetView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse('index'))

    def post(self, request, *args, **kwargs):
        code = kwargs['code']
        user_email = kwargs['email']
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        email_verifications = PasswordReset.objects.filter(code=code, email=user_email)

        if email_verifications.exists() and not email_verifications.first().is_expired():
            user = User.objects.get(email=user_email)
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                return redirect('users:reset_complete')
            else:
                error_message = "Passwords do not match"
                return render(request, self.template_name, {'error_message': error_message})
        return HttpResponseRedirect(reverse('index'))


def confirming_view(request):
    return render(request, 'users/password_reset_done.html')


def reset_complete_view(request):
    return render(request, 'users/password_reset_complete.html')


def logout(request):
    auth.logout(request)
    return redirect('index')
