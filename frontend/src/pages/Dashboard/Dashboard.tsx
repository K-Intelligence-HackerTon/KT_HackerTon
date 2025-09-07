// frontend/src/pages/Dashboard/Dashboard.tsx - 수정
import React, { useState, useEffect } from 'react';
import './Dashboard.css';

const Dashboard: React.FC = () => {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [fireAlerts, setFireAlerts] = useState([
    {
      id: 1,
      location: '양평군 용문면',
      confidence: 95.2,
      status: 'critical',
      timestamp: new Date(Date.now() - 300000),
      coordinates: { lat: 37.5665, lng: 127.9780 }
    },
    {
      id: 2,
      location: '가평군 청평면',
      confidence: 78.5,
      status: 'warning',
      timestamp: new Date(Date.now() - 600000),
      coordinates: { lat: 37.7451, lng: 127.4251 }
    }
  ]);

  const [sensorData, setSensorData] = useState({
    temperature: 32.5,
    humidity: 45.2,
    smokeDensity: 78.3,
    windSpeed: 12.4,
    airQuality: 156
  });

  const [cctvFeeds, setCctvFeeds] = useState([
    {
      id: 1,
      name: '용문산 CCTV',
      status: 'active',
      lastUpdate: new Date(Date.now() - 10000),
      fireDetected: true,
      confidence: 92.1
    },
    {
      id: 2,
      name: '청편산 CCTV',
      status: 'active',
      lastUpdate: new Date(Date.now() - 15000),
      fireDetected: false,
      confidence: 15.3
    }
  ]);

  // 시연용 실시간 데이터 시뮬레이션
  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
      
      // 센서 데이터 시뮬레이션
      setSensorData(prev => ({
        temperature: Math.max(20, Math.min(40, prev.temperature + (Math.random() - 0.5) * 0.5)),
        humidity: Math.max(0, Math.min(100, prev.humidity + (Math.random() - 0.5) * 2)),
        smokeDensity: Math.max(0, Math.min(100, prev.smokeDensity + (Math.random() - 0.5) * 3)),
        windSpeed: Math.max(0, Math.min(20, prev.windSpeed + (Math.random() - 0.5) * 1)),
        airQuality: Math.max(0, Math.min(300, prev.airQuality + (Math.random() - 0.5) * 5))
      }));

      // CCTV 데이터 시뮬레이션
      setCctvFeeds(prev => prev.map(cctv => ({
        ...cctv,
        lastUpdate: new Date(),
        confidence: Math.max(0, Math.min(100, cctv.confidence + (Math.random() - 0.5) * 2))
      })));

      // 새로운 화재 알림 시뮬레이션 (10% 확률)
      if (Math.random() < 0.1) {
        const newAlert = {
          id: Date.now(),
          location: ['양평군 용문면', '가평군 청평면', '포천군 내촌면', '여주시 산북면'][Math.floor(Math.random() * 4)],
          confidence: Math.random() * 30 + 70,
          status: Math.random() > 0.5 ? 'critical' : 'warning',
          timestamp: new Date(),
          coordinates: { 
            lat: 37.5 + Math.random() * 0.5, 
            lng: 127.3 + Math.random() * 0.5 
          }
        };
        setFireAlerts(prev => [newAlert, ...prev.slice(0, 4)]);
      }
    }, 2000);

    return () => clearInterval(timer);
  }, []);

  // 화재 알림 제거 함수
  const removeAlert = (id: number) => {
    setFireAlerts(prev => prev.filter(alert => alert.id !== id));
  };

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <div className="header-content">
          <div className="header-title">
            <div className="title-icon">🚨</div>
            <div className="title-text">
              <h1>산불 대응 AI Agent 시스템</h1>
              <p>믿:음 2.0 LLM 기반 실시간 모니터링</p>
            </div>
          </div>
          <div className="header-info">
            <div className="current-time">
              <div className="time-icon">⏰</div>
              <div className="time-text">
                <div className="time-label">현재 시간</div>
                <div className="time-value">{currentTime.toLocaleString('ko-KR')}</div>
              </div>
            </div>
            <div className="system-status">
              <div className="status-indicator active"></div>
              <span>시스템 정상</span>
            </div>
          </div>
        </div>
      </div>

      <div className="dashboard-content">
        {/* 실시간 알림 */}
        <div className="alert-section">
          <div className="section-header">
            <h2>🚨 실시간 화재 알림</h2>
            <div className="alert-count">{fireAlerts.length}건</div>
          </div>
          <div className="alert-grid">
            {fireAlerts.map(alert => (
              <div key={alert.id} className={`alert-card ${alert.status}`}>
                <div className="alert-card-header">
                  <div className="alert-location">
                    <div className="location-icon">🗺️</div>
                    <span>{alert.location}</span>
                  </div>
                  <div className="alert-actions">
                    <div className={`confidence-badge ${alert.status}`}>
                      {alert.confidence.toFixed(1)}%
                    </div>
                    <button 
                      className="alert-close"
                      onClick={() => removeAlert(alert.id)}
                    >
                      ✕
                    </button>
                  </div>
                </div>
                <div className="alert-card-body">
                  <div className="alert-time">
                    <div className="time-icon">⏰</div>
                    <span>{alert.timestamp.toLocaleString('ko-KR')}</span>
                  </div>
                  <div className="alert-coords">
                    <div className="coords-icon">📍</div>
                    <span>({alert.coordinates.lat.toFixed(4)}, {alert.coordinates.lng.toFixed(4)})</span>
                  </div>
                </div>
                <div className="alert-card-footer">
                  <div className={`status-indicator ${alert.status}`}></div>
                  <span>{alert.status === 'critical' ? '긴급' : '주의'}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 센서 데이터 */}
        <div className="sensor-section">
          <div className="section-header">
            <h2>📊 실시간 센서 데이터</h2>
            <div className="sensor-status-indicator">
              <div className="status-dot active"></div>
              <span>실시간 업데이트 중</span>
            </div>
          </div>
          <div className="sensor-grid">
            <div className="sensor-card temperature">
              <div className="sensor-icon">🌡</div>
              <div className="sensor-content">
                <div className="sensor-label">온도</div>
                <div className="sensor-value">{sensorData.temperature.toFixed(1)}°C</div>
                <div className={`sensor-status ${sensorData.temperature > 30 ? 'warning' : 'normal'}`}>
                  {sensorData.temperature > 30 ? '높음' : '정상'}
                </div>
              </div>
            </div>
            <div className="sensor-card humidity">
              <div className="sensor-icon">💧</div>
              <div className="sensor-content">
                <div className="sensor-label">습도</div>
                <div className="sensor-value">{sensorData.humidity.toFixed(1)}%</div>
                <div className={`sensor-status ${sensorData.humidity < 50 ? 'warning' : 'normal'}`}>
                  {sensorData.humidity < 50 ? '낮음' : '정상'}
                </div>
              </div>
            </div>
            <div className="sensor-card smoke">
              <div className="sensor-icon">💨</div>
              <div className="sensor-content">
                <div className="sensor-label">연기 농도</div>
                <div className="sensor-value">{sensorData.smokeDensity.toFixed(1)}</div>
                <div className={`sensor-status ${sensorData.smokeDensity > 70 ? 'critical' : 'normal'}`}>
                  {sensorData.smokeDensity > 70 ? '위험' : '정상'}
                </div>
              </div>
            </div>
            <div className="sensor-card wind">
              <div className="sensor-icon">🌪</div>
              <div className="sensor-content">
                <div className="sensor-label">풍속</div>
                <div className="sensor-value">{sensorData.windSpeed.toFixed(1)} m/s</div>
                <div className={`sensor-status ${sensorData.windSpeed > 10 ? 'warning' : 'normal'}`}>
                  {sensorData.windSpeed > 10 ? '강함' : '약함'}
                </div>
              </div>
            </div>
            <div className="sensor-card air">
              <div className="sensor-icon">🌬</div>
              <div className="sensor-content">
                <div className="sensor-label">대기질</div>
                <div className="sensor-value">{sensorData.airQuality.toFixed(0)}</div>
                <div className={`sensor-status ${sensorData.airQuality > 150 ? 'critical' : 'normal'}`}>
                  {sensorData.airQuality > 150 ? '나쁨' : '좋음'}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* CCTV 모니터링 */}
        <div className="cctv-section">
          <div className="section-header">
            <h2>📹 CCTV 모니터링</h2>
            <div className="cctv-count">{cctvFeeds.length}대 운영중</div>
          </div>
          <div className="cctv-grid">
            {cctvFeeds.map(cctv => (
              <div key={cctv.id} className="cctv-card">
                <div className="cctv-card-header">
                  <div className="cctv-name">
                    <div className="camera-icon">📷</div>
                    <span>{cctv.name}</span>
                  </div>
                  <div className={`cctv-status ${cctv.status}`}>
                    <div className="status-dot"></div>
                    {cctv.status === 'active' ? '활성' : '비활성'}
                  </div>
                </div>
                <div className="cctv-feed">
                  <div className="cctv-placeholder">
                    {cctv.name === '용문산 CCTV' ? (
                      <img 
                        src="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=200&fit=crop&crop=center" 
                        alt="용문산 CCTV"
                        className="cctv-image"
                      />
                    ) : cctv.name === '청편산 CCTV' ? (
                      <img 
                        src="https://images.unsplash.com/photo-1441974231531-c6227db76b6e?w=400&h=200&fit=crop&crop=center" 
                        alt="청편산 CCTV"
                        className="cctv-image"
                      />
                    ) : (
                      <div className="cctv-image">
                        {cctv.fireDetected ? '🔥' : '🌲'}
                      </div>
                    )}
                    {cctv.fireDetected && (
                      <div className="fire-detection-overlay">
                        <div className="fire-alert">
                          <span className="fire-icon">🔥</span>
                          <span className="fire-confidence">{cctv.confidence.toFixed(1)}%</span>
                        </div>
                      </div>
                    )}
                  </div>
                </div>
                <div className="cctv-card-footer">
                  <div className="cctv-update">
                    <div className="update-icon">🔄</div>
                    <span>마지막 업데이트: {cctv.lastUpdate.toLocaleTimeString('ko-KR')}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* 지도 모니터링 */}
        <div className="map-section">
          <div className="section-header">
            <h2>🗺️ 실시간 모니터링 지도</h2>
            <div className="map-legend">
              <div className="legend-item">
                <div className="legend-color critical"></div>
                <span>화재 위험 (90% 이상)</span>
              </div>
              <div className="legend-item">
                <div className="legend-color warning"></div>
                <span>주의 (70-90%)</span>
              </div>
              <div className="legend-item">
                <div className="legend-color normal"></div>
                <span>정상 (70% 미만)</span>
              </div>
            </div>
          </div>
          <div className="map-container">
            <div className="map-placeholder">
              <img 
                src="/images/용문산.png" 
                alt="실시간 모니터링 지도"
                className="map-image"
              />
              <div className="map-overlay">
                <div className="map-grid"></div>
                <div className="map-markers">
                  {fireAlerts.map(alert => (
                    <div
                      key={alert.id}
                      className={`map-marker ${alert.status}`}
                      style={{
                        left: `${30 + Math.random() * 40}%`,
                        top: `${20 + Math.random() * 60}%`
                      }}
                    >
                      <div className="marker-icon">🔥</div>
                      <div className="marker-pulse"></div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;