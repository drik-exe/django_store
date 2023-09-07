from django.contrib import auth
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import  reverse_lazy
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from products.models import Basket
from django.views.generic.edit import CreateView, UpdateView
from common.views import TitleMixin


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

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context['baskets'] = Basket.objects.filter(user=self.request.user)
        return context

def logout(request):
    auth.logout(request)
    return redirect('index')


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return redirect('users:profile')
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     baskets = Basket.objects.filter(user=request.user)
#
#     context = {
#         'title': 'Store - Profile',
#         'form': form,
#         'baskets': baskets,
#
#     }
#     return render(request, 'users/profile.html', context)


# def registration(request):
#
#     if request.method == 'POST':
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Поздравляем, вы зарегестрировались')
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password2']
#             user = auth.authenticate(username=username, password=password)
#             auth.login(request, user)
#             return redirect('index')
#     else:
#         form = UserRegistrationForm()
#     context = {
#         'form': form,
#     }
#     return render(request, 'users/registration.html', context)


# def login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = auth.authenticate(username=username, password=password)
#             if user is not None:
#                 auth.login(request, user)
#                 return redirect('index')
#     else:
#         form = UserLoginForm()
#
#     context = {
#         'form': form,
#     }
#     return render(request, 'users/login.html', context)


