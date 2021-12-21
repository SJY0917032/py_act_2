from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.shortcuts import redirect, render
from .forms import SignupForm
from django.contrib.auth.views import LoginView, logout_then_login
import hashlib


    
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            signed_user = form.save()
            auth_login(request, signed_user)
            messages.success(request, '회원가입을 환영합니다.')
            signed_user.send_welcome_email()  # FIXME: Celery로 처리하는 것을 추천.
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
    else:
        form = SignupForm()
    return render(request, 'accounts/signup_form.html',{
        'form' : form,
    })
    
    
login = LoginView.as_view(template_name="accounts/login_form.html")
    
def logout(request):
    messages.success(request, '로그아웃 됐습니다.')
    return logout_then_login(request)