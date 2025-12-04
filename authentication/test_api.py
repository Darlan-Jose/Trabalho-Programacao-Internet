# authentication/test_api.py
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import Vehicle, Dealer

class PurchaseAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.dealer = Dealer.objects.create(
            dealer_id="DL001",
            dealer_name="João Silva",
            dlpasswd="dealer123",
            is_public=True
        )
        self.vehicle = Vehicle.objects.create(
            name="Carro Teste",
            brand="TOYOTA",
            body_type="SEDAN",
            quantity_available=5
        )
    
    def test_public_vehicles_api(self):
        response = self.client.get('/api/vehicles/public/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
    
    def test_purchase_api(self):
        data = {
            'customer_name': 'Cliente Teste',
            'gender': 'M',
            'email': 'cliente@teste.com',
            'phone': '11999999999',
            'monthly_salary': '5000.00',
            'dealer_id': self.dealer.dealer_id,
            'vehicle_id': self.vehicle.id
        }
        response = self.client.post('/api/purchase/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])