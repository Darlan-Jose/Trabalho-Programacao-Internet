from django.core.management.base import BaseCommand
from django.utils import timezone
from authentication.models import Admin, Dealer, Vehicle

class Command(BaseCommand):
    help = 'Popula o banco de dados com dados iniciais (admins, dealers e veículos)'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Remove todos os registros antes de criar os novos',
        )
    
    def handle(self, *args, **options):
        
        if options['reset']:
            self.stdout.write(self.style.WARNING('⚠️  Removendo todos os registros existentes...'))
            Admin.objects.all().delete()
            Dealer.objects.all().delete()
            Vehicle.objects.all().delete()
            self.stdout.write(self.style.SUCCESS('✅ Todos os registros antigos foram removidos!'))
        
        self.stdout.write('Iniciando população do banco de dados...')
        
        # Criar Admins
        try:
            admin = Admin(
                admin_name='root',
                passwd='test'  
            )
            admin.save()
            self.stdout.write(
                self.style.SUCCESS(f"✅ Admin '{admin.admin_name}' criado com sucesso!")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erro ao criar admin: {e}")
            )
        
        # Criar Dealers
        try:
            dealer = Dealer(
                dealer_id='D001',
                dealer_name='João Silva',
                dlpasswd='dealer123',  
                is_public=True
            )
            dealer.save()
            self.stdout.write(
                self.style.SUCCESS(f"✅ Dealer '{dealer.dealer_name}' criado com sucesso!")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erro ao criar dealer: {e}")
            )
        
        # Criar Veículos
        try:
            vehicles_data = [
                {'name': 'Car_toyota1', 'brand': 'TOYOTA', 'body_type': 'SUV', 'quantity_available': 5},
                {'name': 'Car_toyota2', 'brand': 'TOYOTA', 'body_type': 'SEDAN', 'quantity_available': 3},
                {'name': 'Car_toyota3', 'brand': 'TOYOTA', 'body_type': 'HATCHBACK', 'quantity_available': 8},
                {'name': 'Car_byd1', 'brand': 'BYD', 'body_type': 'SUV', 'quantity_available': 4},
                {'name': 'Car_byd2', 'brand': 'BYD', 'body_type': 'SEDAN', 'quantity_available': 6},
                {'name': 'Car_byd3', 'brand': 'BYD', 'body_type': 'HATCHBACK', 'quantity_available': 2},
            ]
            
            for data in vehicles_data:
                vehicle, created = Vehicle.objects.get_or_create(
                    name=data['name'],
                    defaults={
                        'brand': data['brand'],
                        'body_type': data['body_type'],
                        'quantity_available': data['quantity_available']
                    }
                )
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f"✅ Veículo '{vehicle.name}' criado com sucesso!")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"⚠️  Veículo '{vehicle.name}' já existe!")
                    )
                    
            self.stdout.write(self.style.SUCCESS('✅ Veículos criados com sucesso!'))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"❌ Erro ao criar veículos: {e}")
            )
        
        self.stdout.write(self.style.SUCCESS('🎉 População do banco de dados concluída!'))