from django.contrib import admin
from django import forms
from .models import Vehicle, Dealer, Purchase, Admin
from .utils import hash_password, is_valid_bcrypt_hash

# Register your models here.

class AdminForm(forms.ModelForm):
    class Meta:
        model = Admin
        fields = '__all__'
    
    def clean_passwd(self):
        password = self.cleaned_data.get('passwd')
        # Se a senha foi alterada e não está criptografada, criptografar
        if password and not is_valid_bcrypt_hash(password):
            return hash_password(password)
        return password

class DealerForm(forms.ModelForm):
    class Meta:
        model = Dealer
        fields = '__all__'
    
    def clean_dlpasswd(self):
        password = self.cleaned_data.get('dlpasswd')
        # Se a senha foi alterada e não está criptografada, criptografar
        if password and not is_valid_bcrypt_hash(password):
            return hash_password(password)
        return password

@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    form = AdminForm
    list_display = ['admin_name', 'created_at']
    search_fields = ['admin_name']

@admin.register(Dealer)
class DealerAdmin(admin.ModelAdmin):
    form = DealerForm
    list_display = ['dealer_id', 'dealer_name', 'is_public', 'created_at']
    list_filter = ['is_public', 'created_at']
    search_fields = ['dealer_id', 'dealer_name']
    list_editable = ['is_public']

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'body_type', 'quantity_available', 'created_at', 'image_preview']
    list_filter = ['brand', 'body_type']
    search_fields = ['name', 'brand']
    ordering = ['brand', 'name']
    readonly_fields = ['image_preview']
    
    def image_preview(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 50px; max-width: 50px;" />'
        return "Sem imagem"
    image_preview.short_description = 'Preview'
    image_preview.allow_tags = True

@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ['purchase_code', 'customer_name', 'vehicle', 'dealer', 'purchase_date']
    list_filter = ['dealer', 'purchase_date', 'gender']
    search_fields = ['customer_name', 'email', 'purchase_code']
    readonly_fields = ['purchase_date', 'purchase_code']
    ordering = ['-purchase_date']