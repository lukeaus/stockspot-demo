from django.contrib import admin
from .models import Security, Price


class SecurityAdmin(admin.ModelAdmin):
    search_fields = ('code', 'security_id',)
    fields = ('code', 'security_id', 'description', 'security_type', 'price_latest_price',
        'price_latest_date')
    readonly_fields = ('price_latest', 'price_latest_price', 'price_latest_date')


admin.site.register(Security, SecurityAdmin)


class PriceAdmin(admin.ModelAdmin):
    search_fields = ('code', 'security_id',)
    fields = ('security', 'id_security', 'price', 'date', 'price_latest', 'price_latest_price',
        'price_latest_date')
    readonly_fields = ('price_latest', 'price_latest_price', 'price_latest_date')


admin.site.register(Price, PriceAdmin)
