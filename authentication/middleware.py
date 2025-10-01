from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied
from django.contrib import messages

class SecurityHeadersMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Adiciona headers de segurança em todas as respostas
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Prevenir cache de páginas sensíveis
        if request.path.startswith('/admin/') or request.path.startswith('/dealer/'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        
        return response

class SessionSecurityMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Regenera sessão periodicamente
        if request.user.is_authenticated:
            if not request.session.get('session_regenerated'):
                request.session.cycle_key()
                request.session['session_regenerated'] = True

class AccessControlMiddleware(MiddlewareMixin):
    """
    Middleware para tratamento global de acesso negado
    """
    def process_exception(self, request, exception):
        if isinstance(exception, PermissionDenied):
            messages.error(request, 'Acesso negado. Permissão insuficiente.')
            from django.shortcuts import render
            return render(request, 'authentication/access_denied.html', {
                'message': 'Acesso negado. Permissão insuficiente.'
            }, status=403)
        return None

class SessionExpiryMiddleware(MiddlewareMixin):
    """
    Middleware para detectar sessão expirada e mostrar mensagem
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            # Verifica se a sessão expirou
            if not request.session.get('_auth_user_id'):
                messages.warning(request, 'Sua sessão expirou. Por favor, faça login novamente.')
                from django.contrib.auth import logout
                logout(request)
                return redirect('login')