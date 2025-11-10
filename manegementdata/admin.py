from django.contrib import admin
from .models import (
    Makhbaz, Takiya, 
    Taslima_makhbaz, Taslima_takiya,
    Beneficiary_makhbaz, Beneficiary_takiya
)

@admin.register(Makhbaz)
class MakhbazAdmin(admin.ModelAdmin):
    list_display = ['name', 'governorate', 'oven_type', 'contract_type', 'status', 'created_at']
    list_filter = ['governorate', 'oven_type', 'contract_type', 'status', 'created_at']
    search_fields = ['name', 'owner_name', 'owner_id', 'mobile_number', 'address']
    date_hierarchy = 'created_at'
    list_per_page = 20

@admin.register(Takiya)
class TakiyaAdmin(admin.ModelAdmin):
    list_display = ['name', 'governorate', 'daily_capacity', 'status', 'created_at']
    list_filter = ['governorate', 'status', 'created_at']
    search_fields = ['name', 'owner_name', 'owner_id', 'mobile_number', 'address']
    date_hierarchy = 'created_at'
    list_per_page = 20

@admin.register(Taslima_makhbaz)
class TaslimaMakhbazAdmin(admin.ModelAdmin):
    list_display = ['makhbaz', 'taslima_date', 'flour', 'yeast', 'salt', 'until_date']
    list_filter = ['taslima_date', 'makhbaz__governorate', 'makhbaz']
    search_fields = ['makhbaz__name', 'additions']
    date_hierarchy = 'taslima_date'
    list_per_page = 20
    raw_id_fields = ['makhbaz']

@admin.register(Taslima_takiya)
class TaslimaTakiyaAdmin(admin.ModelAdmin):
    list_display = ['takiya', 'taslima_date', 'rice', 'oil', 'lentils', 'until_date']
    list_filter = ['taslima_date', 'takiya__governorate', 'takiya']
    search_fields = ['takiya__name', 'additions', 'vegetable']
    date_hierarchy = 'taslima_date'
    list_per_page = 20
    raw_id_fields = ['takiya']

@admin.register(Beneficiary_takiya)
class BeneficiaryTakiyaAdmin(admin.ModelAdmin):
    list_display = ['beneficiary_name', 'contact_person', 'phone_number', 'distribution_type', 'distribution_date', 'takiya']
    list_filter = ['distribution_type', 'distribution_date', 'takiya']
    search_fields = ['beneficiary_name', 'contact_person', 'phone_number']
    date_hierarchy = 'distribution_date'
    list_per_page = 20
    raw_id_fields = ['takiya']

@admin.register(Beneficiary_makhbaz)
class BeneficiaryMakhbazAdmin(admin.ModelAdmin):
    list_display = ['beneficiary_name', 'contact_person', 'phone_number', 'distribution_type', 'distribution_date', 'makhbaz']
    list_filter = ['distribution_type', 'distribution_date', 'makhbaz']
    search_fields = ['beneficiary_name', 'contact_person', 'phone_number']
    date_hierarchy = 'distribution_date'
    list_per_page = 20
    raw_id_fields = ['makhbaz']
    