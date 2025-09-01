import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api'; // Adjust the base URL as needed

// Function to get trades
export const getTrades = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/trades/`);
        return response.data;
    } catch (error) {
        console.error('Error fetching trades:', error);
        throw error;
    }
};

// Function to get portfolios
export const getPortfolios = async () => {
    try {
        const response = await axios.get(`${API_BASE_URL}/portfolios/`);
        return response.data;
    } catch (error) {
        console.error('Error fetching portfolios:', error);
        throw error;
    }
};

// Function to create a new trade
export const createTrade = async (tradeData) => {
    try {
        const response = await axios.post(`${API_BASE_URL}/trades/`, tradeData);
        return response.data;
    } catch (error) {
        console.error('Error creating trade:', error);
        throw error;
    }
};

// Function to update a trade
export const updateTrade = async (tradeId, tradeData) => {
    try {
        const response = await axios.put(`${API_BASE_URL}/trades/${tradeId}/`, tradeData);
        return response.data;
    } catch (error) {
        console.error('Error updating trade:', error);
        throw error;
    }
};

// Function to delete a trade
export const deleteTrade = async (tradeId) => {
    try {
        await axios.delete(`${API_BASE_URL}/trades/${tradeId}/`);
    } catch (error) {
        console.error('Error deleting trade:', error);
        throw error;
    }
};