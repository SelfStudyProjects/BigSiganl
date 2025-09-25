// src/components/Landing/TrustSection.js
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../../services/api';
import './TrustSection.css';

const TrustSection = () => {
  const [summaryData, setSummaryData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummaryData = async () => {
      try {
        const data = await api.getDashboardData();
        setSummaryData(data);
      } catch (error) {
        console.error('요약 데이터 로드 실패:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchSummaryData();
  }, []);

  if (loading) {
    return (
      <section className="trust-section">
        <div className="container">
          <div className="loading">데이터 로딩 중...</div>
        </div>
      </section>
    );
  }

  return (
    <section className="trust-section">
      <div className="container">
        <div className="trust-header">
          <h2>투명한 성과 공개</h2>
          <p className="trust-subtitle">
            우리는 성공과 실패를 모두 공개합니다. 실제 AI 시그널 기반 백테스팅 결과를 확인하세요.
          </p>
        </div>

        <div className="trust-stats">
          <div className="stat-grid">
            <div className="stat-card">
              <div className="stat-number">814</div>
              <div className="stat-label">실제 거래 시그널</div>
              <div className="stat-period">2024.07-09</div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number">59</div>
              <div className="stat-label">분석 기간 (일)</div>
              <div className="stat-period">연속 모니터링</div>
            </div>
            
            <div className="stat-card highlight">
              <div className="stat-number">7</div>
              <div className="stat-label">테스트 전략</div>
              <div className="stat-period">다양한 포트폴리오</div>
            </div>
            
            <div className="stat-card">
              <div className="stat-number best">+0.89%</div>
              <div className="stat-label">최고 성과</div>
              <div className="stat-period">USDT Only</div>
            </div>
          </div>
        </div>

        <div className="trust-message">
          <div className="message-content">
            <h3>왜 실패 결과도 공개하나요?</h3>
            <p>
              투자에는 항상 리스크가 따르며, AI 예측도 100% 정확할 수 없습니다. 
              우리는 모든 백테스팅 결과를 투명하게 공개하여, 
              여러분이 충분한 정보를 바탕으로 현명한 투자 결정을 내리실 수 있도록 돕습니다.
            </p>
          </div>
        </div>

        <div className="trust-actions">
          <Link to="/analysis" className="btn-primary">
            상세 분석 결과 보기
          </Link>
          <a 
            href="https://t.me/bigsignal_ai" 
            target="_blank" 
            rel="noopener noreferrer"
            className="btn-secondary"
          >
            텔레그램 가입하기
          </a>
        </div>
      </div>
    </section>
  );
};

export default TrustSection;