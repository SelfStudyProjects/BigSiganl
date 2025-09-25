import React from 'react';

const DetailedResults = () => {
  return (
    <section style={{ padding: '2rem 0' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1rem' }}>
        <h2 style={{ marginBottom: '2rem' }}>상세 분석 결과</h2>
        <div style={{ background: 'white', padding: '2rem', borderRadius: '0.5rem', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
          <p style={{ color: '#666', lineHeight: 1.6 }}>
            상세한 백테스팅 결과와 전략별 분석 데이터가 여기에 표시됩니다. 
            추후 더 구체적인 분석 지표와 차트가 추가될 예정입니다.
          </p>
        </div>
      </div>
    </section>
  );
};

export default DetailedResults;