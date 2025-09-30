import React from 'react';

const ExportButton = ({ portfolios }) => {
  const exportToCSV = () => {
    const headers = ['포트폴리오,초기투자,현재가치,손익,수익률'];
    
    const rows = portfolios.map(p => 
      `${p.display_name},${p.initial_value},${p.final_value},${p.profit_loss},${p.total_return}`
    );
    
    const csv = [headers, ...rows].join('\n');
    const blob = new Blob(['\uFEFF' + csv], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `portfolio_report_${new Date().toISOString().split('T')[0]}.csv`;
    link.click();
  };

  return (
    <button className="btn-secondary" onClick={exportToCSV}>
      📥 데이터 내보내기 (CSV)
    </button>
  );
};

export default ExportButton;