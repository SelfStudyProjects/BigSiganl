// src/components/Analysis/InteractiveCharts.js
import React, { useState } from 'react';
import { getChartUrl } from '../../services/api';
import './InteractiveCharts.css';

const InteractiveCharts = () => {
  const [selectedChart, setSelectedChart] = useState('portfolio_performance');
  const [imageError, setImageError] = useState(false);

  const chartOptions = [
    { key: 'portfolio_performance', label: '포트폴리오 성과 비교', icon: '📊' },
    { key: 'timeline', label: '시간별 수익률 변화', icon: '📈' },
    { key: 'asset_distribution', label: '자산 분포', icon: '🥧' },
    { key: 'monthly_returns', label: '월별 수익률', icon: '📅' },
    { key: 'risk_return_scatter', label: '리스크-수익률 분석', icon: '⚖️' },
    { key: 'buy_hold_comparison', label: 'Buy & Hold 비교', icon: '💎' }
  ];

  return (
    <section className="interactive-charts">
      <div className="container">
        <h2>상세 분석 차트</h2>
        
        <div className="chart-tabs">
          {chartOptions.map(option => (
            <button
              key={option.key}
              className={`chart-tab ${selectedChart === option.key ? 'active' : ''}`}
              onClick={() => {
                setSelectedChart(option.key);
                setImageError(false);
              }}
            >
              <span className="tab-icon">{option.icon}</span>
              <span className="tab-label">{option.label}</span>
            </button>
          ))}
        </div>

        <div className="chart-container">
          <p className="chart-description">{getChartDescription(selectedChart)}</p>

          {!imageError ? (
            <img
              src={typeof getChartUrl === 'function' ? getChartUrl(selectedChart) : `/api/analysis/charts/${selectedChart}/`}
              alt={chartOptions.find(opt => opt.key === selectedChart)?.label || selectedChart}
              className="chart-image"
              onError={() => {
                console.warn('Chart image failed to load for', selectedChart);
                setImageError(true);
              }}
            />
          ) : (
            <div className="chart-placeholder">
              <p>⚠️ 차트를 불러올 수 없습니다</p>
              <small>백엔드에서 차트가 생성되었는지, URL(/api/analysis/charts/{selectedChart}/)을 확인하세요.</small>
            </div>
          )}
        </div>
      </div>
    </section>
  );
};

const getChartDescription = (chartType) => {
  const descriptions = {
    portfolio_performance: "7가지 포트폴리오 전략의 최종 수익률을 비교합니다. USDT Only가 가장 우수한 성과를 보였습니다.",
    timeline: "시간이 지남에 따라 각 포트폴리오의 가치가 어떻게 변화했는지 보여줍니다.",
    asset_distribution: "전체 거래 중 각 자산(BTC, DOGE, USDT, USDC)의 거래 빈도를 보여줍니다.",
    monthly_returns: "7월, 8월, 9월 각 월별 포트폴리오 성과를 비교합니다.",
    risk_return_scatter: "각 전략의 리스크(변동성) 대비 수익률을 분석합니다.",
    buy_hold_comparison: "매수 후 보유 전략 대비 BigSignal AI 전략의 성과를 비교합니다."
  };
  
  return (
    <p className="chart-desc">{descriptions[chartType]}</p>
  );
};

export default InteractiveCharts;