from django.test import TestCase
from django.contrib.auth.models import User
from .models import Stock, UserPortfolio

class StockModelTest(TestCase):
    def setUp(self):
        Stock.objects.create(symbol="AKBNK", name="Akbank", current_price=12.34)

    def test_stock_creation(self):
        stock = Stock.objects.get(symbol="AKBNK")
        self.assertEqual(stock.name, "Akbank")

class PortfolioTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        
    def test_portfolio_creation(self):
        portfolio = UserPortfolio.objects.get(user=self.user)
        self.assertEqual(portfolio.balance, 100000.00)