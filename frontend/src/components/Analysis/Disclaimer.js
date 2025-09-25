import React from 'react';

const Disclaimer = () => {
  return (
    <section style={{ padding: '2rem 0', backgroundColor: '#f8f9fa' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1rem' }}>
        <div style={{ 
          background: '#fff3cd', 
          border: '1px solid #ffeaa7', 
          borderRadius: '0.5rem', 
          padding: '2rem',
          display: 'flex',
          alignItems: 'flex-start',
          gap: '1rem'
        }}>
          <div style={{ fontSize: '2rem' }}>⚠️</div>
          <div>
            <h3 style={{ marginBottom: '1rem', color: '#856404' }}>투자 위험 고지</h3>
            <p style={{ color: '#856404', lineHeight: 1.6, marginBottom: '1rem' }}>
              위 분석 결과는 과거 데이터 기반 백테스팅이며, 미래 수익을 보장하지 않습니다.
            </p>
            <p style={{ color: '#856404', lineHeight: 1.6 }}>
              암호화폐 투자는 높은 변동성과 손실 위험을 수반하므로, 
              반드시 본인의 투자 성향과 리스크 허용 범위를 고려하여 신중히 결정하시기 바랍니다.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
};

export default Disclaimer;