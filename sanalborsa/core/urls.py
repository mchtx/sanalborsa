from django.urls import path
from . import views
from .views import register, dashboard, buy_stock, sell_stock, portfolio, transaction_history, leaderboard

app_name = 'core' 

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('buy/<int:stock_id>/', views.buy_stock, name='buy_stock'),
    path('sell/<int:stock_id>/', views.sell_stock, name='sell_stock'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('transactions/', views.transaction_history, name='transactions'),
    path('transactions/clear/', views.clear_transaction_history, name='clear_transactions'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
    
]
