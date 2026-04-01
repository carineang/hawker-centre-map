import { describe, it, expect, vi, beforeEach } from 'vitest';
import { api } from '../services/api';

describe('API Service', () => {
  beforeEach(() => {
    global.fetch = vi.fn();
  });

  describe('getHawkers', () => {
    it('should fetch hawkers without filters', async () => {
      const mockData = [
        { id: 1, name: 'Maxwell Food Centre', region: 'Central' },
        { id: 2, name: 'Chinatown Complex', region: 'Central' }
      ];
      
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockData
      });
      
      const result = await api.getHawkers();
      
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('/api/hawkers')
      );
      expect(result).toEqual(mockData);
    });
    
    it('should fetch hawkers with region filter', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      });
      
      await api.getHawkers({ region: 'Central' });
      
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('region=Central')
      );
    });
    
    it('should fetch hawkers with search filter', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => []
      });
      
      await api.getHawkers({ search: 'Maxwell' });
      
      expect(global.fetch).toHaveBeenCalledWith(
        expect.stringContaining('search=Maxwell')
      );
    });
    
    it('should handle API errors', async () => {
      global.fetch.mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error'
      });
      
      await expect(api.getHawkers()).rejects.toThrow('Failed to fetch hawkers');
    });
  });
});