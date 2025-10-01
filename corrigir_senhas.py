# corrigir_senhas.py
import os
import django
import bcrypt

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web_project.settings')
django.setup()

from authentication.models import Admin, Dealer

def criar_hashes_corretos():
    """Cria hashes bcrypt válidos para as senhas padrão"""
    
    # Hash para a senha 'test' (admin)
    senha_test = 'test'
    salt = bcrypt.gensalt(rounds=12)
    hash_test = bcrypt.hashpw(senha_test.encode('utf-8'), salt)
    
    # Hash para a senha 'dealer123' (dealer)
    senha_dealer = 'dealer123'
    hash_dealer = bcrypt.hashpw(senha_dealer.encode('utf-8'), salt)
    
    print("Hashes gerados:")
    print(f"Senha 'test': {hash_test.decode('utf-8')}")
    print(f"Senha 'dealer123': {hash_dealer.decode('utf-8')}")
    
    return hash_test.decode('utf-8'), hash_dealer.decode('utf-8')

def corrigir_banco_dados():
    """Corrige os registros no banco de dados"""
    
    hash_admin, hash_dealer = criar_hashes_corretos()
    
    # Atualizar admin
    try:
        admin = Admin.objects.get(admin_name='root')
        admin.passwd = hash_admin
        admin.save()
        print("✅ Admin 'root' atualizado com sucesso!")
    except Admin.DoesNotExist:
        print("❌ Admin 'root' não encontrado")
    
    # Atualizar dealers
    dealers_data = [
        ('D001', 'João Silva', 'dealer123'),
        ('D002', 'Maria Santos', 'dealer456')
    ]
    
    for dealer_id, dealer_name, senha in dealers_data:
        try:
            dealer = Dealer.objects.get(dealer_id=dealer_id)
            if senha == 'dealer123':
                dealer.dlpasswd = hash_dealer
            else:
                # Hash específico para dealer456
                salt = bcrypt.gensalt(rounds=12)
                hash_specific = bcrypt.hashpw(senha.encode('utf-8'), salt)
                dealer.dlpasswd = hash_specific.decode('utf-8')
            
            dealer.save()
            print(f"✅ Dealer {dealer_id} atualizado com sucesso!")
        except Dealer.DoesNotExist:
            print(f"❌ Dealer {dealer_id} não encontrado")

if __name__ == "__main__":
    print("Iniciando correção das senhas...")
    corrigir_banco_dados()
    print("Correção concluída!")