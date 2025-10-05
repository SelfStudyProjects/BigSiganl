// src/pages/AnalysisPage.js
import React from 'react';
import AnalysisHeader from '../components/Analysis/AnalysisHeader';
import PerformanceOverview from '../components/Analysis/PerformanceOverview';
import InteractiveCharts from '../components/Analysis/InteractiveCharts';
import DetailedResults from '../components/Analysis/DetailedResults';
import Disclaimer from '../components/Analysis/Disclaimer';
import './AnalysisPage.css';
import { getPerformanceData, getDashboardData } from '../services/api';

// useEffect에서 API 호출 확인
useEffect(() => {
  const fetchData = async () => {
    try {
      const data = await getPerformanceData();
      console.log('Performance data:', data);
      // 데이터 상태 업데이트
    } catch (error) {
      console.error('API Error:', error);
    }
  };
  fetchData();
}, []);

const AnalysisPage = () => {
  return (
    <div className="analysis-page">
      <AnalysisHeader />
      <PerformanceOverview />
      <InteractiveCharts />
      <DetailedResults />
      <Disclaimer />
    </div>
  );
};

export default AnalysisPage;