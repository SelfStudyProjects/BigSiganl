import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import PortfolioChart from './components/PortfolioChart';
import PortfolioSelector from './components/PortfolioSelector';
import ComparisonTable from './components/ComparisonTable';
import TradesList from './components/TradesList';
import Header from './components/Header';
import './styles/global.css';

function App() {
    return (
        <Router>
            <div>
                <Header />
                <Switch>
                    <Route path="/" exact component={Dashboard} />
                    <Route path="/portfolio-chart" component={PortfolioChart} />
                    <Route path="/portfolio-selector" component={PortfolioSelector} />
                    <Route path="/comparison-table" component={ComparisonTable} />
                    <Route path="/trades-list" component={TradesList} />
                </Switch>
            </div>
        </Router>
    );
}

export default App;