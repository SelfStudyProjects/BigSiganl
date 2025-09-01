// This file contains utility functions for charting.

export const formatChartData = (data) => {
    return data.map(item => ({
        x: item.date,
        y: item.value
    }));
};

export const calculateMovingAverage = (data, windowSize) => {
    const movingAverages = [];
    for (let i = 0; i <= data.length - windowSize; i++) {
        const window = data.slice(i, i + windowSize);
        const average = window.reduce((sum, value) => sum + value.y, 0) / windowSize;
        movingAverages.push({ x: window[windowSize - 1].x, y: average });
    }
    return movingAverages;
};

export const getChartOptions = (title) => {
    return {
        responsive: true,
        plugins: {
            legend: {
                display: true,
                position: 'top',
            },
            title: {
                display: true,
                text: title,
            },
        },
    };
};