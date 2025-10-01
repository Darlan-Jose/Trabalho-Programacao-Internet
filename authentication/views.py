from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import time
from .forms import CustomAuthenticationForm
from .decorators import admin_required, dealer_required
from .utils import increment_login_attempts, reset_login_attempts, is_account_locked, get_remaining_attempts

@csrf_protect
@csrf_protect
@csrf_protect
def login_view(request):
    """
    View de login com sistema de bloqueio por tentativas - CORRIGIDA
    """
    
    if request.user.is_authenticated:
        messages.info(request, 'Você já está logado.')
        response = HttpResponseRedirect(get_redirect_url(request.user))
        set_secure_headers(response)
        return response
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
        else:
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
        
        
        # AGORA VERIFICA O BLOQUEIO ANTES DE TUDO
        if username:  # Só verifica bloqueio se tem username
            lock_status = is_account_locked(request, username)
            #print(f"🎯 [DEBUG] Status do bloqueio: {lock_status}")
            
            if lock_status['locked']:
                messages.error(request, lock_status['message'])
                form = CustomAuthenticationForm()  
                return render(request, 'authentication/login.html', {
                    'form': form,
                    'account_locked': True,
                    'lock_message': lock_status['message']
                })
        
        # Só agora valida o formulário completo
        if form.is_valid():
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # **LOGIN BEM-SUCEDIDO - Reseta tentativas**
                reset_login_attempts(request, username)
                
                request.session.cycle_key()
                login(request, user)
                
                messages.success(request, f'Login realizado com sucesso! Bem-vindo, {user.username}.')
                
                redirect_url = get_redirect_url(user, request.GET.get('next'))
                response = HttpResponseRedirect(redirect_url)
                set_secure_headers(response)
                return response
            else:
                # **LOGIN FALHOU - Incrementa tentativas**
                attempt_info = increment_login_attempts(request, username)
                remaining_attempts = get_remaining_attempts(request, username)
                
                
                # VERIFICA BLOQUEIO NOVAMENTE APÓS INCREMENTAR
                lock_status = is_account_locked(request, username)
                if lock_status['locked']:
                    messages.error(request, lock_status['message'])
                    return render(request, 'authentication/login.html', {
                        'form': form,
                        'account_locked': True,
                        'lock_message': lock_status['message']
                    })
                
                if remaining_attempts <= 3:
                    messages.warning(request, f'Credenciais inválidas. {remaining_attempts} tentativa(s) restante(s) antes do bloqueio.')
                else:
                    messages.error(request, 'Credenciais inválidas. Verifique seu usuário e senha.')
                
                form.add_error(None, 'Credenciais inválidas')
        else:
            username = request.POST.get('username', '')
            if username:
                attempt_info = increment_login_attempts(request, username)
                remaining_attempts = get_remaining_attempts(request, username)
                
                lock_status = is_account_locked(request, username)
                if lock_status['locked']:
                    messages.error(request, lock_status['message'])
                    form = CustomAuthenticationForm()  
                    return render(request, 'authentication/login.html', {
                        'form': form,
                        'account_locked': True,
                        'lock_message': lock_status['message']
                    })
                
                if remaining_attempts <= 3:
                    messages.warning(request, f'Erro no formulário. {remaining_attempts} tentativa(s) restante(s) antes do bloqueio.')
            
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'authentication/login.html', {
        'form': form,
        'account_locked': False
    })

def logout_view(request):
    """
    View de logout com limpeza segura da sessão e mensagem
    """
    if request.user.is_authenticated:
        username = request.user.username
        if 'login_attempts' in request.session:
            del request.session['login_attempts']
        request.session.flush()
        logout(request)
        messages.success(request, f'Logout realizado com sucesso. Até logo, {username}!')
    else:
        messages.info(request, 'Você não estava logado.')
    
    response = HttpResponseRedirect('/login/')
    set_secure_headers(response)
    return response

def get_redirect_url(user, next_url=None):
    """
    Determina a URL de redirecionamento baseado no grupo do usuário
    """
    if next_url and next_url.startswith('/'):
        return next_url
    
    if user.groups.filter(name='Admin').exists():
        return '/admincar/dashboard/'
    elif user.groups.filter(name='Dealer').exists():
        return '/dealer/dashboard/'
    else:
        return '/dashboard/'

def set_secure_headers(response):
    """
    Configura cabeçalhos de segurança HTTP
    """
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    response['X-Content-Type-Options'] = 'nosniff'
    response['X-Frame-Options'] = 'DENY'
    response['X-XSS-Protection'] = '1; mode=block'
    
    if response.status_code in [301, 302]:
        response['Location'] = response['Location']

@login_required
def dashboard_view(request):
    """
    Dashboard principal com verificação de sessão
    """
    if not request.session.get('_auth_user_id'):
        messages.warning(request, 'Sessão expirada. Por favor, faça login novamente.')
        response = HttpResponseRedirect('/login/')
        set_secure_headers(response)
        return response
    
    messages.info(request, 'Redirecionando para seu dashboard...')
    return redirect(get_redirect_url(request.user))

@admin_required
def admin_dashboard(request):
    """
    Dashboard admin com headers seguros
    """
    if not request.session.get('welcome_shown'):
        messages.success(request, 'Acesso concedido ao Dashboard Administrativo.')
        request.session['welcome_shown'] = True
    
    context = {
        'user': request.user,
        'user_groups': list(request.user.groups.values_list('name', flat=True)),
        'session_key': request.session.session_key[:10] + '...' if request.session.session_key else 'None'
    }
    
    response = render(request, 'authentication/admin_dashboard.html', context)
    set_secure_headers(response)
    return response

@dealer_required
def dealer_dashboard(request):
    """
    Dashboard dealer com headers seguros
    """
    if not request.session.get('welcome_shown'):
        messages.success(request, 'Acesso concedido ao Dashboard Dealer.')
        request.session['welcome_shown'] = True
    
    context = {
        'user': request.user,
        'user_groups': list(request.user.groups.values_list('name', flat=True)),
        'session_key': request.session.session_key[:10] + '...' if request.session.session_key else 'None'
    }
    
    response = render(request, 'authentication/dealer_dashboard.html', context)
    set_secure_headers(response)
    return response

def access_denied(request):
    """
    View para página de acesso negado com mensagem contextual
    """
    message = request.GET.get('message', 'Você não tem permissão para acessar esta página.')
    
    messages.error(request, message)
    
    context = {'message': message}
    response = render(request, 'authentication/access_denied.html', context, status=403)
    set_secure_headers(response)
    return response

def home_view(request):
    """
    Página inicial do sistema
    """
    
    context = {
        'user': request.user,
    }
    
    response = render(request, 'authentication/home.html', context)
    set_secure_headers(response)
    return response