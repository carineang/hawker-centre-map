import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import HawkerMap from '../components/HawkerMap';

// Mock Leaflet
vi.mock('react-leaflet', () => ({
  MapContainer: ({ children }) => <div data-testid="map-container">{children}</div>,
  TileLayer: () => <div>TileLayer</div>,
  Marker: ({ children, position }) => <div data-testid={`marker-${position[0]}`}>{children}</div>,
  Popup: ({ children }) => <div data-testid="popup">{children}</div>,
  useMap: () => ({
    setView: vi.fn(),
    fitBounds: vi.fn()
  })
}));

describe('HawkerMap Component', () => {
  const mockHawkers = [
    {
      id: 1,
      name: 'Maxwell Food Centre',
      address: '1 Kadayanallur St',
      postal_code: '069184',
      latitude: 1.2801,
      longitude: 103.8451,
      region: 'Central',
      total_stalls: 100
    },
    {
      id: 2,
      name: 'Chinatown Complex',
      address: '335 Smith St',
      postal_code: '050335',
      latitude: 1.2838,
      longitude: 103.8432,
      region: 'Central',
      total_stalls: 200
    }
  ];

  it('should render map container', () => {
    render(<HawkerMap hawkers={[]} />);
    expect(screen.getByTestId('map-container')).toBeInTheDocument();
  });

  it('should render markers for each hawker', () => {
    render(<HawkerMap hawkers={mockHawkers} />);
    
    expect(screen.getByTestId('marker-1.2801')).toBeInTheDocument();
    expect(screen.getByTestId('marker-1.2838')).toBeInTheDocument();
  });

  it('should not render markers when hawkers array is empty', () => {
    render(<HawkerMap hawkers={[]} />);
    
    expect(screen.queryByTestId('marker-1.2801')).not.toBeInTheDocument();
  });
});