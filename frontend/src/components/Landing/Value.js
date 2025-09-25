import React from 'react';

const Value = () => {
  return (
    <section style={{ padding: '4rem 0', backgroundColor: 'white' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1rem' }}>
        <h2 style={{ textAlign: 'center', fontSize: '2.5rem', marginBottom: '3rem', color: '#333' }}>
          BigSignal이 제공하는 가치
        </h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(400px, 1fr))', gap: '3rem' }}>
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🚀</div>
            <h3 style={{ marginBottom: '1rem', color: '#333' }}>고성능 AI 엔진</h3>
            <p style={{ color: '#666', lineHeight: 1.6 }}>
              고성능 NVIDIA GPU 기반의 빠른 계산력으로 대규모 데이터를 분석해, 
              시장 흐름을 놓치지 않는 매매를 지원합니다.
            </p>
          </div>
          
          <div style={{ textAlign: 'center' }}>
            <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>⚡</div>
            <h3 style={{ marginBottom: '1rem', color: '#333' }}>편의성과 전문성의 조화</h3>
            <p style={{ color: '#666', lineHeight: 1.6 }}>
              종일 시세를 모니터링할 필요 없이, 자동으로 최적의 매매 시점을 잡아주어 
              효율적인 투자 시간을 제공합니다.
            </p>
          </div>
        </div>
        
        <div style={{ textAlign: 'center', marginTop: '3rem' }}>
          <h3 style={{ fontSize: '1.5rem', marginBottom: '1rem', color: '#333' }}>
            지금 BigSignal과 함께, 새로운 투자 경험을 누려보세요!
          </h3>
          <p style={{ color: '#666', lineHeight: 1.6, maxWidth: '800px', margin: '0 auto' }}>
            인공지능 트레이딩은 이제 전문가만의 전유물이 아닙니다. BigSignal과 함께라면, 
            누구나 고성능 AI의 도움을 받아 부담없이 암호화폐 시장에 참여할 수 있습니다.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Value;