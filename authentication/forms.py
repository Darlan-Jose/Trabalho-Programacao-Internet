# authentication/forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Purchase

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class PurchaseForm(forms.ModelForm):
    cep = forms.CharField(
        max_length=9,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '00000-000',
            'id': 'cep-field'
        }),
        label='CEP'
    )
    
    class Meta:
        model = Purchase
        fields = [
            'customer_name', 'gender', 'email', 'phone', 'monthly_salary',
            'cep', 'street', 'number', 'neighborhood', 'city', 'state'
        ]
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Seu nome completo'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'seu.email@exemplo.com'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '(11) 99999-9999'
            }),
            'monthly_salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '5000.00',
                'step': '0.01'
            }),
            'street': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da rua',
                'id': 'street-field'
            }),
            'number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '123',
                'id': 'number-field'
            }),
            'neighborhood': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome do bairro',
                'id': 'neighborhood-field'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nome da cidade',
                'id': 'city-field'
            }),
            'state': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'UF',
                'id': 'state-field',
                'maxlength': '2'
            }),
        }
        labels = {
            'customer_name': 'Nome Completo',
            'gender': 'Gênero',
            'email': 'E-mail',
            'phone': 'Telefone',
            'monthly_salary': 'Salário Mensal (R$)',
            'cep': 'CEP',
            'street': 'Rua',
            'number': 'Número',
            'neighborhood': 'Bairro',
            'city': 'Cidade',
            'state': 'Estado',
        }
    
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        # Validação básica de telefone
        if len(phone) < 10:
            raise forms.ValidationError('Número de telefone inválido.')
        return phone
    
    def clean_monthly_salary(self):
        salary = self.cleaned_data.get('monthly_salary')
        if salary <= 0:
            raise forms.ValidationError('O salário deve ser maior que zero.')
        return salary
    
    def clean_cep(self):
        cep = self.cleaned_data.get('cep', '')
        # Remove caracteres não numéricos
        cep = ''.join(filter(str.isdigit, cep))
        if cep and len(cep) != 8:
            raise forms.ValidationError('CEP deve ter 8 dígitos.')
        return cep