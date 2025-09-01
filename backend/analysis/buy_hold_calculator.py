"""
Buy & Hold 전략 계산기
"""
CLASS BuyHoldCalculator:
    METHOD calculate_buy_hold_performance(asset, start_date, end_date):
        trades = GET trades FOR asset BETWEEN start_date AND end_date
        
        IF no trades:
            RETURN initial performance data
        
        first_trade = trades[0]
        initial_price = first_trade.price
        initial_quantity = initial_budget / initial_price
        
        performance_history = []
        
        FOR each trade IN trades:
            current_value = initial_quantity * trade.price
            pnl_absolute = current_value - initial_budget
            pnl_percentage = (pnl_absolute / initial_budget) * 100
            
            APPEND {
                'timestamp': trade.timestamp,
                'portfolio_value': current_value,
                'pnl_percentage': pnl_percentage,
                'asset_price': trade.price
            } TO performance_history
        
        RETURN performance_history
    
    METHOD generate_buy_hold_data():
        assets = ['BTC', 'USDT', 'DOGE']
        buy_hold_data = {}
        
        FOR each asset:
            performance = calculate_buy_hold_performance(asset)
            buy_hold_data[f'BuyHold_{asset}'] = {
                'asset': asset,
                'initial_budget': initial_budget,
                'performance_history': performance
            }
        
        RETURN buy_hold_data