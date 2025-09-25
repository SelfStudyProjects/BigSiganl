import React from 'react';

const PortfolioSelector = ({ portfolios, onSelect }) => {
    return (
        <div className="portfolio-selector">
            <h2>Select a Portfolio</h2>
            <ul>
                {portfolios.map((portfolio) => (
                    <li key={portfolio.id} onClick={() => onSelect(portfolio)}>
                        {portfolio.name}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default PortfolioSelector;