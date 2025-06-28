import axios from 'axios';
import type { ModelListResponse } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api';

export const fetchModels = async (): Promise<ModelListResponse> => {
  try {
    const response = await axios.get(`${API_BASE_URL}/models`);
    return response.data;
  } catch (error) {
    console.error('Error fetching models:', error);
    throw new Error('Failed to fetch models list');
  }
};