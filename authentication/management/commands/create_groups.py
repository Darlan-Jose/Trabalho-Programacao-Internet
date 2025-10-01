# authentication/management/commands/create_groups.py
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission

class Command(BaseCommand):
    help = 'Cria os grupos iniciais do sistema'

    def handle(self, *args, **options):
        # Grupo Admin
        admin_group, created = Group.objects.get_or_create(name='Admin')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo Admin criado com sucesso'))
        
        # Grupo Dealer
        dealer_group, created = Group.objects.get_or_create(name='Dealer')
        if created:
            self.stdout.write(self.style.SUCCESS('Grupo Dealer criado com sucesso'))