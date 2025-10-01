# authentication/management/commands/fix_passwords.py
from django.core.management.base import BaseCommand
import bcrypt
from authentication.models import Admin, Dealer

class Command(BaseCommand):
    help = 'Corrige hashes de senha inválidos'

    def handle(self, *args, **options):
        self.stdout.write('Corrigindo hashes de senha...')
        
        # Gerar hash válido para 'test'
        senha_test = 'test'
        hash_test = bcrypt.hashpw(senha_test.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
        
        # Gerar hash válido para 'dealer123'
        senha_dealer123 = 'dealer123'
        hash_dealer123 = bcrypt.hashpw(senha_dealer123.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
        
        # Gerar hash válido para 'dealer456'
        senha_dealer456 = 'dealer456'
        hash_dealer456 = bcrypt.hashpw(senha_dealer456.encode('utf-8'), bcrypt.gensalt(12)).decode('utf-8')
        
        # Atualizar admin
        try:
            admin = Admin.objects.get(admin_name='root')
            admin.passwd = hash_test
            admin.save()
            self.stdout.write(self.style.SUCCESS('✅ Admin root atualizado'))
        except Admin.DoesNotExist:
            # Criar admin se não existir
            Admin.objects.create(admin_name='root', passwd=hash_test)
            self.stdout.write(self.style.SUCCESS('✅ Admin root criado'))
        
        # Atualizar dealers
        dealers_data = [
            ('D001', 'João Silva', hash_dealer123),
            ('D002', 'Maria Santos', hash_dealer456)
        ]
        
        for dealer_id, dealer_name, hash_senha in dealers_data:
            try:
                dealer = Dealer.objects.get(dealer_id=dealer_id)
                dealer.dlpasswd = hash_senha
                dealer.save()
                self.stdout.write(self.style.SUCCESS(f'✅ Dealer {dealer_id} atualizado'))
            except Dealer.DoesNotExist:
                Dealer.objects.create(
                    dealer_id=dealer_id,
                    dealer_name=dealer_name,
                    dlpasswd=hash_senha
                )
                self.stdout.write(self.style.SUCCESS(f'✅ Dealer {dealer_id} criado'))
        
        self.stdout.write(self.style.SUCCESS('✅ Todas as senhas foram corrigidas!'))