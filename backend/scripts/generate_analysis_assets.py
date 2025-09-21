"""
Generate analysis charts and a summary report into media/charts/
Usage (Windows PowerShell):
  cd c:\BIGSIGNAL\backend
  .\.venv\Scripts\python.exe scripts\generate_analysis_assets.py

This script will:
- create media/charts (cross-platform)
- generate several placeholder charts using matplotlib/seaborn
- write a text summary report

If DB is available and you want real data, the script can be extended to pull from Django models.
"""
import os
from pathlib import Path
import json

# Create folder cross-platform
BASE_DIR = Path(__file__).resolve().parent.parent
MEDIA_DIR = BASE_DIR / 'media' / 'charts'
MEDIA_DIR.mkdir(parents=True, exist_ok=True)

# Import plotting libs
try:
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    import seaborn as sns
    import numpy as np
    import pandas as pd
except Exception as e:
    print('필수 패키지가 설치되지 않았습니다. 다음을 실행하세요:')
    print('pip install matplotlib pandas seaborn numpy')
    raise

print(f'미디어 폴더: {MEDIA_DIR}')

# Generate synthetic sample data for charts
np.random.seed(42)
days = pd.date_range(end=pd.Timestamp.today(), periods=180)
portfolio_names = ['BTC_Only','USDT_Only','DOGE_Only','BTC_USDT','BTC_DOGE','USDT_DOGE','BTC_USDT_DOGE']

# 1) portfolio_performance.png - cumulative returns
plt.figure(figsize=(10,6))
for name in portfolio_names:
    returns = np.random.normal(loc=0.0005, scale=0.01, size=len(days))
    cum = np.cumprod(1+returns) - 1
    plt.plot(days, cum, label=name)
plt.legend()
plt.title('전략별 누적 수익률 (샘플)')
plt.ylabel('누적 수익률')
plt.xlabel('날짜')
plt.tight_layout()
plt.savefig(MEDIA_DIR / 'portfolio_performance.png')
plt.close()

# 2) portfolio_timeline.png - value over time for one portfolio
plt.figure(figsize=(10,6))
vals = 1000000 * (1 + np.cumsum(np.random.normal(0.0002, 0.005, size=len(days))))
plt.plot(days, vals)
plt.title('포트폴리오 가치 타임라인 (샘플)')
plt.ylabel('KRW')
plt.xlabel('날짜')
plt.tight_layout()
plt.savefig(MEDIA_DIR / 'portfolio_timeline.png')
plt.close()

# 3) asset_distribution.png - pie chart of trade counts
labels = ['BTC','DOGE','USDC','USDT']
sizes = [220, 386, 135, 73]
plt.figure(figsize=(6,6))
plt.pie(sizes, labels=labels, autopct='%1.1f%%')
plt.title('자산별 거래 분포 (샘플)')
plt.savefig(MEDIA_DIR / 'asset_distribution.png')
plt.close()

# 4) monthly_returns.png - monthly returns heatmap
months = pd.date_range(end=pd.Timestamp.today(), periods=12, freq='M').strftime('%Y-%m')
data = np.random.normal(0.01, 0.05, (len(portfolio_names), len(months)))
df = pd.DataFrame(data, index=portfolio_names, columns=months)
plt.figure(figsize=(12,4))
sns.heatmap(df, annot=True, fmt='.2f', cmap='RdYlGn')
plt.title('월별 수익률 히트맵 (샘플)')
plt.tight_layout()
plt.savefig(MEDIA_DIR / 'monthly_returns.png')
plt.close()

# 5) risk_return_scatter.png - scatter risk-return
risks = np.random.uniform(0.05, 0.3, size=len(portfolio_names))
rets = np.random.uniform(-0.1, 0.2, size=len(portfolio_names))
plt.figure(figsize=(8,6))
plt.scatter(risks, rets)
for i, txt in enumerate(portfolio_names):
    plt.annotate(txt, (risks[i], rets[i]))
plt.xlabel('리스크 (표준편차)')
plt.ylabel('연간 수익률 (샘플)')
plt.title('리스크-수익률 스캐터')
plt.tight_layout()
plt.savefig(MEDIA_DIR / 'risk_return_scatter.png')
plt.close()

# 6) buy_hold_comparison.png - buy&hold vs strategy
plt.figure(figsize=(10,6))
buy_hold = np.cumprod(1 + np.random.normal(0.0003, 0.006, size=len(days))) - 1
strategy = np.cumprod(1 + np.random.normal(0.0005, 0.009, size=len(days))) - 1
plt.plot(days, buy_hold, label='Buy & Hold')
plt.plot(days, strategy, label='Signal Strategy')
plt.legend()
plt.title('Buy & Hold 비교 (샘플)')
plt.tight_layout()
plt.savefig(MEDIA_DIR / 'buy_hold_comparison.png')
plt.close()

# 7) analysis_report.txt
report = f"""
BigSignal 분석 리포트 (샘플)
생성일: {pd.Timestamp.today()}

요약:
- 총 포트폴리오 수: {len(portfolio_names)}
- 데이터 범위: 최근 {len(days)}일

상세:
- 각 차트는 샘플 시뮬레이션으로 생성되었습니다. 실제 데이터로 대체하려면 scripts/generate_analysis_assets.py를 수정하여 DB에서 데이터를 읽어오도록 하세요.
"""
with open(MEDIA_DIR / 'analysis_report.txt', 'w', encoding='utf-8') as f:
    f.write(report)

print('미디어 자산 생성 완료:')
for p in MEDIA_DIR.iterdir():
    print(' -', p.name)
