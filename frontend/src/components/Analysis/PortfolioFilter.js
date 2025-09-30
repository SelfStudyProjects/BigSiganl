import React from 'react';
import './PortfolioFilter.css';

const PortfolioFilter = ({ onFilterChange }) => {
  const [filters, setFilters] = React.useState({
    sortBy: 'return', // return, name, value
    showNegative: true,
    assetType: 'all' // all, single, mixed
  });

  const handleChange = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <div className="portfolio-filter">
      <div className="filter-group">
        <label>정렬 기준:</label>
        <select 
          value={filters.sortBy}
          onChange={(e) => handleChange('sortBy', e.target.value)}
        >
          <option value="return">수익률순</option>
          <option value="name">이름순</option>
          <option value="value">현재가치순</option>
        </select>
      </div>

      <div className="filter-group">
        <label>포트폴리오 유형:</label>
        <select 
          value={filters.assetType}
          onChange={(e) => handleChange('assetType', e.target.value)}
        >
          <option value="all">전체</option>
          <option value="single">단일 자산</option>
          <option value="mixed">복합 자산</option>
        </select>
      </div>

      <div className="filter-group">
        <label>
          <input 
            type="checkbox"
            checked={filters.showNegative}
            onChange={(e) => handleChange('showNegative', e.target.checked)}
          />
          마이너스 수익 포함
        </label>
      </div>
    </div>
  );
};

export default PortfolioFilter;