import { useEffect, useRef } from 'react';
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

/**
 * Fix default Leaflet marker icons when using React-Leaflet.
 */
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon-2x.png',
  iconUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-icon.png',
  shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
});

/**
 * Fit the map bounds to the given markers.
 *
 * @param {Object} props
 * @param {Array} props.markers - Array of marker objects with latitude and longitude
 */
function FitBounds({ markers }) {
  const map = useMap();
  
  useEffect(() => {
    if (markers && markers.length > 0) {
      const bounds = L.latLngBounds(markers.map(m => [m.latitude, m.longitude]));
      
      if (markers.length === 1) {
        map.setView([markers[0].latitude, markers[0].longitude], 15);
      } else {
        map.fitBounds(bounds, { padding: [50, 50] });
      }
    }
  }, [markers, map]);
  
  return null;
}

/**
 * HawkerMap component
 *
 * Displays a Leaflet map with markers for each hawker centre.
 * Supports auto-fitting to visible markers and zooming to a selected hawker.
 *
 * @param {Object} props
 * @param {Array} props.hawkers - Array of hawker centre objects
 * @param {Object|null} props.selectedHawker - Hawker centre to zoom to
 * @param {Function} props.onMarkerClick - Callback when a marker is clicked
 */
function HawkerMap({ hawkers, selectedHawker, onMarkerClick }) {
  const mapRef = useRef(null);
  
  // When a hawker is selected, zoom to it
  useEffect(() => {
    if (selectedHawker && mapRef.current) {
      const map = mapRef.current;
      map.setView([selectedHawker.latitude, selectedHawker.longitude], 15);
    }
  }, [selectedHawker]);
  
  // When hawkers are filtered, auto-fit
  const shouldAutoFit = hawkers.length > 0 && !selectedHawker;
  
  const handleMarkerClick = (hawker, markerEvent) => {
    onMarkerClick(hawker);
  };
  
  return (
    <MapContainer
      ref={mapRef}
      center={[1.3521, 103.8198]}
      zoom={12}
      style={{ width: '100%', height: '100%', borderRadius: '12px' }}
      zoomControl={true}
      attributionControl={true}
    >
      {shouldAutoFit && <FitBounds markers={hawkers} />}
      
      <TileLayer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>'
      />
      
      {hawkers.map((hawker) => (
        <Marker
          key={hawker.id}
          position={[hawker.latitude, hawker.longitude]}
          eventHandlers={{
            click: (e) => {
              onMarkerClick(hawker);
            }
          }}
        >
          <Popup>
            <div style={{ padding: '6px', minWidth: '200px' }}>
              <h3 style={{ fontWeight: 'bold', fontSize: '18px', marginBottom: '8px' }}>{hawker.name}</h3>
              <p style={{ fontSize: '13px', marginBottom: '4px' }}>{hawker.address}</p>
              <p style={{ fontSize: '13px', marginBottom: '2px' }}>📍 Postal code: {hawker.postal_code}</p>
              <p style={{ fontSize: '13px', marginBottom: '8px' }}>🗺️ Region: {hawker.region}</p>
              {hawker.total_stalls > 0 && (
                <p style={{ fontSize: '13px', marginBottom: '8px' }}>🍜 Stalls: {hawker.total_stalls} stalls</p>
              )}
            </div>
          </Popup>
        </Marker>
      ))}
    </MapContainer>
  );
}

export default HawkerMap;
