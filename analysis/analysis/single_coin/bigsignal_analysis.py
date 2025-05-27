import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from scripts.utils import load_trade_data, calculate_returns, save_results

def analyze_single_coins():
    # 거래 데이터 로드
    trades_df = load_trade_data('bigsignal')
    
    # 분석할 코인 리스트
    coins = ['BTC', 'DOGE', 'USDT']
    investment_amount = 1000000  # 100만원
    
    # 각 코인별 분석
    for coin in coins:
        results = calculate_returns(trades_df, investment_amount, [coin])
        save_results(results, 'bigsignal', 'single_coin', f'{coin.lower()}_results')

if __name__ == '__main__':
    analyze_single_coins()
