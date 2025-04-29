from django.contrib import admin
from .models import Stock, UserPortfolio, UserHolding, Transaction

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'name', 'current_price', 'last_updated')
    search_fields = ('symbol', 'name')

@admin.register(UserPortfolio)
class UserPortfolioAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    search_fields = ('user__username',)

@admin.register(UserHolding)
class UserHoldingAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'stock', 'quantity', 'average_buy_price')
    list_filter = ('portfolio__user',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('portfolio', 'stock', 'transaction_type', 'quantity', 'price', 'timestamp')
    list_filter = ('transaction_type', 'portfolio__user')
    date_hierarchy = 'timestamp'