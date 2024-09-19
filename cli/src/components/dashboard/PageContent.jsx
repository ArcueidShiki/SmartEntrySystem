import React, { useEffect, useState } from 'react';
import './pageContent.css';

function PageContent() {
  const [currentReading, setCurrentReading] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:4000';

  const fetchData = () => {
    setIsLoading(true);
    setError(null);

    // Fetch JSON data
    fetch(`${API_URL}/api/real_time_data`)
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        console.log("Fetched data:", data);
        setCurrentReading(data.current_reading);
        setIsLoading(false);
      })
      .catch(e => {
        console.error("Error fetching data:", e);
        setError(e.message);
        setIsLoading(false);
      });

    // Fetch image
    fetch(`${API_URL}/api/current_image`)
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.blob();
      })
      .then(blob => {
        const imageUrl = URL.createObjectURL(blob);
        setImageUrl(imageUrl);
      })
      .catch(e => {
        console.error("Error fetching image:", e);
        setError(e.message);
      });
  };

  useEffect(() => {
    fetchData();
    // Set up polling every 5 seconds
    const interval = setInterval(fetchData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">
      <div className="upper-section">
        <h1>Real-time Monitoring</h1>
        {imageUrl ? (
          <img src={imageUrl} alt="Real-time camera feed" style={{maxWidth: '100%', height: 'auto'}} />
        ) : (
          <p>Loading image...</p>
        )}
      </div>
      <div className="lower-section">
        {isLoading ? (
          <div className="text-box">
            <h2>Loading data...</h2>
          </div>
        ) : error ? (
          <div className="text-box">
            <h2>Error: {error}</h2>
          </div>
        ) : currentReading ? (
          <>
            <div className="text-box">
              <h2>Temperature: {currentReading.temperature}°C</h2>
            </div>
            <div className="text-box">
              <h2>Mask: {currentReading.mask_status}</h2>
            </div>
            <div className="text-box">
              <h2>Last Updated: {new Date(currentReading.timestamp).toLocaleString()}</h2>
            </div>
          </>
        ) : (
          <div className="text-box">
            <h2>No data available</h2>
          </div>
        )}
      </div>
    </div>
  );
}

export default PageContent;