from django.shortcuts import redirect
from ..forms import LoginForm
from django.contrib.auth import logout
from django.contrib.auth import views as auth_views


class UserLoginView(auth_views.LoginView):
  template_name = 'accounts/login.html'
  form_class = LoginForm
  success_url = '/dashboard'

def user_logout_view(request):
  logout(request)
  return redirect('/login')
  