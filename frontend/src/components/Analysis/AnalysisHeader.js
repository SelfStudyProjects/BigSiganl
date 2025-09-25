import React from 'react';

const AnalysisHeader = () => {
  return (
    <section style={{ padding: '3rem 0', backgroundColor: '#f8f9fa', textAlign: 'center' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1rem' }}>
        <h1 style={{ fontSize: '2.5rem', marginBottom: '1rem', color: '#333' }}>
          백테스팅 분석 결과
        </h1>
        <p style={{ fontSize: '1.1rem', color: '#666', maxWidth: '600px', margin: '0 auto' }}>
          2024년 7-9월 BigSignal AI 시그널 814건의 실제 거래 데이터를 기반으로 한 
          포트폴리오 성과 분석입니다.
        </p>
      </div>
    </section>
  );
};

export default AnalysisHeader;