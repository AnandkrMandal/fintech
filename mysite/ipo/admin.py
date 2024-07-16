from django.contrib import admin
from .models import IPO

class IPOAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'price_band', 'open_date', 'close_date', 'issue_size', 'issue_type', 'listing_date', 'status', 'ipo_price', 'listing_price', 'listing_gain', 'current_market_price', 'current_return')
    search_fields = ('company_name', 'status')
    list_filter = ('status', 'open_date', 'close_date', 'listing_date')

admin.site.register(IPO, IPOAdmin)

