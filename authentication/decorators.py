from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import Group
from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.contrib import messages
from functools import wraps

def group_required(group_name, login_url=None):
    """
    Decorator para views que verifica se o usuário pertence a um grupo específico.
    """
    def in_group(user):
        if user.is_authenticated:
            return user.groups.filter(name=group_name).exists()
        return False
    
    return user_passes_test(in_group, login_url=login_url)

def admin_required(view_func):
    """
    Decorator específico para usuários Admin com tratamento de acesso negado
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Você precisa estar logado para acessar esta página.')
            from django.shortcuts import redirect
            return redirect('login')
        
        is_admin = request.user.groups.filter(name='Admin').exists()
        if not is_admin:
            messages.error(request, 'Acesso restrito para administradores.')
            return render(request, 'authentication/access_denied.html', {
                'message': 'Acesso restrito para administradores.'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper

def dealer_required(view_func):
    """
    Decorator específico para usuários Dealer com tratamento de acesso negado
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Você precisa estar logado para acessar esta página.')
            from django.shortcuts import redirect
            return redirect('login')
        
        is_dealer = request.user.groups.filter(name='Dealer').exists()
        if not is_dealer:
            messages.error(request, 'Acesso restrito para dealers.')
            return render(request, 'authentication/access_denied.html', {
                'message': 'Acesso restrito para dealers.'
            }, status=403)
        
        return view_func(request, *args, **kwargs)
    return wrapper

def permission_required(perm, login_url=None):
    """
    Decorator para views que verifica se o usuário tem uma permissão específica.
    """
    def has_perm(user):
        if user.is_authenticated:
            return user.has_perm(perm)
        return False
    
    return user_passes_test(has_perm, login_url=login_url)