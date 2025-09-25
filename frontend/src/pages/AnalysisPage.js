// src/pages/AnalysisPage.js
import React from 'react';
import AnalysisHeader from '../components/Analysis/AnalysisHeader';
import PerformanceOverview from '../components/Analysis/PerformanceOverview';
import InteractiveCharts from '../components/Analysis/InteractiveCharts';
import DetailedResults from '../components/Analysis/DetailedResults';
import Disclaimer from '../components/Analysis/Disclaimer';
import './AnalysisPage.css';

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