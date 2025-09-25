/*
포트폴리오 성과 차트 컴포넌트
*/
IMPORT React, useRef, useEffect
IMPORT Chart from 'chart.js'
IMPORT chartUtils

FUNCTION PortfolioChart({ data, buyHoldData }):
    chartRef = useRef(null)
    chartInstance = useRef(null)
    
    EFFECT when data or buyHoldData changes:
        IF chartInstance.current exists:
            DESTROY existing chart
        
        IF data exists:
            CALL createChart()
    
    FUNCTION createChart():
        ctx = GET context from chartRef
        
        datasets = []
        
        # 포트폴리오 데이터셋 추가
        FOR each portfolio IN data:
            PUSH {
                label: portfolio.name + ' (수익률 %)',
                data: FORMAT portfolio performance data,
                borderColor: GET random color,
                fill: false,
                tension: 0.1
            } TO datasets
        
        # Buy & Hold 데이터셋 추가 (점선으로)
        IF buyHoldData exists:
            FOR each buyhold IN buyHoldData:
                PUSH {
                    label: buyhold.name + ' (Buy & Hold)',
                    data: FORMAT buyhold performance data,
                    borderColor: GET random color,
                    borderDash: [5, 5],
                    fill: false,
                    tension: 0.1
                } TO datasets
        
        chartInstance.current = NEW Chart(ctx, {
            type: 'line',
            data: { datasets },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        type: 'time',
                        time: {
                            unit: 'day',
                            displayFormats: { day: 'MM-DD' }
                        },
                        title: { display: true, text: '날짜' }
                    },
                    y: {
                        title: { display: true, text: '수익률 (%)' },
                        ticks: {
                            callback: function(value) {
                                RETURN value + '%'
                            }
                        }
                    }
                },
                plugins: {
                    tooltip: {
                        mode: 'index',
                        intersect: false,
                        callbacks: {
                            label: function(context) {
                                RETURN context.dataset.label + ': ' + 
                                       context.parsed.y.toFixed(2) + '%'
                            }
                        }
                    },
                    legend: { position: 'top' }
                }
            }
        })
    
    RETURN:
        <div className="chart-container">
            <h2>포트폴리오 성과 비교</h2>
            <canvas ref={chartRef} />
        </div>