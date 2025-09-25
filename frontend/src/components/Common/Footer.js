import React from 'react';

const Footer = () => {
  return (
    <footer style={{ padding: '2rem', backgroundColor: '#343a40', color: 'white', textAlign: 'center' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto' }}>
        <p>© 2024 BigSignal. AI 기반 USDT 자동 트레이딩</p>
        <p style={{ marginTop: '0.5rem', fontSize: '0.9rem', opacity: 0.8 }}>
          투자에는 리스크가 따르며, 과거 성과가 미래 수익을 보장하지 않습니다.
        </p>
      </div>
    </footer>
  );
};

export default Footer;