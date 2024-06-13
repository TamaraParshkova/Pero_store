from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib. auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin



from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from orders.models import Order
from .forms import LoginForm, RegisterUserForm, ProfileUserForm

class LoginUser(LoginView):
    form_class = LoginForm
    template_name = 'users/login.html'
    extra_context = {'title': "Авторизация"}
    
    # def get_success_url(self):
    #     return reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    extra_context = {'title': "Регистрация"}    
    success_url = reverse_lazy('register_done')

class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': "Профиль пользователя"}
 
    def get_success_url(self):
        return reverse_lazy('profile')
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_orders = Order.objects.filter(user=self.request.user)
        context['user_orders'] = user_orders
        return context

class Logout_user(LogoutView):
    template_name='homepage.html'
 
     

