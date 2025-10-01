# authentication/management/commands/migrate_passwords.py
from django.core.management.base import BaseCommand
from authentication.utils import hash_password
from authentication.models import Admin, Dealer

class Command(BaseCommand):
    help = 'Migra senhas em texto plano para hash bcrypt'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando migração de senhas...')
        
        # Migrar admins
        admins_migrated = 0
        for admin in Admin.objects.all():
            if not admin.passwd.startswith('$2b$'):
                admin.passwd = hash_password(admin.passwd)
                admin.save()
                admins_migrated += 1
        
        # Migrar dealers
        dealers_migrated = 0
        for dealer in Dealer.objects.all():
            if not dealer.dlpasswd.startswith('$2b$'):
                dealer.dlpasswd = hash_password(dealer.dlpasswd)
                dealer.save()
                dealers_migrated += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Migração concluída: {admins_migrated} admins e {dealers_migrated} dealers migrados'
            )
        )