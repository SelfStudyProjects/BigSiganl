// src/components/Landing/Hero.js
import React from 'react';
import { Link } from 'react-router-dom';
import './Hero.css';

const Hero = () => {
  return (
    <section className="hero">
      <div className="hero-bg">
        <div className="notification-banner">
          <span className="notification-icon">🔥</span>
          <span className="notification-text">Get Notified</span>
          <a 
            href="https://t.me/bigsignal_ai" 
            target="_blank" 
            rel="noopener noreferrer"
            className="notification-button"
          >
            Join Our Telegram
          </a>
        </div>
      </div>
      
      <div className="hero-content">
        <div className="container">
          <h1 className="hero-title">
            AI로 만나는 USDT 자동 트레이딩
          </h1>
          
          <p className="hero-description">
            끊임없이 변동하는 USDT 시장에서 매매 타이밍을 놓치지 않으려면, 시세를 24시간 모니터링하고 분석해야 합니다. 
            그러나 시장 변동성이 워낙 높아, 매 순간 스스로 전략을 세우기에는 큰 부담이 따릅니다. 
            BigSignal은 이러한 문제를 해결하기 위해 고성능 NVIDIA GPU와 인공지능 알고리즘을 결합해, 
            누구나 손쉽게 사용할 수 있는 USDT 자동 매매 서비스를 제공합니다.
          </p>
        </div>
      </div>
    </section>
  );
};

export default Hero;