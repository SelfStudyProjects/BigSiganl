"""
포트폴리오 시뮬레이션 엔진
"""
CLASS PortfolioEngine:
    INITIALIZE:
        - initial_budget = 1000000
        - portfolios = {}
        - asset_prices = {}
    
    METHOD initialize_portfolios():
        portfolio_configs = [
            {'name': 'BTC_Only', 'assets': ['BTC']},
            {'name': 'USDT_Only', 'assets': ['USDT']},
            {'name': 'DOGE_Only', 'assets': ['DOGE']},
            {'name': 'BTC_USDT', 'assets': ['BTC', 'USDT']},
            {'name': 'BTC_DOGE', 'assets': ['BTC', 'DOGE']},
            {'name': 'USDT_DOGE', 'assets': ['USDT', 'DOGE']},
            {'name': 'BTC_USDT_DOGE', 'assets': ['BTC', 'USDT', 'DOGE']}
        ]
        
        FOR each config:
            CREATE Portfolio instance
            SET initial values
            SAVE to database
    
    METHOD simulate_trade(portfolio, trade):
        IF trade.asset NOT IN portfolio.assets:
            RETURN False  # 이 포트폴리오는 해당 자산을 거래하지 않음
        
        IF trade.action == 'BUY':
            available_cash = portfolio.cash_balance
            trade_amount = available_cash * (trade.percentage / 100)
            
            IF trade_amount > available_cash:
                trade_amount = available_cash
            
            IF trade_amount > 0 AND trade.price > 0:
                quantity_bought = trade_amount / trade.price
                portfolio.holdings[trade.asset] += quantity_bought
                portfolio.cash_balance -= trade_amount
                RETURN True
        
        ELIF trade.action == 'SELL':
            current_holding = portfolio.holdings.get(trade.asset, 0)
            sell_quantity = current_holding * (trade.percentage / 100)
            
            IF sell_quantity > current_holding:
                sell_quantity = current_holding
            
            IF sell_quantity > 0:
                sell_amount = sell_quantity * trade.price
                portfolio.holdings[trade.asset] -= sell_quantity
                portfolio.cash_balance += sell_amount
                RETURN True
        
        RETURN False
    
    METHOD calculate_portfolio_value(portfolio, current_prices):
        total_value = portfolio.cash_balance
        
        FOR asset, quantity IN portfolio.holdings:
            IF quantity > 0:
                asset_price = current_prices.get(asset, 0)
                total_value += quantity * asset_price
        
        RETURN total_value
    
    METHOD update_all_portfolios():
        trades = GET all trades ORDER BY timestamp
        portfolios = GET all portfolios
        
        FOR each portfolio:
            RESET to initial state
            
            FOR each trade:
                IF simulate_trade(portfolio, trade):
                    current_value = calculate_portfolio_value(portfolio)
                    pnl_absolute = current_value - initial_budget
                    pnl_percentage = (pnl_absolute / initial_budget) * 100
                    
                    UPDATE portfolio values
                    CREATE PortfolioSnapshot
                    SAVE portfolio