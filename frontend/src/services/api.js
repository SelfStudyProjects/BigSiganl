// API Base URL 설정 (환경변수 사용)
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// 포트폴리오 성과 데이터
export const getPerformanceData = async () => {
  const response = await fetch(`${API_BASE_URL}/api/analysis/performance/`);
  if (!response.ok) throw new Error('Failed to fetch performance data');
  return response.json();
};

// 대시보드 요약 데이터
export const getDashboardData = async () => {
  const response = await fetch(`${API_BASE_URL}/api/analysis/dashboard-summary/`);
  if (!response.ok) throw new Error('Failed to fetch dashboard data');
  return response.json();
};

// 차트 이미지 URL 생성
export const getChartUrl = (chartName) => {
  return `${API_BASE_URL}/api/analysis/charts/${chartName}/`;
};

// 거래 데이터 (기존 함수 - 있으면 유지, 없으면 추가)
export const getTrades = async () => {
  const response = await fetch(`${API_BASE_URL}/api/trades/`);
  if (!response.ok) throw new Error('Failed to fetch trades');
  return response.json();
};

// 포트폴리오 목록 (기존 함수 - 있으면 유지, 없으면 추가)
export const getPortfolios = async () => {
  const response = await fetch(`${API_BASE_URL}/api/portfolios/`);
  if (!response.ok) throw new Error('Failed to fetch portfolios');
  return response.json();
};

// 타임라인 데이터 (추가)
export const getTimelineData = async (portfolio = 'All_Assets', days = 30) => {
  const response = await fetch(`${API_BASE_URL}/api/analysis/timeline/?portfolio=${portfolio}&days=${days}`);
  if (!response.ok) throw new Error('Failed to fetch timeline data');
  return response.json();
};

// 거래 통계 (추가)
export const getTradingStats = async () => {
  const response = await fetch(`${API_BASE_URL}/api/analysis/trading-stats/`);
  if (!response.ok) throw new Error('Failed to fetch trading stats');
  return response.json();
};

// 리스크 메트릭 (추가)
export const getRiskMetrics = async () => {
  const response = await fetch(`${API_BASE_URL}/api/analysis/risk-metrics/`);
  if (!response.ok) throw new Error('Failed to fetch risk metrics');
  return response.json();
};