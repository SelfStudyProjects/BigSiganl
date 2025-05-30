import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from scripts.utils import load_trade_data, calculate_returns, save_results
from itertools import combinations

def analyze_two_coins():
    # 거래 데이터 로드
    trades_df = load_trade_data('bigsignal')
    
    # 분석할 코인 리스트
    coins = ['BTC', 'DOGE', 'USDT']
    investment_amount = 1000000  # 100만원
    
    # 두 개의 코인 조합 분석
    for coin_pair in combinations(coins, 2):
        results = calculate_returns(trades_df, investment_amount, list(coin_pair))
        filename = f"{coin_pair[0].lower()}_{coin_pair[1].lower()}_results"
        save_results(results, 'bigsignal', 'two_coins', filename)

if __name__ == '__main__':
    analyze_two_coins()
