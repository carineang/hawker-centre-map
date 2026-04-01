/**
 * API utility module for interacting with the Hawker Centre backend.
 *
 * Uses the environment variable `VITE_API_URL` if available,
 * otherwise defaults to `http://localhost:8000`.
 */

const API_BASE = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
    /**
   * Fetch hawker centres from the API with optional filters.
   *
   * @param {Object} [filters={}] - Filters to apply to the hawker search.
   * @param {string} [filters.region] - Filter by region (e.g., "Central", "East").
   * @param {string} [filters.search] - Search by name (case-insensitive).
   * @returns {Promise<Array<Object>>} A promise that resolves to an array of hawker objects.
   * @throws {Error} Throws an error if the fetch fails.
   *
   * @example
   * const hawkers = await api.getHawkers({ region: 'Central', search: 'Maxwell' });
   */
    async getHawkers(filters = {}) {
        try {
            const params = new URLSearchParams();

            if (filters.region) params.append('region', filters.region);
            if (filters.search) params.append('search', filters.search);

            const url = `${API_BASE}/api/hawkers${params.toString() ? '?' + params : ''}`;

            const response = await fetch(url);

            if (!response.ok) {
                throw new Error(`Failed to fetch hawkers: ${response.status} ${response.statusText}`);
            }

            return response.json();
        } catch (error) {
            console.error('[API] getHawkers error:', error);
            throw error;
        }
  },
};
