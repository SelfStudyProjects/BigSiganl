// src/pages/AnalysisPage.js
import React, { useEffect, useState } from 'react';
import AnalysisHeader from '../components/Analysis/AnalysisHeader';
import PerformanceOverview from '../components/Analysis/PerformanceOverview';
import InteractiveCharts from '../components/Analysis/InteractiveCharts';
import DetailedResults from '../components/Analysis/DetailedResults';
import Disclaimer from '../components/Analysis/Disclaimer';
import './AnalysisPage.css';
import { getPerformanceData, getDashboardData } from '../services/api';

const AnalysisPage = () => {
  const [performanceData, setPerformanceData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const data = await getPerformanceData();
        console.log('Performance data:', data);
        setPerformanceData(data);
      } catch (error) {
        console.error('API Error:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

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