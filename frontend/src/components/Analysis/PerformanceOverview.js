// src/components/Analysis/PerformanceOverview.js
import React, { useState, useEffect } from 'react';
import { getPerformanceData } from '../../services/api';
import './PerformanceOverview.css';

const safeNumber = (v, fallback = 0) => {
  const n = Number(v);
  return Number.isFinite(n) ? n : fallback;
};

const fmtPercent = (v) => `${v >= 0 ? '+' : ''}${v.toFixed(2)}%`;
const fmtCurrency = (v) => {
  try {
    return Number(v).toLocaleString();
  } catch (e) {
    return String(v);
  }
};

const PerformanceOverview = () => {
  const [portfolios, setPortfolios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await getPerformanceData();
        console.log('API Response:', response);

        const list = Array.isArray(response?.portfolios) ? response.portfolios : [];
        // normalize numeric fields to avoid runtime errors
        const normalized = list.map(p => ({
          name: p.name || p.display_name || 'Unnamed',
          display_name: p.display_name || (p.name || 'Unnamed').replace('_', ' '),
          total_return: safeNumber(p.total_return ?? p.pnl_percentage ?? p.total_return, 0),
          final_value: safeNumber(p.final_value ?? p.current_value ?? p.final_value, 0),
          initial_value: safeNumber(p.initial_value ?? p.initial_budget ?? 0, 0),
          profit_loss: safeNumber(p.profit_loss ?? p.pnl_absolute ?? 0, 0)
        }));

        setPortfolios(normalized);
      } catch (err) {
        console.error('Failed to fetch performance data:', err);
        setError('성과 데이터를 불러오지 못했습니다.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="loading-spinner">로딩 중...</div>;
  }

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  if (!portfolios || portfolios.length === 0) {
    return <div className="empty-message">표시할 포트폴리오 데이터가 없습니다.</div>;
  }

  // 안전한 최고/최저 산출
  const bestPortfolio = portfolios.reduce((prev, curr) =>
    curr.total_return > prev.total_return ? curr : prev
  , portfolios[0]);
  
  const worstPortfolio = portfolios.reduce((prev, curr) =>
    curr.total_return < prev.total_return ? curr : prev
  , portfolios[0]);

  return (
    <section className="performance-overview">
      <h2>포트폴리오 성과 순위</h2>
      <div className="portfolio-grid">
        {portfolios.map((portfolio) => {
          const isBest = portfolio.name === bestPortfolio.name;
          const isWorst = portfolio.name === worstPortfolio.name;
          const isPositive = portfolio.total_return >= 0;

          return (
            <div 
              key={portfolio.name}
              className={`portfolio-card ${isPositive ? 'positive' : 'negative'}`}
            >
              {isBest && <span className="badge best">🏆 최고</span>}
              {isWorst && <span className="badge worst">⚠️ 최저</span>}
              
              <h3>{portfolio.display_name}</h3>
              
              <div className="main-stat">
                <span className="return-percentage">
                  {fmtPercent(portfolio.total_return)}
                </span>
              </div>
              
              <div className="portfolio-stats">
                <div className="stat-row">
                  <span className="label">초기 투자:</span>
                  <span className="value">{fmtCurrency(portfolio.initial_value)}원</span>
                </div>
                <div className="stat-row">
                  <span className="label">현재 가치:</span>
                  <span className="value">{fmtCurrency(portfolio.final_value)}원</span>
                </div>
                <div className="stat-row">
                  <span className="label">손익:</span>
                  <span className={`value ${isPositive ? 'gain' : 'loss'}`}>
                    {isPositive ? '+' : ''}{fmtCurrency(portfolio.profit_loss)}원
                  </span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
};

export default PerformanceOverview;