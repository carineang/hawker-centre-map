const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
  
    // Get hawkers
    async getHawkers(filters = {}) {
        const params = new URLSearchParams();
        if (filters.region) params.append('region', filters.region);
        if (filters.search) params.append('search', filters.search);
        const response = await fetch(`${API_BASE}/api/hawkers?${params}`);
        if (!response.ok) throw new Error('Failed to fetch hawkers');
        return response.json();
  },
};
