import bcrypt
from django.conf import settings
import re
from django.core.cache import cache
import time

# =============================================================================
# SEÇÃO 1: FUNÇÕES DE HASH DE SENHA
# =============================================================================

def hash_password(password):
    """Gera hash bcrypt para a senha"""
    if not password:
        raise ValueError("Password cannot be empty")
    
    # Gerar salt e hash
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def check_password(password, hashed):
    """Verifica se a senha corresponde ao hash"""
    if not password or not hashed:
        return False
    
    if not is_valid_bcrypt_hash(hashed):
        return False

    try:
        password_bytes = password.encode('utf-8')
        hashed_bytes = hashed.encode('utf-8')
        return bcrypt.checkpw(password_bytes, hashed_bytes)
    except Exception as e:
        print(f"[bcrypt.checkpw] Erro ao verificar senha: {e}")
        print(f"password (type={type(password)}): {password}")
        print(f"hashed (type={type(hashed)}): {hashed}")
        return False

def is_valid_bcrypt_hash(hashed):
    """Verifica se a string tem formato de hash bcrypt válido"""
    if not hashed:
        return False
    
    # Padrão do hash bcrypt: $2a$, $2b$, $2y$ seguido de custo e 53 caracteres
    bcrypt_pattern = r'^\$2[abxy]\$\d{2}\$[A-Za-z0-9./]{53}$'
    return re.match(bcrypt_pattern, hashed) is not None

def migrate_single_password(plain_password):
    """Migra uma senha em texto plano para hash bcrypt"""
    if not plain_password:
        return None
    
    return hash_password(plain_password)

def migrate_passwords():
    """Função para migrar senhas em texto plano para hash"""
    from .models import Admin, Dealer
    
    migrated_count = 0
    
    for admin in Admin.objects.all():
        if not is_valid_bcrypt_hash(admin.passwd):
            print(f"Migrando senha do admin: {admin.admin_name}")
            admin.passwd = migrate_single_password(admin.passwd)
            admin.save()
            migrated_count += 1
    
    for dealer in Dealer.objects.all():
        if not is_valid_bcrypt_hash(dealer.dlpasswd):
            print(f"Migrando senha do dealer: {dealer.dealer_id}")
            dealer.dlpasswd = migrate_single_password(dealer.dlpasswd)
            dealer.save()
            migrated_count += 1
    
    return migrated_count

# =============================================================================
# SEÇÃO 2: SISTEMA DE BLOQUEIO POR TENTATIVAS
# =============================================================================

def get_client_ip_address(request):
    """
    Obtém o IP real do cliente (método nativo - sem dependências externas)
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip or 'unknown'

def get_login_attempts_key(username, ip_address):
    """
    Gera chave única para tentativas de login
    """
    return f'login_attempts:{username}:{ip_address}'

def get_ip_block_key(ip_address):
    """
    Gera chave para bloqueio por IP
    """
    return f'ip_block:{ip_address}'

def increment_login_attempts(request, username):
    """
    Incrementa contador de tentativas falhas
    """
    # Configurações padrão caso não estejam definidas
    config = getattr(settings, 'LOGIN_SECURITY_CONFIG', {
        'MAX_LOGIN_ATTEMPTS': 8,
        'LOCKOUT_TIME': 900,
        'IP_LOCKOUT_ATTEMPTS': 15,
        'IP_LOCKOUT_TIME': 1800,
    })
    
    ip_address = get_client_ip_address(request)
    
    # Tentativas na sessão atual
    session_attempts = request.session.get('login_attempts', 0) + 1
    request.session['login_attempts'] = session_attempts
    
    # Tentativas totais no cache
    cache_key = get_login_attempts_key(username, ip_address)
    attempts = cache.get(cache_key, 0) + 1
    cache.set(cache_key, attempts, config['LOCKOUT_TIME'])
    
    # Tentativas por IP
    ip_attempts = cache.get(f'ip_attempts:{ip_address}', 0) + 1
    cache.set(f'ip_attempts:{ip_address}', ip_attempts, config['IP_LOCKOUT_TIME'])
    
    return {
        'session_attempts': session_attempts,
        'total_attempts': attempts,
        'ip_attempts': ip_attempts,
        'ip_address': ip_address,
        'remaining_attempts': max(0, config['MAX_LOGIN_ATTEMPTS'] - attempts)
    }

def reset_login_attempts(request, username):
    """
    Reseta contadores após login bem-sucedido
    """
    ip_address = get_client_ip_address(request)
    
    # Limpa sessão
    if 'login_attempts' in request.session:
        del request.session['login_attempts']
    if 'locked_until' in request.session:
        del request.session['locked_until']
    
    # Limpa cache
    cache_key = get_login_attempts_key(username, ip_address)
    cache.delete(cache_key)
    cache.delete(f'ip_attempts:{ip_address}')
    cache.delete(get_ip_block_key(ip_address))

def is_account_locked(request, username):
    """
    Verifica se a conta está bloqueada
    """
    
    # Configurações padrão
    config = getattr(settings, 'LOGIN_SECURITY_CONFIG', {
        'MAX_LOGIN_ATTEMPTS': 8,
        'LOCKOUT_TIME': 900,
        'IP_LOCKOUT_ATTEMPTS': 15,
        'IP_LOCKOUT_TIME': 1800,
    })
    
    ip_address = get_client_ip_address(request)
    current_time = time.time()
    
    
    # Verifica bloqueio por IP primeiro
    ip_block_key = get_ip_block_key(ip_address)
    ip_blocked_until = cache.get(ip_block_key)
    
    if ip_blocked_until and ip_blocked_until > current_time:
        remaining_time = int((ip_blocked_until - current_time) / 60)
        #print(f"🔍 [DEBUG] BLOQUEADO POR IP - Tempo restante: {remaining_time}min")
        return {
            'locked': True,
            'reason': 'ip',
            'until': ip_blocked_until,
            'message': f'IP bloqueado por excesso de tentativas. Tente novamente em {remaining_time} minutos.'
        }
    
    # Verifica bloqueio por usuário
    cache_key = get_login_attempts_key(username, ip_address)
    attempts = cache.get(cache_key, 0)
    
    # Verifica se excedeu tentativas por IP
    ip_attempts = cache.get(f'ip_attempts:{ip_address}', 0)
    
    if ip_attempts >= config['IP_LOCKOUT_ATTEMPTS']:
        lockout_time = config['IP_LOCKOUT_TIME']
        blocked_until = current_time + lockout_time
        cache.set(ip_block_key, blocked_until, lockout_time)
        remaining_time = int(lockout_time / 60)
        #print(f"🔍 [DEBUG] BLOQUEADO POR IP - Excedeu limite")
        return {
            'locked': True,
            'reason': 'ip',
            'until': blocked_until,
            'message': f'IP bloqueado por excesso de tentativas. Tente novamente em {remaining_time} minutos.'
        }
    
    # Verifica se excedeu tentativas por usuário
    if attempts >= config['MAX_LOGIN_ATTEMPTS']:
        lockout_time = config['LOCKOUT_TIME']
        blocked_until = current_time + lockout_time
        
        
        # Verifica se já está registrado como bloqueado
        lock_key = cache_key + ':locked'
        existing_lock = cache.get(lock_key)
        if not existing_lock or existing_lock < current_time:
            cache.set(lock_key, blocked_until, lockout_time)
            #print(f"🔍 [DEBUG] Novo bloqueio setado até: {blocked_until}")
        
        remaining_time = int((blocked_until - current_time) / 60)
        return {
            'locked': True,
            'reason': 'user',
            'until': blocked_until,
            'message': f'Conta bloqueada por excesso de tentativas. Tente novamente em {remaining_time} minutos.'
        }
    
    return {'locked': False}

def get_remaining_attempts(request, username):
    """
    Retorna tentativas restantes
    """
    config = getattr(settings, 'LOGIN_SECURITY_CONFIG', {
        'MAX_LOGIN_ATTEMPTS': 8,
        'LOCKOUT_TIME': 900,
    })
    
    ip_address = get_client_ip_address(request)
    cache_key = get_login_attempts_key(username, ip_address)
    attempts = cache.get(cache_key, 0)
    
    return max(0, config['MAX_LOGIN_ATTEMPTS'] - attempts)

def get_security_status(request, username):
    """
    Retorna status completo de segurança para debug ou exibição
    """
    ip_address = get_client_ip_address(request)
    lock_status = is_account_locked(request, username)
    remaining = get_remaining_attempts(request, username)
    
    return {
        'ip_address': ip_address,
        'is_locked': lock_status['locked'],
        'lock_reason': lock_status.get('reason', 'none'),
        'lock_message': lock_status.get('message', ''),
        'remaining_attempts': remaining,
        'session_attempts': request.session.get('login_attempts', 0)
    }