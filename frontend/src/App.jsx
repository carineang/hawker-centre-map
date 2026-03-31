import { useState, useEffect, useRef } from 'react';
import HawkerMap from './components/HawkerMap';
import { api } from './services/api';

function App() {
  const [hawkers, setHawkers] = useState([]);
  const [filteredHawkers, setFilteredHawkers] = useState([]);
  const [selectedRegion, setSelectedRegion] = useState('');
  const [regionStats, setRegionStats] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [windowWidth, setWindowWidth] = useState(window.innerWidth);
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState('');
  const [searchTerm, setSearchTerm] = useState('');
  
  const regions = ['All', 'Central', 'North', 'East', 'West', 'North-East'];
  
  // Debounce timer
  const debounceTimerRef = useRef(null);
  
  // Track window resize for responsive adjustments
  useEffect(() => {
    const handleResize = () => setWindowWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  // Debounce search term: wait 500ms after user stops typing
  useEffect(() => {
    // Clear previous timer
    if (debounceTimerRef.current) {
      clearTimeout(debounceTimerRef.current);
    }
    
    // Set new timer
    debounceTimerRef.current = setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
    }, 500);
    
    return () => {
      if (debounceTimerRef.current) {
        clearTimeout(debounceTimerRef.current);
      }
    };
  }, [searchTerm]);
  
  useEffect(() => {
    loadHawkers();
    loadRegionStats();
  }, []);
  
  useEffect(() => {
    let filtered = hawkers;
    
    if (debouncedSearchTerm) {
      filtered = filtered.filter(h => 
        h.name.toLowerCase().includes(debouncedSearchTerm.toLowerCase())
      );
    }
    
    if (selectedRegion && selectedRegion !== 'All') {
      filtered = filtered.filter(h => h.region === selectedRegion);
    }
    
    setFilteredHawkers(filtered);
  }, [debouncedSearchTerm, selectedRegion, hawkers]);
  
  const loadHawkers = async () => {
    try {
      const data = await api.getHawkers();
      setHawkers(data);
      setFilteredHawkers(data);
    } catch (error) {
      console.error('Failed to load hawkers:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  const loadRegionStats = async () => {
    try {
      const stats = await api.getRegionStats();
      setRegionStats(stats);
    } catch (error) {
      console.error('Failed to load region stats:', error);
    }
  };
  
  const handleResetFilters = () => {
    setSearchTerm('');
    setDebouncedSearchTerm('');
    setSelectedRegion('');
  };
  
  const isMobile = windowWidth < 768;
  
  if (isLoading) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '100vh' }}>
        <div className="text-center">
          <div className="text-lg">Loading hawker centres...</div>
        </div>
      </div>
    );
  }
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <div className="header">
        <h1>🍜 Singapore Hawker Centre Map</h1>
      </div>
      <div className={isMobile ? 'hawker-layout' : 'hawker-layout'}>
        <div className="hawker-sidebar" style={isMobile ? { order: 2 } : {}}>
          <div className="card">
            <h2 style={{ fontSize: '18px', marginBottom: '12px' }}>🔍 Search & Filter</h2>
            
            <input
              type="text"
              placeholder="Search by name..."
              className="input"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ marginBottom: '12px' }}
            />
            
            {searchTerm !== debouncedSearchTerm && searchTerm && (
              <p style={{ fontSize: '12px', color: 'var(--text)', marginTop: '-8px', marginBottom: '12px' }}>
                Searching...
              </p>
            )}
            
            <select
              className="select"
              value={selectedRegion}
              onChange={(e) => setSelectedRegion(e.target.value)}
              style={{ marginBottom: '12px' }}
            >
              {regions.map(region => (
                <option key={region} value={region}>{region}</option>
              ))}
            </select>
            
            <button
              className="btn btn-secondary btn-block"
              onClick={handleResetFilters}
            >
              Reset Filters
            </button>
          </div>
          
          {regionStats && (
            <div className="card">
              <h2 style={{ fontSize: '18px', marginBottom: '12px' }}>📊 Region Distribution</h2>
              {Object.entries(regionStats).map(([region, count]) => (
                <div key={region} style={{ marginBottom: '12px' }}>
                  <div className="flex justify-between text-sm">
                    <span>{region}</span>
                    <span>{count}</span>
                  </div>
                  <div className="progress-bar">
                    <div 
                      className="progress-fill"
                      style={{ width: `${(count / hawkers.length) * 100}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        
        <div className="hawker-main" style={isMobile ? { order: 1 } : {}}>
          <div className="map-fixed">
            <HawkerMap
              hawkers={filteredHawkers}
            />
          </div>
          
          <div className="stats-bar">
            <span>Showing {filteredHawkers.length} of {hawkers.length} hawker centres</span>
            {searchTerm !== debouncedSearchTerm && searchTerm && (
              <span style={{ fontSize: '12px', color: 'var(--accent)' }}>
                Searching...
              </span>
            )}
          </div>
        </div>
      </div>
      
      <div className="footer">
        <p>Data from Data.gov.sg</p>
      </div>
    </div>
  );
}

export default App;
