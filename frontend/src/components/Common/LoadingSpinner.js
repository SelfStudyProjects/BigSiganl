import React from 'react';
import './LoadingSpinner.css';

const LoadingSpinner = ({ message = '데이터를 불러오는 중...' }) => {
  return (
    <div className="loading-container">
      <div className="spinner"></div>
      <p>{message}</p>
    </div>
  );
};

export default LoadingSpinner;