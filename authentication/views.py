from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
import time
from .forms import CustomAuthenticationForm, PurchaseForm  
from .decorators import admin_required, dealer_required
from .utils import increment_login_attempts, reset_login_attempts, is_account_locked, get_remaining_attempts
from .models import Vehicle, Dealer, Purchase  

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

@dealer_required
def dealer_vehicles(request):
    """
    View para listar veículos disponíveis para dealers
    """
    vehicles = Vehicle.objects.all().order_by('brand', 'name')
    
    # Estatísticas
    total_vehicles = vehicles.count()
    total_available = sum(vehicle.quantity_available for vehicle in vehicles)
    
    # Agrupar por marca para o template
    vehicles_by_brand = {}
    for vehicle in vehicles:
        if vehicle.brand not in vehicles_by_brand:
            vehicles_by_brand[vehicle.brand] = []
        vehicles_by_brand[vehicle.brand].append(vehicle)
    
    context = {
        'user': request.user,
        'vehicles': vehicles,
        'vehicles_by_brand': vehicles_by_brand,
        'total_vehicles': total_vehicles,
        'total_available': total_available,
    }
    
    response = render(request, 'authentication/vehicles.html', context)
    set_secure_headers(response)
    return response

def public_dealers(request):
    """
    Página pública com lista de dealers disponíveis
    """
    dealers = Dealer.objects.filter(is_public=True).order_by('dealer_name')
    
    context = {
        'dealers': dealers,
        'total_dealers': dealers.count(),
    }
    
    response = render(request, 'authentication/public_dealers.html', context)
    set_secure_headers(response)
    return response

def public_dealer_vehicles(request, dealer_id):
    """
    Página pública com veículos disponíveis de um dealer específico
    """
    dealer = get_object_or_404(Dealer, dealer_id=dealer_id, is_public=True)
    vehicles = Vehicle.objects.all().order_by('brand', 'name')
    
    # Estatísticas
    total_vehicles = vehicles.count()
    total_available = sum(vehicle.quantity_available for vehicle in vehicles)
    
    # Agrupar por marca para o template
    vehicles_by_brand = {}
    for vehicle in vehicles:
        if vehicle.brand not in vehicles_by_brand:
            vehicles_by_brand[vehicle.brand] = []
        vehicles_by_brand[vehicle.brand].append(vehicle)
    
    context = {
        'dealer': dealer,
        'vehicles': vehicles,
        'vehicles_by_brand': vehicles_by_brand,
        'total_vehicles': total_vehicles,
        'total_available': total_available,
    }
    
    response = render(request, 'authentication/public_vehicles.html', context)
    set_secure_headers(response)
    return response

def purchase_vehicle(request, dealer_id, vehicle_id):
    """
    View para processar a compra de um veículo
    """
    dealer = get_object_or_404(Dealer, dealer_id=dealer_id, is_public=True)
    vehicle = get_object_or_404(Vehicle, id=vehicle_id)
    
    # Verificar se o veículo está disponível
    if vehicle.quantity_available <= 0:
        messages.error(request, 'Este veículo não está mais disponível para compra.')
        return redirect('public_dealer_vehicles', dealer_id=dealer.dealer_id)
    
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            try:
                # Criar a compra
                purchase = form.save(commit=False)
                purchase.vehicle = vehicle
                purchase.dealer = dealer
                purchase.save()
                
                # Reduzir a quantidade disponível do veículo
                vehicle.quantity_available -= 1
                vehicle.save()
                
                messages.success(
                    request, 
                    f'Compra realizada com sucesso! Código: {purchase.purchase_code}'
                )
                
                # Redirecionar para página de confirmação
                return redirect('purchase_success', purchase_code=purchase.purchase_code)
                
            except Exception as e:
                messages.error(request, f'Erro ao processar compra: {str(e)}')
        else:
            messages.error(request, 'Por favor, corrija os erros no formulário.')
    else:
        form = PurchaseForm()
    
    context = {
        'form': form,
        'vehicle': vehicle,
        'dealer': dealer,
    }
    
    response = render(request, 'authentication/purchase_form.html', context)
    set_secure_headers(response)
    return response

def purchase_success(request, purchase_code):
    """
    Página de confirmação de compra
    """
    purchase = get_object_or_404(Purchase, purchase_code=purchase_code)
    
    context = {
        'purchase': purchase,
    }
    
    response = render(request, 'authentication/purchase_success.html', context)
    set_secure_headers(response)
    return response

def public_all_vehicles(request):
    """
    Página pública com todos os veículos disponíveis (sem dealer específico)
    """
    vehicles = Vehicle.objects.all().order_by('brand', 'name')
    
    # Estatísticas
    total_vehicles = vehicles.count()
    total_available = sum(vehicle.quantity_available for vehicle in vehicles)
    
    # Agrupar por marca para o template
    vehicles_by_brand = {}
    for vehicle in vehicles:
        if vehicle.brand not in vehicles_by_brand:
            vehicles_by_brand[vehicle.brand] = []
        vehicles_by_brand[vehicle.brand].append(vehicle)
    
    context = {
        'vehicles': vehicles,
        'vehicles_by_brand': vehicles_by_brand,
        'total_vehicles': total_vehicles,
        'total_available': total_available,
    }
    
    response = render(request, 'authentication/public_vehicles.html', context)
    set_secure_headers(response)
    return response