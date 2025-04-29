from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Stock, UserPortfolio, UserHolding, Transaction
from .forms import RegisterForm


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
           
            login(request, user)
            messages.success(request, "Hesabınız oluşturuldu! 100.000 TL başlangıç bakiyeniz yüklendi.")
            return redirect('core:dashboard')
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def dashboard(request):
    # Portfolio'yu get_or_create ile al
    portfolio, created = UserPortfolio.objects.get_or_create(user=request.user)
    
    stocks = Stock.objects.all()
    return render(request, 'core/dashboard.html', {
        'stocks': stocks,
        'portfolio': portfolio
    })

@login_required
def buy_stock(request, stock_id):
    if request.method == 'POST':
        stock = get_object_or_404(Stock, id=stock_id)
        portfolio = get_object_or_404(UserPortfolio, user=request.user)
        quantity = int(request.POST.get('quantity', 1))

        total_cost = stock.current_price * quantity

        if quantity <= 0:
            messages.error(request, "Geçersiz miktar!")
            return redirect('core:dashboard')

        if portfolio.balance < total_cost:
            messages.error(request, "Yetersiz bakiye!")
            return redirect('core:dashboard')

        # Update portfolio balance
        portfolio.balance -= total_cost
        portfolio.save()

        # Update or create holding
        holding, created = UserHolding.objects.get_or_create(
            portfolio=portfolio,
            stock=stock,
            defaults={
                'quantity': quantity,
                'average_buy_price': stock.current_price
            }
        )

        if not created:
            new_avg = ((holding.average_buy_price * holding.quantity) + 
                       (stock.current_price * quantity)) / (holding.quantity + quantity)
            holding.average_buy_price = new_avg
            holding.quantity += quantity
            holding.save()

        # Create transaction record
        Transaction.objects.create(
            portfolio=portfolio,
            stock=stock,
            transaction_type='BUY',
            quantity=quantity,
            price=stock.current_price
        )

        messages.success(request, f"{stock.symbol} hissesinden {quantity} adet alındı!")

    return redirect('core:dashboard')


@login_required
def sell_stock(request, stock_id):
    if request.method == 'POST':
        stock = get_object_or_404(Stock, id=stock_id)
        portfolio = get_object_or_404(UserPortfolio, user=request.user)
        holding = get_object_or_404(UserHolding, portfolio=portfolio, stock=stock)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            messages.error(request, "Geçersiz miktar!")
            return redirect('core:portfolio')
            
        if holding.quantity < quantity:
            messages.error(request, "Yeterli hisse bulunmuyor!")
            return redirect('core:portfolio')
        
        total_sale = stock.current_price * quantity
        
        # Update portfolio balance
        portfolio.balance += total_sale
        portfolio.save()
        
        # Update holding
        holding.quantity -= quantity
        if holding.quantity == 0:
            holding.delete()
        else:
            holding.save()
        
        # Create transaction record
        Transaction.objects.create(
            portfolio=portfolio,
            stock=stock,
            transaction_type='SELL',
            quantity=quantity,
            price=stock.current_price
        )
        
        messages.success(request, f"{stock.symbol} hissesinden {quantity} adet satıldı!")
    
    return redirect('core:portfolio')

@login_required
def portfolio(request):
    portfolio = get_object_or_404(UserPortfolio, user=request.user)
    holdings = UserHolding.objects.filter(portfolio=portfolio)
    
    total_investment = sum(h.current_value() for h in holdings)
    total_assets = portfolio.balance + total_investment
    
    return render(request, 'core/portfolio.html', {
        'portfolio': portfolio,
        'holdings': holdings,
        'total_investment': total_investment,
        'total_assets': total_assets,
    })

@login_required
def transaction_history(request):
    portfolio = get_object_or_404(UserPortfolio, user=request.user)
    transactions = Transaction.objects.filter(portfolio=portfolio).order_by('-timestamp')
    return render(request, 'core/transactions.html', {
        'transactions': transactions,
        'portfolio': portfolio
    })
@login_required
def clear_transaction_history(request):
    portfolio = get_object_or_404(UserPortfolio, user=request.user)
    Transaction.objects.filter(portfolio=portfolio).delete()
    messages.success(request, "İşlem geçmişiniz başarıyla temizlendi.")
    return redirect('core:transactions')

def leaderboard(request):
    portfolios = UserPortfolio.objects.select_related('user').all()
    leaderboard_data = []
    
    for portfolio in portfolios:
        holdings = UserHolding.objects.filter(portfolio=portfolio)
        investment_value = sum(h.current_value() for h in holdings)
        total_assets = portfolio.balance + investment_value
        
        leaderboard_data.append({
            'user': portfolio.user.username,
            'total_assets': total_assets,
            'balance': portfolio.balance,
            'investment_value': investment_value,
            'profit_loss': total_assets - 100000  # Başlangıç bakiyesine göre kar/zarar
        })
    
    leaderboard_data.sort(key=lambda x: x['total_assets'], reverse=True)
    
    return render(request, 'core/leaderboard.html', {
        'leaderboard': leaderboard_data
    })