import React from 'react';
import { Line } from 'react-chartjs-2';

const PortfolioChart = ({ data }) => {
    const chartData = {
        labels: data.map(item => item.date),
        datasets: [
            {
                label: 'Portfolio Value',
                data: data.map(item => item.value),
                borderColor: 'rgba(75,192,192,1)',
                backgroundColor: 'rgba(75,192,192,0.2)',
                fill: true,
            },
        ],
    };

    const options = {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true,
            },
        },
    };

    return (
        <div>
            <h2>Portfolio Value Over Time</h2>
            <Line data={chartData} options={options} />
        </div>
    );
};

export default PortfolioChart;