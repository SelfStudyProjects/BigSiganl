// src/components/Landing/UsageGuide.js
import React from 'react';
import './UsageGuide.css';

const UsageGuide = () => {
  return (
    <section className="usage-guide">
      <div className="container">
        <h2>사용 방법과 유의사항</h2>
        
        <div className="usage-steps">
          <div className="step">
            <div className="step-number">1</div>
            <div className="step-content">
              <h3>텔레그램 알림 수신 후 직접 매매</h3>
              <p>
                텔레그램 메시지로 BigSignal의 매매 신호를 받아보실 수 있습니다. 
                신호를 참고하여 투자자가 직접 거래소에서 매매를 진행하시면 됩니다. 
                전량 매수·매도는 리스크가 높을 수 있으므로 텔레그램 메시지에 제공되는 
                매수·매도 비율 정보를 활용해 신중하게 투자하시길 권장합니다. 
                이 방식은 본인 판단에 따라 유연하게 투자할 수 있다는 장점이 있습니다. 
                텔레그램 링크는 홈페이지 상단에서 확인하실 수 있습니다.
              </p>
            </div>
          </div>

          <div className="step">
            <div className="step-number">2</div>
            <div className="step-content">
              <h3>마음에 드시면 자동 매매로!</h3>
              <p>
                텔레그램 메시지를 이용한 직접 매매를 충분히 테스트해 보신 뒤, 
                자동 매매가 필요하다고 느끼시면, 빗썸 API 키를 BigSignal에 연동해 
                AI가 24시간 자동으로 매수·매도를 진행하도록 전환할 수 있습니다. 
                (연결 원하시는 분은 donghoonlee@hanyang.ac.kr 으로 연락해주시면, 
                연결 방법을 안내해드리겠습니다.)
              </p>
            </div>
          </div>

          <div className="step">
            <div className="step-number">3</div>
            <div className="step-content">
              <h3>리스크 주의</h3>
              <p>
                암호화폐 시장의 특성상 손실 위험이 늘 존재하며, AI 예측도 100% 성공을 보장할 수는 없습니다. 
                과거 성과가 미래 수익률을 보장하지 않으므로, 반드시 본인의 투자 성향과 
                리스크 허용 범위를 고려하시기 바랍니다.
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
};

export default UsageGuide;