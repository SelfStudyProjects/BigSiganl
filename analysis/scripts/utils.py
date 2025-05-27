import pandas as pd
from datetime import datetime
import os

def get_project_root():
    """프로젝트 루트 디렉토리 경로를 반환합니다."""
    current_path = os.path.abspath(__file__)
    while os.path.basename(current_path) != 'BigSignal':
        current_path = os.path.dirname(current_path)
        if current_path == os.path.dirname(current_path):  # 루트 디렉토리에 도달
            raise Exception("프로젝트 루트 디렉토리를 찾을 수 없습니다.")
    return current_path

def load_trade_data(source: str) -> pd.DataFrame:
    """
    거래 데이터를 로드하는 함수
    
    Args:
        source (str): 'bigsignal' 또는 'bithumb'
    
    Returns:
        pd.DataFrame: 거래 데이터
    """
    project_root = get_project_root()
    file_path = os.path.join(project_root, 'analysis', 'data', source, 'trades.csv')
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"거래 데이터 파일을 찾을 수 없습니다: {file_path}")
    
    df = pd.read_csv(file_path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def calculate_returns(trades_df: pd.DataFrame, investment_amount: float, coins: list) -> dict:
    """
    수익률을 계산하는 함수
    
    Args:
        trades_df (pd.DataFrame): 거래 데이터
        investment_amount (float): 투자 금액
        coins (list): 분석할 코인 리스트
    
    Returns:
        dict: 수익률 정보
    """
    results = {}
    per_coin_amount = investment_amount / len(coins)
    
    for coin in coins:
        coin_trades = trades_df[trades_df['pair'].str.contains(coin)]
        if coin_trades.empty:
            continue
            
        initial_price = coin_trades.iloc[0]['price']
        final_price = coin_trades.iloc[-1]['price']
        
        # 수익률 계산
        returns = ((final_price - initial_price) / initial_price) * 100
        
        results[coin] = {
            'initial_price': initial_price,
            'final_price': final_price,
            'returns': returns,
            'investment_amount': per_coin_amount,
            'final_amount': per_coin_amount * (1 + returns/100)
        }
    
    return results

def save_results(results: dict, source: str, analysis_type: str, filename: str):
    """
    분석 결과를 저장하는 함수
    
    Args:
        results (dict): 분석 결과
        source (str): 'bigsignal' 또는 'bithumb'
        analysis_type (str): 'single_coin', 'two_coins', 'three_coins'
        filename (str): 저장할 파일 이름
    """
    project_root = get_project_root()
    save_dir = os.path.join(project_root, 'results', analysis_type, source)
    os.makedirs(save_dir, exist_ok=True)
    
    # 결과를 DataFrame으로 변환
    results_df = pd.DataFrame.from_dict(results, orient='index')
    results_df.to_csv(os.path.join(save_dir, f'{filename}.csv'), encoding='utf-8-sig')
