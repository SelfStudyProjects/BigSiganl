// src/components/Analysis/PerformanceOverview.js
import React, { useState, useEffect } from 'react';
import { api } from '../../services/api';
import './PerformanceOverview.css';

const PerformanceOverview = () => {
  const [performanceData, setPerformanceData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await api.getPerformanceData();
        setPerformanceData(data);
      } catch (error) {
        console.error('성과 데이터 로드 실패:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) return <div className="loading">로딩 중...</div>;

  const portfolios = performanceData?.portfolios || [];
  const sortedPortfolios = [...portfolios].sort((a, b) => b.total_return - a.total_return);

  return (
    <section className="performance-overview">
      <div className="container">
        <h2>포트폴리오 성과 순위</h2>
        
        <div className="performance-grid">
          {sortedPortfolios.map((portfolio, index) => (
            <div 
              key={portfolio.name} 
              className={`performance-card ${index === 0 ? 'best' : index >= sortedPortfolios.length - 2 ? 'worst' : ''}`}
            >
              <div className="rank">#{index + 1}</div>
              <div className="portfolio-name">{portfolio.name}</div>
              <div className={`return-rate ${portfolio.total_return >= 0 ? 'positive' : 'negative'}`}>
                {portfolio.total_return >= 0 ? '+' : ''}{portfolio.total_return.toFixed(2)}%
              </div>
              <div className="final-value">
                {portfolio.final_value.toLocaleString()}원
              </div>
              {index === 0 && <div className="badge best">최고 성과</div>}
              {index >= sortedPortfolios.length - 2 && <div className="badge worst">주의 필요</div>}
            </div>
          ))}
        </div>

        <div className="key-insights">
          <h3>핵심 인사이트</h3>
          <div className="insights-grid">
            <div className="insight">
              <div className="insight-icon">🏆</div>
              <div className="insight-content">
                <h4>최고 성과 전략</h4>
                <p>USDT Only 전략이 +0.89%로 가장 우수한 성과를 기록했습니다.</p>
              </div>
            </div>
            
            <div className="insight">
              <div className="insight-icon">📊</div>
              <div className="insight-content">
                <h4>단일 자산 우위</h4>
                <p>복합 자산 전략보다 단일 자산 전략이 더 나은 성과를 보였습니다.</p>
              </div>
            </div>
            
            <div className="insight">
              <div className="insight-icon">⚠️</div>
              <div className="insight-content">
                <h4>리스크 관리 중요</h4>
                <p>BTC Only 전략은 -4.46%로 가장 높은 손실을 기록했습니다.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default PerformanceOverview;