import React from 'react';
import { Line } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    TimeScale,
} from 'chart.js';
import 'chartjs-adapter-date-fns';
import styled from 'styled-components';

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend,
    TimeScale
);

const ChartContainer = styled.div`
    width: 80%;
    max-width: 800px;
    height: 400px;
    margin: 0 auto;
    padding: 16px;
`;

const PriceHistoryChart = ({ data }) => {
    // Ensure dates are properly formatted and sorted
    const formattedData = data.map(entry => ({
        date: new Date(entry.created_at).toISOString(), // ISO format for time scale
        price: parseFloat(entry.price)
    })).sort((a, b) => new Date(a.date) - new Date(b.date));

    console.log('Formatted Data:', formattedData);

    const chartData = {
        labels: formattedData.map(entry => entry.date),
        datasets: [
            {
                label: 'Price',
                data: formattedData.map(entry => entry.price),
                fill: false,
                backgroundColor: 'rgba(54, 162, 235, 0.2)', // Light blue background
                borderColor: 'rgba(54, 162, 235, 1)', // Darker blue border
                pointBackgroundColor: 'rgba(75, 192, 192, 1)', // Point color
                pointBorderColor: '#fff', // Point border color
                pointHoverBackgroundColor: '#fff', // Point hover background color
                pointHoverBorderColor: 'rgba(75, 192, 192, 1)', // Point hover border color
                pointRadius: 5,
                pointHoverRadius: 8,
                tension: 0.4
            }
        ]
    };

    const options = {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
            x: {
                type: 'time',
                time: {
                    unit: 'day',
                    tooltipFormat: 'P'
                },
                title: {
                    display: true,
                    text: 'Date',
                    font: {
                        size: 14
                    }
                }
            },
            y: {
                beginAtZero: false,
                title: {
                    display: true,
                    text: 'Price (EUR)',
                    font: {
                        size: 14
                    }
                }
            }
        },
        plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                    font: {
                        size: 12
                    }
                }
            },
            tooltip: {
                callbacks: {
                    label: function (tooltipItem) {
                        return `Price: €${tooltipItem.raw}`;
                    }
                }
            }
        }
    };

    return (
        <ChartContainer>
            <Line data={chartData} options={options} />
        </ChartContainer>
    );
};

export default PriceHistoryChart;
