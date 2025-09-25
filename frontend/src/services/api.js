// src/services/api.js - 완전한 버전
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// 기존 함수들
export const getTrades = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/api/trades/`);
        return response.data;
    } catch (error) {
        console.error('Error fetching trades:', error);
        throw error;
    }
};

export const getPortfolios = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/api/portfolios/`);
        return response.data;
    } catch (error) {
        console.error('Error fetching portfolios:', error);
        throw error;
    }
};

// 새로운 분석 함수들
export const getPerformanceData = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/analysis/performance/`);
        if (!response.ok) throw new Error('API 호출 실패');
        return await response.json();
    } catch (error) {
        console.error('성과 데이터 로드 실패:', error);
        throw error;
    }
};

export const getDashboardData = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/api/analysis/dashboard/`);
        if (!response.ok) throw new Error('API 호출 실패');
        return await response.json();
    } catch (error) {
        console.error('대시보드 데이터 로드 실패:', error);
        throw error;
    }
};

export const getChartUrl = (chartType) => `${API_BASE_URL}/media/charts/${chartType}.png`;

// 통합 API 객체 - 이 부분이 핵심!
export const api = {
    trades: {
        getAll: getTrades,
    },
    portfolios: {
        getAll: getPortfolios,
    },
    analysis: {
        getPerformanceData: getPerformanceData,
        getDashboardData: getDashboardData,
        getChartUrl: getChartUrl  // 이 부분이 중요!
    }
};