import React, { useEffect, useState } from 'react';
import { fetchTrades } from '../services/api';

const TradesList = () => {
    const [trades, setTrades] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const getTrades = async () => {
            try {
                const data = await fetchTrades();
                setTrades(data);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        getTrades();
    }, []);

    if (loading) {
        return <div>Loading...</div>;
    }

    if (error) {
        return <div>Error: {error}</div>;
    }

    return (
        <div>
            <h2>Trades List</h2>
            <ul>
                {trades.map(trade => (
                    <li key={trade.id}>
                        {trade.symbol}: {trade.quantity} at {trade.price}
                    </li>
                ))}
            </ul>
        </div>
    );
};

export default TradesList;