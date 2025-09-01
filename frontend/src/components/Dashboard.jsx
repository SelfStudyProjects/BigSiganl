import React from 'react';
import PortfolioChart from './PortfolioChart';
import PortfolioSelector from './PortfolioSelector';
import ComparisonTable from './ComparisonTable';
import TradesList from './TradesList';
import Header from './Header';
import './Dashboard.css';

const Dashboard = () => {
    return (
        <div className="dashboard">
            <Header />
            <PortfolioSelector />
            <PortfolioChart />
            <ComparisonTable />
            <TradesList />
        </div>
    );
};

export default Dashboard;