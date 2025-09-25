import React from 'react';

const Features = () => {
  const features = [
    {
      title: "빗썸 USDT·USDC 거래 수수료 무료",
      description: "매매 시 추가 비용 부담 없이 적은 변동에도 수익 실현이 가능합니다."
    },
    {
      title: "USDT 시장의 높은 변동성으로 잠재 수익 극대화",
      description: "전통적인 FX(외환) 투자 대비 더 큰 수익을 노릴 수 있습니다."
    },
    {
      title: "독자 개발 AI 예측 모델",
      description: "고성능 NVIDIA GPU로 방대한 데이터를 처리해 정교한 예측이 가능합니다."
    }
  ];

  return (
    <section style={{ padding: '4rem 0', backgroundColor: '#f8f9fa' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '0 1rem' }}>
        <h2 style={{ textAlign: 'center', fontSize: '2.5rem', marginBottom: '3rem', color: '#333' }}>
          왜 BigSignal을 사용해야 하나요?
        </h2>
        
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem' }}>
          {features.map((feature, index) => (
            <div key={index} style={{ 
              background: 'white', 
              padding: '2rem', 
              borderRadius: '0.5rem',
              boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
            }}>
              <h3 style={{ marginBottom: '1rem', color: '#333' }}>
                {index + 1}. {feature.title}
              </h3>
              <p style={{ color: '#666', lineHeight: 1.6 }}>
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;