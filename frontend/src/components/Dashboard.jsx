/*
메인 대시보드 컴포넌트
*/
IMPORT React, useState, useEffect
IMPORT PortfolioChart, PortfolioSelector, ComparisonTable, TradesList

FUNCTION Dashboard({ portfolios }):
    STATE selectedPortfolios = all portfolios initially
    STATE chartData = null
    STATE buyHoldData = null
    STATE showComparison = false
    
    EFFECT when portfolios or selectedPortfolios change:
        CALL updateChartData()
        CALL fetchBuyHoldData()
    
    FUNCTION updateChartData():
        filtered_data = FILTER portfolios by selectedPortfolios
        chart_formatted_data = FORMAT data for Chart.js
        SET chartData = chart_formatted_data
    
    FUNCTION fetchBuyHoldData():
        TRY:
            data = AWAIT api.getBuyHoldComparison()
            SET buyHoldData = data
        CATCH error:
            CONSOLE.log(error)
    
    FUNCTION handlePortfolioSelection(portfolio_ids):
        SET selectedPortfolios = portfolio_ids
    
    FUNCTION toggleComparison():
        SET showComparison = !showComparison
    
    RETURN:
        <div className="dashboard">
            <div className="dashboard-controls">
                <PortfolioSelector 
                    portfolios={portfolios}
                    selectedPortfolios={selectedPortfolios}
                    onSelectionChange={handlePortfolioSelection}
                />
                <button onClick={toggleComparison}>
                    {showComparison ? 'Hide' : 'Show'} Buy & Hold Comparison
                </button>
            </div>
            
            <div className="dashboard-main">
                <PortfolioChart 
                    data={chartData}
                    buyHoldData={showComparison ? buyHoldData : null}
                />
                
                <div className="dashboard-tables">
                    <ComparisonTable 
                        portfolios={selectedPortfolios}
                        buyHoldData={buyHoldData}
                    />
                    <TradesList limit={10} />
                </div>
            </div>
        </div>