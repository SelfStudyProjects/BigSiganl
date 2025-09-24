const TrustSection = () => (
  <section className="trust-section">
    <div className="container">
      <h3>투명한 성과 공개</h3>
      <p>실제 AI 시그널 814건 백테스팅 결과</p>
      <div className="trust-stats">
        <div className="stat">
          <span className="number">814</span>
          <span className="label">실제 거래</span>
        </div>
        <div className="stat">
          <span className="number">59일</span>
          <span className="label">분석 기간</span>
        </div>
      </div>
      <Link to="/analysis" className="btn-secondary">
        상세 분석 결과 보기 →
      </Link>
    </div>
  </section>
);