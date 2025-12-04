from rest_framework import serializers
from .models import Purchase, Vehicle, Dealer

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'name', 'brand', 'body_type', 'quantity_available', 'image']
        read_only_fields = ['id']

class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ['dealer_id', 'dealer_name', 'is_public']
        read_only_fields = ['dealer_id']

class PurchaseSerializer(serializers.ModelSerializer):
    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    dealer_name = serializers.CharField(source='dealer.dealer_name', read_only=True)
    vehicle_id = serializers.IntegerField(write_only=True)
    dealer_id = serializers.CharField(write_only=True)
    
    class Meta:
        model = Purchase
        fields = [
            'id', 'customer_name', 'gender', 'email', 'phone', 
            'monthly_salary', 'purchase_date', 'purchase_code',
            'dealer_id', 'vehicle_id', 'vehicle_name', 'dealer_name',
            'cep', 'street', 'number', 'neighborhood', 'city', 'state'  # NOVOS CAMPOS
        ]
        read_only_fields = ['purchase_code', 'purchase_date', 'id']
    
    def validate(self, data):
        """
        Validação customizada para a compra
        """
        dealer_id = data.get('dealer_id')
        vehicle_id = data.get('vehicle_id')
        
        # Verificar se o dealer existe e é público
        try:
            dealer = Dealer.objects.get(dealer_id=dealer_id, is_public=True)
            data['dealer'] = dealer  # Adiciona o objeto dealer aos dados validados
        except Dealer.DoesNotExist:
            raise serializers.ValidationError({"dealer_id": "Concessionária não encontrada ou não disponível."})
        
        # Verificar se o veículo existe e está disponível
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
            if vehicle.quantity_available <= 0:
                raise serializers.ValidationError({"vehicle_id": "Veículo não disponível para compra."})
            data['vehicle'] = vehicle  # Adiciona o objeto vehicle aos dados validados
        except Vehicle.DoesNotExist:
            raise serializers.ValidationError({"vehicle_id": "Veículo não encontrado."})
        
        return data
    
    def create(self, validated_data):
        """
        Cria a compra e atualiza o estoque do veículo
        """
        # Extrai os objetos que foram adicionados na validação
        vehicle = validated_data.pop('vehicle')
        dealer = validated_data.pop('dealer')
        
        # Remove os IDs pois vamos usar os objetos
        validated_data.pop('vehicle_id', None)
        validated_data.pop('dealer_id', None)
        
        # Criar a compra com os objetos relacionados
        purchase = Purchase.objects.create(
            vehicle=vehicle,
            dealer=dealer,
            **validated_data
        )
        
        # Atualizar estoque
        vehicle.quantity_available -= 1
        vehicle.save()
        
        return purchase

class PurchaseDetailSerializer(serializers.ModelSerializer):
    """
    Serializer específico para leitura de compras
    Inclui informações detalhadas dos relacionamentos
    """
    vehicle_name = serializers.CharField(source='vehicle.name', read_only=True)
    vehicle_brand = serializers.CharField(source='vehicle.brand', read_only=True)
    vehicle_body_type = serializers.CharField(source='vehicle.body_type', read_only=True)
    dealer_name = serializers.CharField(source='dealer.dealer_name', read_only=True)
    dealer_id = serializers.CharField(source='dealer.dealer_id', read_only=True)
    
    class Meta:
        model = Purchase
        fields = [
            'id', 'purchase_code', 'customer_name', 'gender', 'email', 
            'phone', 'monthly_salary', 'purchase_date',
            'dealer_id', 'dealer_name', 'vehicle_id', 'vehicle_name',
            'vehicle_brand', 'vehicle_body_type'
        ]
        read_only_fields = fields  # Todos os campos são somente leitura