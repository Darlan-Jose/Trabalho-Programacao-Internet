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
    class Meta:
        model = Purchase
        fields = ['customer_name', 'gender', 'email', 'phone', 'monthly_salary']
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
        }
        labels = {
            'customer_name': 'Nome Completo',
            'gender': 'Gênero',
            'email': 'E-mail',
            'phone': 'Telefone',
            'monthly_salary': 'Salário Mensal (R$)',
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