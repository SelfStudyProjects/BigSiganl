#!/usr/bin/env python
"""
BigSignal 포트폴리오 성과 차트 생성기
수집된 거래 데이터를 기반으로 다양한 분석 차트를 생성
"""

import os
import sys
import django
from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
from matplotlib import font_manager

# Django 환경 설정
sys.path.append(str(Path(__file__).parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from trades.models import Trade
from portfolios.models import Portfolio, PortfolioSnapshot
from django.db.models import Q
from django.utils import timezone

# 한글 폰트 설정 (윈도우)
plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 스타일 설정
sns.set_style("whitegrid")
plt.style.use('seaborn-v0_8')

class BigSignalChartGenerator:
    """
    BigSignal 포트폴리오 성과 차트 생성기
    """
    
    def __init__(self):
        self.output_dir = Path('media/charts')
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # 포트폴리오 색상 매핑
        self.portfolio_colors = {
            'BTC_Only': '#F7931A',      # 비트코인 오렌지
            'DOGE_Only': '#C2A633',     # 도지 골드
            'USDT_Only': '#26A17B',     # 테더 그린
            'BTC_DOGE': '#FF6B35',      # 오렌지-레드
            'BTC_USDT': '#4A90E2',      # 블루
            'USDT_DOGE': '#7B68EE',     # 슬레이트 블루
            'BTC_USDT_DOGE': '#FF1744'  # 레드
        }
        
        print("📊 BigSignal 차트 생성기 초기화 완료")
    
    def generate_all_charts(self):
        """
        모든 분석 차트 생성
        """
        print("🚀 모든 차트 생성 시작...")
        
        try:
            # 1. 포트폴리오 성과 비교 차트
            self.create_portfolio_performance_chart()
            
            # 2. 시간별 포트폴리오 가치 변화
            self.create_portfolio_value_timeline()
            
            # 3. 자산별 거래 분포
            self.create_asset_distribution_chart()
            
            # 4. 월별 수익률 비교
            self.create_monthly_returns_chart()
            
            # 5. 리스크-수익률 산점도
            self.create_risk_return_scatter()
            
            # 6. Buy & Hold vs BigSignal 비교
            self.create_buy_hold_comparison()
            
            print("✅ 모든 차트 생성 완료!")
            print(f"📁 저장 위치: {self.output_dir.absolute()}")
            
        except Exception as e:
            print(f"❌ 차트 생성 오류: {e}")
            import traceback
            traceback.print_exc()
    
    def create_portfolio_performance_chart(self):
        """
        포트폴리오별 수익률 비교 막대 차트
        """
        print("📈 포트폴리오 성과 비교 차트 생성 중...")
        
        # 데이터 수집
        portfolios = Portfolio.objects.all().order_by('-profit_loss_percentage')
        
        names = [p.name.replace('_', ' ') for p in portfolios]
        returns = [float(p.profit_loss_percentage) for p in portfolios]
        colors = [self.portfolio_colors.get(p.name, '#999999') for p in portfolios]
        
        # 차트 생성
        fig, ax = plt.subplots(figsize=(12, 8))
        bars = ax.bar(names, returns, color=colors, alpha=0.8, edgecolor='white', linewidth=2)
        
        # 수익률 라벨 추가
        for bar, return_val in zip(bars, returns):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + (0.5 if height >= 0 else -1),
                   f'{return_val:.1f}%', ha='center', va='bottom' if height >= 0 else 'top',
                   fontweight='bold', fontsize=11)
        
        # 차트 꾸미기
        ax.set_title('BigSignal 포트폴리오 전략별 수익률 비교', fontsize=16, fontweight='bold', pad=20)
        ax.set_ylabel('수익률 (%)', fontsize=12)
        ax.set_xlabel('포트폴리오 전략', fontsize=12)
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.grid(True, alpha=0.3)
        
        # x축 라벨 회전
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # 저장
        filename = self.output_dir / 'portfolio_performance.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ 저장: {filename}")
    
    def create_portfolio_value_timeline(self):
        """
        시간별 포트폴리오 가치 변화 라인 차트
        """
        print("📊 포트폴리오 가치 변화 타임라인 생성 중...")
        
        # 스냅샷 데이터 수집
        snapshots = PortfolioSnapshot.objects.all().order_by('timestamp')
        
        if not snapshots.exists():
            print("   ⚠️ 포트폴리오 스냅샷 데이터가 없습니다.")
            return
        
        # 데이터프레임 생성
        data = []
        for snapshot in snapshots:
            data.append({
                'timestamp': snapshot.timestamp,
                'portfolio': snapshot.portfolio.name,
                'value': float(snapshot.total_value),
                'profit_loss_pct': float(snapshot.profit_loss_percentage)
            })
        
        df = pd.DataFrame(data)
        
        # 차트 생성
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
        
        # 상단: 절대 가치
        for portfolio_name in df['portfolio'].unique():
            portfolio_data = df[df['portfolio'] == portfolio_name]
            color = self.portfolio_colors.get(portfolio_name, '#999999')
            ax1.plot(portfolio_data['timestamp'], portfolio_data['value'], 
                    label=portfolio_name.replace('_', ' '), color=color, linewidth=2, alpha=0.8)
        
        ax1.set_title('포트폴리오별 총 가치 변화', fontsize=14, fontweight='bold')
        ax1.set_ylabel('포트폴리오 가치 ($)', fontsize=11)
        ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.grid(True, alpha=0.3)
        
        # 하단: 수익률
        for portfolio_name in df['portfolio'].unique():
            portfolio_data = df[df['portfolio'] == portfolio_name]
            color = self.portfolio_colors.get(portfolio_name, '#999999')
            ax2.plot(portfolio_data['timestamp'], portfolio_data['profit_loss_pct'], 
                    label=portfolio_name.replace('_', ' '), color=color, linewidth=2, alpha=0.8)
        
        ax2.set_title('포트폴리오별 수익률 변화', fontsize=14, fontweight='bold')
        ax2.set_ylabel('수익률 (%)', fontsize=11)
        ax2.set_xlabel('시간', fontsize=11)
        ax2.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 저장
        filename = self.output_dir / 'portfolio_timeline.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ 저장: {filename}")
    
    def create_asset_distribution_chart(self):
        """
        자산별 거래 분포 파이 차트
        """
        print("🥧 자산별 거래 분포 차트 생성 중...")
        
        # 자산별 거래 수 집계
        from django.db.models import Count
        asset_counts = Trade.objects.values('asset').annotate(count=Count('id')).order_by('-count')
        
        assets = [item['asset'] for item in asset_counts]
        counts = [item['count'] for item in asset_counts]
        
        # 색상 설정
        colors = ['#F7931A', '#C2A633', '#26A17B', '#FF6B35', '#4A90E2']
        
        # 차트 생성
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # 파이 차트
        wedges, texts, autotexts = ax1.pie(counts, labels=assets, colors=colors[:len(assets)], 
                                          autopct='%1.1f%%', startangle=90, explode=[0.05]*len(assets))
        ax1.set_title('자산별 거래 분포', fontsize=14, fontweight='bold')
        
        # 막대 차트
        bars = ax2.bar(assets, counts, color=colors[:len(assets)], alpha=0.8)
        ax2.set_title('자산별 거래 수', fontsize=14, fontweight='bold')
        ax2.set_ylabel('거래 수', fontsize=11)
        ax2.set_xlabel('자산', fontsize=11)
        
        # 막대 위에 수치 표시
        for bar, count in zip(bars, counts):
            ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                    str(count), ha='center', va='bottom', fontweight='bold')
        
        plt.tight_layout()
        
        # 저장
        filename = self.output_dir / 'asset_distribution.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ 저장: {filename}")
    
    def create_monthly_returns_chart(self):
        """
        월별 수익률 비교 차트
        """
        print("📅 월별 수익률 차트 생성 중...")
        
        # 스냅샷 데이터로부터 월별 수익률 계산
        snapshots = PortfolioSnapshot.objects.all().order_by('timestamp')
        
        if not snapshots.exists():
            print("   ⚠️ 월별 데이터가 부족합니다.")
            return
        
        # 월별 마지막 스냅샷 추출
        monthly_data = {}
        for snapshot in snapshots:
            month_key = snapshot.timestamp.strftime('%Y-%m')
            if month_key not in monthly_data:
                monthly_data[month_key] = {}
            monthly_data[month_key][snapshot.portfolio.name] = float(snapshot.profit_loss_percentage)
        
        # 데이터프레임 생성
        df = pd.DataFrame(monthly_data).T
        df = df.fillna(0)
        
        # 차트 생성
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # 월별 수익률 막대 차트
        x = np.arange(len(df.index))
        width = 0.1
        
        for i, portfolio in enumerate(df.columns):
            color = self.portfolio_colors.get(portfolio, '#999999')
            offset = (i - len(df.columns)/2) * width
            ax.bar(x + offset, df[portfolio], width, label=portfolio.replace('_', ' '), 
                  color=color, alpha=0.8)
        
        ax.set_title('월별 포트폴리오 수익률 비교', fontsize=14, fontweight='bold')
        ax.set_ylabel('수익률 (%)', fontsize=11)
        ax.set_xlabel('월', fontsize=11)
        ax.set_xticks(x)
        ax.set_xticklabels(df.index, rotation=45)
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 저장
        filename = self.output_dir / 'monthly_returns.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ 저장: {filename}")
    
    def create_risk_return_scatter(self):
        """
        리스크-수익률 산점도
        """
        print("🎯 리스크-수익률 산점도 생성 중...")
        
        portfolios = Portfolio.objects.all()
        
        # 각 포트폴리오의 수익률과 변동성 계산
        portfolio_metrics = []
        
        for portfolio in portfolios:
            snapshots = PortfolioSnapshot.objects.filter(portfolio=portfolio).order_by('timestamp')
            
            if snapshots.count() < 2:
                continue
            
            returns = [float(s.profit_loss_percentage) for s in snapshots]
            
            avg_return = np.mean(returns)
            volatility = np.std(returns) if len(returns) > 1 else 0
            
            portfolio_metrics.append({
                'name': portfolio.name,
                'return': avg_return,
                'risk': volatility,
                'current_return': float(portfolio.profit_loss_percentage)
            })
        
        if not portfolio_metrics:
            print("   ⚠️ 리스크 계산을 위한 데이터가 부족합니다.")
            return
        
        # 차트 생성
        fig, ax = plt.subplots(figsize=(10, 8))
        
        for metric in portfolio_metrics:
            color = self.portfolio_colors.get(metric['name'], '#999999')
            ax.scatter(metric['risk'], metric['current_return'], 
                      s=200, color=color, alpha=0.7, edgecolors='white', linewidth=2)
            ax.annotate(metric['name'].replace('_', ' '), 
                       (metric['risk'], metric['current_return']),
                       xytext=(5, 5), textcoords='offset points', fontsize=10)
        
        ax.set_title('포트폴리오 리스크-수익률 분석', fontsize=14, fontweight='bold')
        ax.set_xlabel('리스크 (변동성 %)', fontsize=11)
        ax.set_ylabel('현재 수익률 (%)', fontsize=11)
        ax.grid(True, alpha=0.3)
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax.axvline(x=0, color='black', linestyle='--', alpha=0.5)
        
        plt.tight_layout()
        
        # 저장
        filename = self.output_dir / 'risk_return_scatter.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ 저장: {filename}")
    
    def create_buy_hold_comparison(self):
        """
        Buy & Hold vs BigSignal 전략 비교
        """
        print("⚖️ Buy & Hold 비교 차트 생성 중...")
        
        # 첫 거래와 마지막 거래 시점의 가격 정보 필요
        trades = Trade.objects.all().order_by('timestamp')
        
        if not trades.exists():
            print("   ⚠️ 거래 데이터가 없습니다.")
            return
        
        first_trade = trades.first()
        last_trade = trades.last()
        
        # 자산별 Buy & Hold 수익률 계산 (단순화)
        asset_prices = {}
        for trade in trades:
            if trade.asset not in asset_prices:
                asset_prices[trade.asset] = {'first': None, 'last': None}
            
            if asset_prices[trade.asset]['first'] is None:
                asset_prices[trade.asset]['first'] = float(trade.price)
            asset_prices[trade.asset]['last'] = float(trade.price)
        
        # Buy & Hold 수익률 계산
        buy_hold_returns = {}
        for asset, prices in asset_prices.items():
            if prices['first'] and prices['last']:
                buy_hold_returns[asset] = ((prices['last'] - prices['first']) / prices['first']) * 100
        
        # BigSignal 전략 수익률
        bigsignal_returns = {}
        for portfolio in Portfolio.objects.all():
            bigsignal_returns[portfolio.name] = float(portfolio.profit_loss_percentage)
        
        # 차트 생성
        fig, ax = plt.subplots(figsize=(12, 8))
        
        # Buy & Hold 전략 (자산별)
        x_pos = 0
        for asset, return_val in buy_hold_returns.items():
            ax.bar(x_pos, return_val, width=0.6, label=f'Buy & Hold ({asset})', 
                  color='lightgray', alpha=0.7, edgecolor='black')
            ax.text(x_pos, return_val + 0.5, f'{return_val:.1f}%', 
                   ha='center', va='bottom', fontweight='bold')
            x_pos += 1
        
        # BigSignal 전략들
        x_pos += 0.5
        for portfolio_name, return_val in bigsignal_returns.items():
            color = self.portfolio_colors.get(portfolio_name, '#999999')
            ax.bar(x_pos, return_val, width=0.6, label=f'BigSignal ({portfolio_name.replace("_", " ")})', 
                  color=color, alpha=0.8, edgecolor='white')
            ax.text(x_pos, return_val + 0.5, f'{return_val:.1f}%', 
                   ha='center', va='bottom', fontweight='bold')
            x_pos += 1
        
        ax.set_title('Buy & Hold vs BigSignal 전략 수익률 비교', fontsize=14, fontweight='bold')
        ax.set_ylabel('수익률 (%)', fontsize=11)
        ax.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax.grid(True, alpha=0.3)
        
        # x축 라벨 제거 (범례로 대체)
        ax.set_xticks([])
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        
        plt.tight_layout()
        
        # 저장
        filename = self.output_dir / 'buy_hold_comparison.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"   ✅ 저장: {filename}")
    
    def generate_summary_report(self):
        """
        종합 분석 리포트 생성
        """
        print("📄 종합 분석 리포트 생성 중...")
        
        # 기본 통계
        total_trades = Trade.objects.count()
        portfolios = Portfolio.objects.all()
        
        # 최고/최저 성과 포트폴리오
        best_portfolio = portfolios.order_by('-profit_loss_percentage').first()
        worst_portfolio = portfolios.order_by('profit_loss_percentage').first()
        
        # 자산별 거래 수
        from django.db.models import Count
        asset_counts = Trade.objects.values('asset').annotate(count=Count('id'))
        
        # 기간 정보
        trades = Trade.objects.all().order_by('timestamp')
        if trades.exists():
            start_date = trades.first().timestamp
            end_date = trades.last().timestamp
            period_days = (end_date - start_date).days
        else:
            start_date = end_date = period_days = None
        
        # 리포트 텍스트 생성
        report = f"""
📊 BIGSIGNAL 포트폴리오 성과 분석 리포트
{'='*50}

📈 기본 정보
- 분석 기간: {start_date.strftime('%Y-%m-%d') if start_date else 'N/A'} ~ {end_date.strftime('%Y-%m-%d') if end_date else 'N/A'} ({period_days}일)
- 총 거래 수: {total_trades:,}개
- 분석 포트폴리오: {portfolios.count()}개 전략

🏆 성과 순위
"""
        
        for i, portfolio in enumerate(portfolios.order_by('-profit_loss_percentage'), 1):
            status = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}위"
            report += f"{status} {portfolio.name.replace('_', ' ')}: {portfolio.profit_loss_percentage:.2f}%\n"
        
        report += f"""
📊 자산별 거래 분포
"""
        for item in asset_counts:
            report += f"- {item['asset']}: {item['count']}개 거래\n"
        
        report += f"""
💡 주요 인사이트
- 최고 성과 전략: {best_portfolio.name.replace('_', ' ')} ({best_portfolio.profit_loss_percentage:.2f}%)
- 최저 성과 전략: {worst_portfolio.name.replace('_', ' ')} ({worst_portfolio.profit_loss_percentage:.2f}%)
- 성과 차이: {best_portfolio.profit_loss_percentage - worst_portfolio.profit_loss_percentage:.2f}%p

📁 생성된 차트
- portfolio_performance.png: 전략별 수익률 비교
- portfolio_timeline.png: 시간별 가치 변화
- asset_distribution.png: 자산별 거래 분포  
- monthly_returns.png: 월별 수익률 추이
- risk_return_scatter.png: 리스크-수익률 분석
- buy_hold_comparison.png: Buy & Hold 전략 비교

🕐 생성 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # 리포트 저장
        report_file = self.output_dir / 'analysis_report.txt'
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"   ✅ 저장: {report_file}")
        
        # 콘솔에도 출력
        print(report)

def main():
    """
    메인 실행 함수
    """
    print("🚀 BigSignal 차트 생성기 시작")
    
    generator = BigSignalChartGenerator()
    
    # 모든 차트 생성
    generator.generate_all_charts()
    
    # 종합 리포트 생성
    generator.generate_summary_report()
    
    print("\n✅ 모든 작업 완료!")
    print(f"📁 결과 확인: {generator.output_dir.absolute()}")

if __name__ == "__main__":
    main()