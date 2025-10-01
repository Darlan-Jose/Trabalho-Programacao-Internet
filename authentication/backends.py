from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import Group
from .models import CustomUser, Admin, Dealer
from .utils import check_password, hash_password, is_valid_bcrypt_hash

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None):
        if not username or not password:
            return None
            
        print(f"Tentativa de login: {username}")
        
        try:
            # Verificar se é admin
            admin = Admin.objects.get(admin_name=username)
            print(f"Admin encontrado: {admin.admin_name}")
            print(f"Hash no banco: {admin.passwd[:20]}...")
            print(f"Hash válido: {is_valid_bcrypt_hash(admin.passwd)}")
            
            if check_password(password, admin.passwd):
                print("Senha do admin válida!")
                return self.get_or_create_user(username, password, 'Admin')
            else:
                print("Senha do admin inválida!")
        except Admin.DoesNotExist:
            print("Admin não encontrado")
            pass
        
        try:
            # Verificar se é dealer
            dealer = Dealer.objects.get(dealer_id=username)
            print(f"Dealer encontrado: {dealer.dealer_id}")
            print(f"Hash no banco: {dealer.dlpasswd[:20]}...")
            
            if check_password(password, dealer.dlpasswd):
                print("Senha do dealer válida!")
                return self.get_or_create_user(username, password, 'Dealer')
            else:
                print("Senha do dealer inválida!")
        except Dealer.DoesNotExist:
            print("Dealer não encontrado")
            pass
        
        print("Autenticação falhou")
        return None
    
    def get_or_create_user(self, username, password, group_name):
        try:
            user = CustomUser.objects.get(username=username)
            print(f"Usuário Django encontrado: {user.username}")
        except CustomUser.DoesNotExist:
            print(f"Criando novo usuário Django: {username}")
            user = CustomUser.objects.create_user(username=username, password=password)
        
        # Garantir que o usuário está no grupo correto
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.clear()
        user.groups.add(group)
        user.save()
        
        print(f"Usuário {username} autenticado como {group_name}")
        return user
    
    def get_user(self, user_id):
        try:
            return CustomUser.objects.get(pk=user_id)
        except CustomUser.DoesNotExist:
            return None