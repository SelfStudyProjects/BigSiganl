import React, { useState } from 'react';
import { FaTelegramPlane } from 'react-icons/fa';

const sectionStyle = {
  maxWidth: '1100px',
  margin: '60px auto 0 auto',
  padding: '0 20px',
  lineHeight: 1.7,
  color: '#222',
  fontFamily: 'Noto Sans KR, sans-serif'
};
const titleStyle = {
  textAlign: 'center',
  fontWeight: 700,
  fontSize: '2rem',
  margin: '60px 0 30px 0'
};
const subtitleStyle = {
  textAlign: 'center',
  fontWeight: 700,
  fontSize: '1.3rem',
  margin: '50px 0 30px 0'
};
const listStyle = {
  margin: '20px 0 40px 0',
  paddingLeft: '20px'
};
const emailStyle = { color: '#b00', textDecoration: 'underline', wordBreak: 'break-all' };
const linkStyle = { color: '#1976d2', textDecoration: 'underline', cursor: 'pointer' };

const topBarStyle = {
  width: '100%',
  background: '#e9cccc',
  minHeight: 80,
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  padding: '0 8vw',
  boxSizing: 'border-box',
};
const logoStyle = {
  fontWeight: 700,
  fontSize: '2rem',
  color: '#b86a6a',
  fontFamily: 'serif',
  letterSpacing: 1,
  flex: 1,
  textAlign: 'left',
  pointerEvents: 'none',
};
const centerBoxStyle = {
  flex: 1,
    display: 'flex',
    justifyContent: 'center',
  alignItems: 'center',
  gap: 20,
};
const rightBoxStyle = {
  flex: 1,
};
const notifyStyle = {
  display: 'flex',
  alignItems: 'center',
  fontSize: '1.15rem',
  marginRight: 10,
  color: '#222',
  fontWeight: 400,
  background: 'none',
  border: 'none',
  cursor: 'default',
  padding: '8px 16px',
  borderRadius: 6,
  transition: 'background 0.2s',
  pointerEvents: 'none',
};
const notifyHoverStyle = {
  background: '#f5e2e2',
};
const telegramBtnStyle = {
  fontSize: '1.2rem',
  padding: '8px 32px',
  border: '1.5px solid #222',
  borderRadius: 6,
  background: 'none',
  cursor: 'pointer',
  fontWeight: 400,
  transition: 'background 0.2s',
};

function App() {
  const [notifyHover, setNotifyHover] = useState(false);
  const [lang, setLang] = useState('ko');

  // 한글/영문 텍스트 정의
  const text = {
    ko: {
      title: "AI로 만나는 USDT 자동 트레이딩",
      desc1: "끊임없이 변동하는 USDT 시장에서 매매 타이밍을 놓치지 않으려면, 시세를 24시간 모니터링하고 분석해야 합니다.",
      desc2: "그러나 시장 변동성이 워낙 높아, 매 순간 스스로 전략을 세우기에는 큰 부담이 따릅니다.",
      desc3: "BigSignal은 이러한 문제를 해결하기 위해 고성능 NVIDIA GPU와 인공지능 알고리즘을 결합해,",
      desc4: "누구나 손쉽게 사용할 수 있는 USDT 자동 매매 서비스를 제공합니다.",
      subtitle1: "사용 방법과 유의사항",
      how1: "텔레그램 알림 수신 후 직접 매매",
      how1_1: "텔레그램 메시지로 BigSignal의 매매 신호를 받아보실 수 있습니다. 신호를 참고하여 투자자가 직접 거래소에서 매매를 진행하시면 됩니다.",
      how1_2: "전량 매수·매도는 리스크가 높을 수 있으므로 텔레그램 메시지에 제공되는 매수·매도 비율 정보를 활용해 신중하게 투자하시길 권장합니다.",
      how1_3: "이 방식은 본인 판단에 따라 유연하게 투자할 수 있다는 장점이 있습니다. 텔레그램 링크는 홈페이지 상단에서 확인하실 수 있습니다.",
      how2: "마음에 드시면 자동 매매로!",
      how2_1: "텔레그램 메시지를 이용한 직접 매매를 충분히 테스트해 보신 뒤, 자동 매매가 필요하다고 느끼시면, 빗썸 API 키를 BigSignal에 연동해 AI가 24시간 자동으로 매수·매도를 진행하도록 전환할 수 있습니다.",
      how2_2: "(연결 원하시는 분은 ",
      how2_3: " 으로 연락해주시면, 연결 방법을 안내해드리겠습니다.)",
      how3: "리스크 주의",
      how3_1: "암호화폐 시장의 특성상 손실 위험이 늘 존재하며, AI 예측도 100% 성공을 보장할 수는 없습니다.",
      how3_2: "과거 성과가 미래 수익률을 보장하지 않으므로, 반드시 본인의 투자 성향과 리스크 허용 범위를 고려하시기 바랍니다.",
      subtitle2: "왜 BigSignal을 사용해야 하나요?",
      why1: "빗썸 USDT·USDC 거래 수수료 무료",
      why1_1: "빗썸에서는 USDT·USDC 거래 수수료가 0원이므로, 매매 시 추가 비용 부담 없이 적은 변동에도 수익 실현이 가능합니다. 수수료가 없어 빈번한 거래 전략도 효율적으로 운용할 수 있어, 다양한 투자 기회를 놓치지 않을 수 있습니다.",
      why2: "USDT 시장의 높은 변동성으로 잠재 수익 극대화",
      why2_1: "USDT는 상대적으로 달러보다 변동성이 높아, 전통적인 FX(외환) 투자 대비 더 큰 수익을 노릴 수 있습니다. BigSignal을 통해 이러한 높은 변동성이 만들어내는 기회를 효율적으로 포착하여, 수익을 극대화할 수 있습니다.",
      why3: "독자 개발 AI 예측 모델",
      why3_1: "BigSignal은 자동화 기계학습 기반의 독점 시계열 예측 기술을 활용해, 향후 USDT 시세 변동을 분석하고 매매 신호를 BUY, SELL, HOLD로 구분합니다. 내부 로직은 보안상 비공개이지만, 고성능 NVIDIA GPU로 방대한 데이터를 처리해 정교한 예측이 가능하다는 점이 핵심입니다.",
      why4: "다양한 기술적 지표 반영",
      why4_1: "ATR, RSI, MACD, 볼린저 밴드 등 주요 지표를 종합적으로 분석해, 단순한 가격 예측을 넘어 시장 심리, 추세, 변동 폭 등을 다각도로 파악합니다. BigSignal의 독점 예측 모델과 각종 지표가 상호 보완적으로 작동하여 안정적인 의사결정을 지원합니다.",
      why5: "백테스트와 최적화",
      why5_1: "백테스트를 통과해 검증된 알고리즘은 Bayesian Optimization 등 진보된 최적화 기법을 활용해 매개변수를 지속적으로 개선함으로써 독자적 모델의 정확도를 끌어올립니다. 또한 시간이 흐르면서 데이터 학습이 진행될수록, 알고리즘 성능 역시 꾸준히 향상됩니다.",
      why6: "리스크 관리 기능",
      why6_1: "BigSignal은 분할매수·분할매도 방식을 통해 시장 변동성에 유연하게 대응하도록 설계되었습니다. 단일 시점에 대규모 자금을 투입하거나 청산하지 않고, 여러 차례에 걸쳐 매수·매도를 나누어 진행함으로써 리스크를 분산할 수 있습니다. 또한 분할 매매 비율에 대한 정보를 제공하여, 투자자가 적절한 매매 전략을 손쉽게 수립하고 조정할 수 있도록 돕습니다.",
      subtitle3: "BigSignal이 제공하는 가치",
      value1: "고성능 AI 엔진",
      value1_1: "고성능 NVIDIA GPU 기반의 빠른 계산력으로 대규모 데이터를 분석해, 시장 흐름을 놓치지 않는 매매를 지원합니다.",
      value2: "편의성과 전문성의 조화",
      value2_1: "종일 시세를 모니터링할 필요 없이, 자동으로 최적의 매매 시점을 잡아주어 효율적인 투자 시간을 제공합니다.",
      value3: "지금 BigSignal과 함께, 새로운 투자 경험을 누려보세요!",
      value4: "인공지능 트레이딩은 이제 전문가만의 전유물이 아닙니다. BigSignal과 함께라면, 누구나 고성능 AI의 도움을 받아 부담없이 암호화폐 시장에 참여할 수 있습니다.",
      value5: "빠르고 정확한 빅데이터 분석, 사용자 중심의 매매 전략, 투명한 정보 제공까지 — BigSignal이 여러분의 투자 여정을 든든하게 지원합니다.",
      value6: "BigSignal은 USDT뿐만 아니라 BTC와 DOGE에 대한 자동 매매 알고리즘도 현재 베타 테스트 중입니다.",
      value7: "관심 있는 분들은 홈페이지 하단에 제공된 텔레그램 링크를 통해 BTC 및 DOGE 시그널을 받아보실 수 있습니다.",
      gotQuestions: '궁금한 점이 있으신가요?',
      email: 'jinyeonge1234@naver.com',
      betaBtc: '비트코인 베타 테스트',
      betaDoge: '도지코인 베타 테스트',
      telegram: '텔레그램',
      korean: '한국어',
      english: 'English',
    },
    en: {
      title: "AI-powered USDT Auto Trading",
      desc1: "To avoid missing the timing in the ever-changing USDT market, you need to monitor and analyze prices 24/7.",
      desc2: "However, due to the high volatility, it's a big burden to set your own strategy every moment.",
      desc3: "BigSignal solves this problem by combining high-performance NVIDIA GPUs and AI algorithms,",
      desc4: "providing an easy-to-use USDT auto trading service for everyone.",
      subtitle1: "How to Use & Precautions",
      how1: "Manual Trading After Telegram Alerts",
      how1_1: "You can receive BigSignal's trading signals via Telegram messages. Refer to the signals and trade directly on the exchange.",
      how1_2: "Full buy/sell can be risky, so we recommend using the buy/sell ratio information provided in the Telegram messages for careful investment.",
      how1_3: "This method allows flexible investment at your own discretion. The Telegram link is available at the top of the homepage.",
      how2: "If Satisfied, Switch to Auto Trading!",
      how2_1: "After thoroughly testing manual trading via Telegram, if you feel the need for auto trading, you can link your Bithumb API key to BigSignal and let the AI trade 24/7 automatically.",
      how2_2: "(If you want to connect, contact ",
      how2_3: " and we will guide you through the process.)",
      how3: "Risk Warning",
      how3_1: "Due to the nature of the cryptocurrency market, there is always a risk of loss, and AI predictions cannot guarantee 100% success.",
      how3_2: "Past performance does not guarantee future returns, so always consider your own investment style and risk tolerance.",
      subtitle2: "Why Use BigSignal?",
      why1: "Zero Bithumb USDT·USDC Trading Fees",
      why1_1: "Bithumb offers zero trading fees for USDT·USDC, so you can realize profits even with small fluctuations. With no fees, you can efficiently operate frequent trading strategies and seize various investment opportunities.",
      why2: "Maximize Potential Profits with USDT Volatility",
      why2_1: "USDT is more volatile than the dollar, so you can aim for higher profits compared to traditional FX investments. BigSignal helps you efficiently capture these opportunities created by high volatility.",
      why3: "Proprietary AI Prediction Model",
      why3_1: "BigSignal uses a proprietary time-series prediction technology based on automated machine learning to analyze future USDT price movements and classify trading signals as BUY, SELL, or HOLD. The internal logic is confidential for security reasons, but high-performance NVIDIA GPUs process vast amounts of data for precise predictions.",
      why4: "Incorporating Various Technical Indicators",
      why4_1: "We comprehensively analyze major indicators such as ATR, RSI, MACD, and Bollinger Bands to understand not only price predictions but also market sentiment, trends, and volatility. BigSignal's proprietary prediction model and various indicators work complementarily to support stable decision-making.",
      why5: "Backtesting & Optimization",
      why5_1: "Algorithms that pass backtesting are continuously improved using advanced optimization techniques such as Bayesian Optimization, increasing the accuracy of our proprietary model. As more data is learned over time, algorithm performance also steadily improves.",
      why6: "Risk Management Features",
      why6_1: "BigSignal is designed to flexibly respond to market volatility through split buying and selling. By dividing buy/sell orders into multiple steps instead of investing or liquidating large amounts at once, you can diversify risk. We also provide information on split trading ratios to help investors easily establish and adjust their trading strategies.",
      subtitle3: "The Value BigSignal Provides",
      value1: "High-Performance AI Engine",
      value1_1: "With high-performance NVIDIA GPUs, we analyze large-scale data quickly to support trading that doesn't miss market trends.",
      value2: "Convenience Meets Expertise",
      value2_1: "No need to monitor prices all day—our AI automatically finds the optimal trading timing, giving you efficient investment time.",
      value3: "Experience a new way of investing with BigSignal!",
      value4: "AI trading is no longer exclusive to experts. With BigSignal, anyone can participate in the crypto market with the help of high-performance AI.",
      value5: "Fast and accurate big data analysis, user-centered trading strategies, and transparent information—BigSignal supports your investment journey.",
      value6: "BigSignal is currently beta testing auto trading algorithms for not only USDT but also BTC and DOGE.",
      value7: "If you're interested, you can receive BTC and DOGE signals via the Telegram link at the bottom of the homepage.",
      gotQuestions: 'Got Questions?',
      email: 'jinyeonge1234@naver.com',
      betaBtc: 'Beta Test with Bitcoin',
      betaDoge: 'Beta Test with Dogecoin',
      telegram: 'Telegram',
      korean: 'Korean',
      english: 'English',
    },
  };

  return (
    <div style={{ background: '#fff', minHeight: '100vh', paddingBottom: 40 }}>
      {/* 상단 바 */}
      <div style={topBarStyle}>
        <span style={logoStyle}>Big</span>
        <div style={centerBoxStyle}>
          <button
            style={notifyStyle}
          >
            <span role="img" aria-label="fire" style={{marginRight: 4}}>🔥</span>Get Notified
          </button>
          <button
            style={telegramBtnStyle}
            onClick={() => window.open('https://t.me/bigsignal_ai', '_blank')}
          >
            Join Our Telegram
          </button>
        </div>
        <div style={rightBoxStyle}></div>
      </div>
      {/* 1. AI로 만나는 USDT 자동 트레이딩 */}
      <section style={sectionStyle}>
        <div style={titleStyle}>{text[lang].title}</div>
        <div style={{ textAlign: 'center', marginBottom: 40 }}>
          {text[lang].desc1}<br />
          {text[lang].desc2}<br />
          {text[lang].desc3}<br />
          {text[lang].desc4}
        </div>
      </section>

      {/* 2. 사용 방법과 유의사항 */}
      <section style={sectionStyle}>
        <div style={subtitleStyle}>{text[lang].subtitle1}</div>
        <ol style={listStyle}>
          <li>
            <b>{text[lang].how1}</b>
            <ul>
              <li>{text[lang].how1_1}</li>
              <li>{text[lang].how1_2}</li>
              <li>{text[lang].how1_3}</li>
            </ul>
          </li>
          <li>
            <b>{text[lang].how2}</b>
            <ul>
              <li>{text[lang].how2_1}</li>
              <li>
                {text[lang].how2_2}<span style={emailStyle}>{text[lang].email}</span>{text[lang].how2_3}
              </li>
            </ul>
          </li>
          <li>
            <b>{text[lang].how3}</b>
            <ul>
              <li>{text[lang].how3_1}</li>
              <li>{text[lang].how3_2}</li>
            </ul>
          </li>
        </ol>
      </section>

      {/* 3. 왜 BigSignal을 사용해야 하나요? */}
      <section style={sectionStyle}>
        <div style={subtitleStyle}>{text[lang].subtitle2}</div>
        <ol style={listStyle}>
          <li>
            <b>{text[lang].why1}</b>
            <div>{text[lang].why1_1}</div>
          </li>
          <li>
            <b>{text[lang].why2}</b>
            <div>{text[lang].why2_1}</div>
          </li>
          <li>
            <b>{text[lang].why3}</b>
            <div>{text[lang].why3_1}</div>
          </li>
          <li>
            <b>{text[lang].why4}</b>
            <div>{text[lang].why4_1}</div>
          </li>
          <li>
            <b>{text[lang].why5}</b>
            <div>{text[lang].why5_1}</div>
          </li>
          <li>
            <b>{text[lang].why6}</b>
            <div>{text[lang].why6_1}</div>
          </li>
        </ol>
      </section>

      {/* 4. BigSignal이 제공하는 가치 */}
      <section style={sectionStyle}>
        <div style={subtitleStyle}>{text[lang].subtitle3}</div>
        <ol style={listStyle}>
          <li>
            <b>{text[lang].value1}</b>
            <div>{text[lang].value1_1}</div>
          </li>
          <li>
            <b>{text[lang].value2}</b>
            <div>{text[lang].value2_1}</div>
          </li>
        </ol>
        <div style={{ margin: '40px 0', textAlign: 'center', fontWeight: 500 }}>
          {text[lang].value3}
        </div>
        <div style={{ margin: '0 0 30px 0', textAlign: 'center' }}>
          {text[lang].value4}<br />
          {text[lang].value5}<br />
          {text[lang].value6}<br />
          {text[lang].value7}
        </div>
        <div style={{ textAlign: 'center', fontSize: '1rem', marginBottom: 30 }}>
          {text[lang].gotQuestions} <a href={`mailto:${text[lang].email}`} style={emailStyle}>{text[lang].email}</a><br />
          <a href="https://t.me/bigsignal_btc" target="_blank" rel="noopener noreferrer" style={linkStyle}>{text[lang].betaBtc}</a><br />
          <a href="https://t.me/bigsignal_doge" target="_blank" rel="noopener noreferrer" style={linkStyle}>{text[lang].betaDoge}</a><br />
        </div>
        {/* 텔레그램 원형 버튼 */}
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', marginBottom: 30 }}>
          <button
            onClick={() => window.open('https://t.me/bigsignal_ai', '_blank')}
            style={{
              width: 48, height: 48, borderRadius: '50%', background: '#63aee3', border: 'none', display: 'flex', alignItems: 'center', justifyContent: 'center', cursor: 'pointer', boxShadow: '0 2px 8px #e0e0e0',
            }}
            aria-label="Telegram"
          >
            <FaTelegramPlane color="#fff" size={28} />
          </button>
        </div>
        {/* 언어 전환 버튼 */}
        <div style={{ display: 'flex', justifyContent: 'center', gap: 30 }}>
          <button onClick={() => setLang('ko')} style={{ background: 'none', border: 'none', color: lang === 'ko' ? '#222' : '#888', fontWeight: lang === 'ko' ? 700 : 400, fontSize: '1rem', cursor: 'pointer', textDecoration: 'underline' }}>{text[lang].korean}</button>
          <button onClick={() => setLang('en')} style={{ background: 'none', border: 'none', color: lang === 'en' ? '#222' : '#888', fontWeight: lang === 'en' ? 700 : 400, fontSize: '1rem', cursor: 'pointer', textDecoration: 'underline' }}>{text[lang].english}</button>
        </div>
      </section>
    </div>
  );
}

export default App;