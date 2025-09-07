import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Alert, List, Avatar, Progress, Tag, Button } from 'antd';
import { 
  FireOutlined, 
  EyeOutlined, 
  RobotOutlined, 
  CheckCircleOutlined,
  ExclamationCircleOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  ReloadOutlined
} from '@ant-design/icons';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { MapContainer, TileLayer, Marker, Popup, Circle } from 'react-leaflet';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

// 아이콘 설정
delete (L.Icon.Default.prototype as any)._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

const Dashboard: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  // 실시간 알림 데이터
  const alerts = [
    {
      id: 1,
      type: 'fire',
      title: '화재 탐지 알림',
      message: '경기도 양평군 용문면에서 화재가 탐지되었습니다.',
      time: '14:32:15',
      level: 'high',
      location: '경기도 양평군 용문면',
      confidence: 95.2
    },
    {
      id: 2,
      type: 'sensor',
      title: '센서 이상 감지',
      message: 'IoT 센서 #S001에서 온도 급상승이 감지되었습니다.',
      time: '14:30:45',
      level: 'medium',
      location: '경기도 양평군 용문면',
      confidence: 87.3
    },
    {
      id: 3,
      type: 'weather',
      title: '기상 경보',
      message: '강풍 경보가 발령되어 화재 확산 위험이 높습니다.',
      time: '14:28:30',
      level: 'high',
      location: '경기도 전역',
      confidence: 92.1
    },
    {
      id: 4,
      type: 'ai',
      title: 'AI 권고안 생성',
      message: '믿:음 LLM이 소방청, 산림청, 지자체 권고안을 생성했습니다.',
      time: '14:25:15',
      level: 'info',
      location: 'AI 시스템',
      confidence: 97.9
    }
  ];

  // 통계 데이터
  const statistics = [
    {
      title: '활성 화재',
      value: 2,
      icon: <FireOutlined style={{ color: '#ff4d1a' }} />,
      color: '#ff4d1a',
      change: '+1',
      changeType: 'increase'
    },
    {
      title: '활성 센서',
      value: 156,
      icon: <EyeOutlined style={{ color: '#1a66cc' }} />,
      color: '#1a66cc',
      change: '+3',
      changeType: 'increase'
    },
    {
      title: 'AI 권고안',
      value: 8,
      icon: <RobotOutlined style={{ color: '#6633cc' }} />,
      color: '#6633cc',
      change: '+2',
      changeType: 'increase'
    },
    {
      title: '승인 완료',
      value: 6,
      icon: <CheckCircleOutlined style={{ color: '#33b233' }} />,
      color: '#33b233',
      change: '+1',
      changeType: 'increase'
    }
  ];

  // 차트 데이터
  const fireTrendData = [
    { time: '00:00', fires: 0, sensors: 150 },
    { time: '04:00', fires: 0, sensors: 152 },
    { time: '08:00', fires: 1, sensors: 154 },
    { time: '12:00', fires: 1, sensors: 155 },
    { time: '16:00', fires: 2, sensors: 156 },
    { time: '20:00', fires: 2, sensors: 156 }
  ];

  const sensorStatusData = [
    { name: '정상', value: 142, color: '#33b233' },
    { name: '주의', value: 10, color: '#ff9500' },
    { name: '경고', value: 3, color: '#ff4d1a' },
    { name: '오류', value: 1, color: '#8c8c8c' }
  ];

  // 지도 데이터
  const fireLocations = [
    { lat: 37.5665, lng: 127.9780, name: '양평군 용문면', severity: 'high' },
    { lat: 37.5512, lng: 127.9880, name: '양평군 서종면', severity: 'medium' }
  ];

  const sensorLocations = [
    { lat: 37.5665, lng: 127.9780, type: 'cctv', status: 'active' },
    { lat: 37.5512, lng: 127.9880, type: 'iot', status: 'warning' },
    { lat: 37.5400, lng: 127.9900, type: 'drone', status: 'active' }
  ];

  const handleRefresh = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      setLastUpdate(new Date());
    }, 1000);
  };

  const getAlertIcon = (type: string) => {
    switch (type) {
      case 'fire': return <FireOutlined style={{ color: '#ff4d1a' }} />;
      case 'sensor': return <EyeOutlined style={{ color: '#1a66cc' }} />;
      case 'weather': return <ExclamationCircleOutlined style={{ color: '#ff9500' }} />;
      case 'ai': return <RobotOutlined style={{ color: '#6633cc' }} />;
      default: return <ExclamationCircleOutlined />;
    }
  };

  const getAlertColor = (level: string) => {
    switch (level) {
      case 'high': return '#ff4d1a';
      case 'medium': return '#ff9500';
      case 'low': return '#33b233';
      case 'info': return '#1a66cc';
      default: return '#8c8c8c';
    }
  };

  return (
    <div>
      {/* 헤더 */}
      <div style={{ 
        display: 'flex', 
        justifyContent: 'space-between', 
        alignItems: 'center',
        marginBottom: '24px'
      }}>
        <h1 style={{ margin: 0, fontSize: '28px', fontWeight: '600' }}>
          🏔️ 산불 대응 AI Agent 시스템 - 메인 대시보드
        </h1>
        <Button 
          type="primary" 
          icon={<ReloadOutlined />} 
          onClick={handleRefresh}
          loading={loading}
        >
          새로고침
        </Button>
      </div>

      {/* 통계 카드 */}
      <Row gutter={[16, 16]} style={{ marginBottom: '24px' }}>
        {statistics.map((stat, index) => (
          <Col xs={24} sm={12} lg={6} key={index}>
            <Card>
              <Statistic
                title={stat.title}
                value={stat.value}
                prefix={stat.icon}
                valueStyle={{ color: stat.color }}
                suffix={
                  <span style={{ 
                    color: stat.changeType === 'increase' ? '#33b233' : '#ff4d1a',
                    fontSize: '14px'
                  }}>
                    {stat.changeType === 'increase' ? <ArrowUpOutlined /> : <ArrowDownOutlined />}
                    {stat.change}
                  </span>
                }
              />
            </Card>
          </Col>
        ))}
      </Row>

      {/* 실시간 알림 */}
      <Card 
        title="🚨 실시간 알림" 
        style={{ marginBottom: '24px' }}
        extra={<Tag color="red">실시간</Tag>}
      >
        <List
          dataSource={alerts}
          renderItem={(alert) => (
            <List.Item>
              <List.Item.Meta
                avatar={<Avatar icon={getAlertIcon(alert.type)} style={{ backgroundColor: getAlertColor(alert.level) }} />}
                title={
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span>{alert.title}</span>
                    <div>
                      <Tag color={getAlertColor(alert.level)}>{alert.level.toUpperCase()}</Tag>
                      <span style={{ color: '#8c8c8c', marginLeft: '8px' }}>{alert.time}</span>
                    </div>
                  </div>
                }
                description={
                  <div>
                    <div>{alert.message}</div>
                    <div style={{ marginTop: '4px', fontSize: '12px', color: '#8c8c8c' }}>
                      위치: {alert.location} | 신뢰도: {alert.confidence}%
                    </div>
                  </div>
                }
              />
            </List.Item>
          )}
        />
      </Card>

      <Row gutter={[16, 16]}>
        {/* 화재 추이 차트 */}
        <Col xs={24} lg={12}>
          <Card title="📈 화재 탐지 추이">
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={fireTrendData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Line type="monotone" dataKey="fires" stroke="#ff4d1a" strokeWidth={2} name="화재 수" />
                <Line type="monotone" dataKey="sensors" stroke="#1a66cc" strokeWidth={2} name="활성 센서" />
              </LineChart>
            </ResponsiveContainer>
          </Card>
        </Col>

        {/* 센서 상태 */}
        <Col xs={24} lg={12}>
          <Card title="📊 센서 상태 분포">
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sensorStatusData}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {sensorStatusData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
            <div style={{ marginTop: '16px' }}>
              {sensorStatusData.map((item, index) => (
                <div key={index} style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <span>
                    <span style={{ 
                      display: 'inline-block', 
                      width: '12px', 
                      height: '12px', 
                      backgroundColor: item.color, 
                      marginRight: '8px',
                      borderRadius: '2px'
                    }} />
                    {item.name}
                  </span>
                  <span>{item.value}개</span>
                </div>
              ))}
            </div>
          </Card>
        </Col>

        {/* 실시간 모니터링 지도 */}
        <Col xs={24}>
          <Card title="🗺️ 실시간 모니터링 지도">
            <div style={{ height: '400px', borderRadius: '8px', overflow: 'hidden' }}>
              <MapContainer
                center={[37.5665, 127.9780]}
                zoom={13}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                
                {/* 화재 위치 */}
                {fireLocations.map((fire, index) => (
                  <Marker key={`fire-${index}`} position={[fire.lat, fire.lng]}>
                    <Popup>
                      <div>
                        <h4>🔥 {fire.name}</h4>
                        <p>심각도: {fire.severity}</p>
                        <p>상태: 활성</p>
                      </div>
                    </Popup>
                  </Marker>
                ))}
                
                {/* 센서 위치 */}
                {sensorLocations.map((sensor, index) => (
                  <Marker key={`sensor-${index}`} position={[sensor.lat, sensor.lng]}>
                    <Popup>
                      <div>
                        <h4>📡 {sensor.type.toUpperCase()} 센서</h4>
                        <p>상태: {sensor.status}</p>
                      </div>
                    </Popup>
                  </Marker>
                ))}
                
                {/* 영향 반경 */}
                <Circle
                  center={[37.5665, 127.9780]}
                  radius={2000}
                  pathOptions={{ color: '#ff4d1a', fillColor: '#ff4d1a', fillOpacity: 0.1 }}
                />
              </MapContainer>
            </div>
          </Card>
        </Col>
      </Row>

      {/* 마지막 업데이트 시간 */}
      <div style={{ 
        textAlign: 'center', 
        marginTop: '24px', 
        color: '#8c8c8c',
        fontSize: '14px'
      }}>
        마지막 업데이트: {lastUpdate.toLocaleString('ko-KR')}
      </div>
    </div>
  );
};

export default Dashboard;
