// frontend/src/pages/LogAudit/LogAudit.tsx
import React, { useState } from 'react';
import './LogAudit.css';

const LogAudit: React.FC = () => {
  const [activityLogs, setActivityLogs] = useState([
    {
      id: 1,
      timestamp: new Date(Date.now() - 300000),
      user: '김소방',
      action: '권고안 승인',
      details: '긴급 화재 진압 및 구조 활동 권고안을 승인했습니다.',
      ip: '192.168.1.100',
      status: 'success'
    },
    {
      id: 2,
      timestamp: new Date(Date.now() - 600000),
      user: '이산림',
      action: '권고안 검토',
      details: '산불방지 및 진화 활동 권고안을 검토 중입니다.',
      ip: '192.168.1.101',
      status: 'info'
    },
    {
      id: 3,
      timestamp: new Date(Date.now() - 900000),
      user: '박지자체',
      action: '센서 데이터 수신',
      details: '양평군 용문면 센서에서 화재 위험 데이터를 수신했습니다.',
      ip: '192.168.1.102',
      status: 'warning'
    },
    {
      id: 4,
      timestamp: new Date(Date.now() - 1200000),
      user: 'AI 시스템',
      action: '화재 탐지',
      details: 'CCTV-01에서 화재를 탐지했습니다. 신뢰도: 95.2%',
      ip: '192.168.1.103',
      status: 'critical'
    },
    {
      id: 5,
      timestamp: new Date(Date.now() - 1500000),
      user: '최관리자',
      action: '시스템 설정 변경',
      details: '화재 탐지 임계값을 85%에서 90%로 변경했습니다.',
      ip: '192.168.1.104',
      status: 'info'
    }
  ]);

  const [systemMetrics, setSystemMetrics] = useState({
    totalAlerts: 156,
    resolvedAlerts: 142,
    pendingAlerts: 14,
    systemUptime: '99.8%',
    averageResponseTime: '2.3초',
    dataProcessingRate: '1,247건/시간'
  });

  const [auditTrail, setAuditTrail] = useState([
    {
      id: 1,
      timestamp: new Date(Date.now() - 1800000),
      event: '사용자 로그인',
      user: '김소방',
      details: '소방청 계정으로 로그인했습니다.',
      severity: 'info'
    },
    {
      id: 2,
      timestamp: new Date(Date.now() - 2100000),
      event: '권한 변경',
      user: '최관리자',
      details: '이산림 사용자의 권한을 승인자로 변경했습니다.',
      severity: 'warning'
    },
    {
      id: 3,
      timestamp: new Date(Date.now() - 2400000),
      event: '데이터 백업',
      user: '시스템',
      details: '일일 데이터 백업이 완료되었습니다.',
      severity: 'info'
    }
  ]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'success': return 'success';
      case 'warning': return 'warning';
      case 'critical': return 'critical';
      case 'info': return 'info';
      default: return 'info';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'critical';
      case 'warning': return 'warning';
      case 'info': return 'info';
      default: return 'info';
    }
  };

  return (
    <div className="log-audit">
      <div className="log-audit-header">
        <h1>로그 및 감사 - 활동 기록 관리</h1>
        <div className="system-status">
          <span className="status-indicator active">시스템 정상</span>
          <span className="last-update">
            마지막 업데이트: {new Date().toLocaleString('ko-KR')}
          </span>
        </div>
      </div>

      <div className="log-audit-content">
        <div className="metrics-panel">
          <h2>시스템 메트릭</h2>
          <div className="metrics-grid">
            <div className="metric-item">
              <div className="metric-label">총 알림 수</div>
              <div className="metric-value">{systemMetrics.totalAlerts}</div>
            </div>
            <div className="metric-item">
              <div className="metric-label">해결된 알림</div>
              <div className="metric-value success">{systemMetrics.resolvedAlerts}</div>
            </div>
            <div className="metric-item">
              <div className="metric-label">대기 중인 알림</div>
              <div className="metric-value warning">{systemMetrics.pendingAlerts}</div>
            </div>
            <div className="metric-item">
              <div className="metric-label">시스템 가동률</div>
              <div className="metric-value success">{systemMetrics.systemUptime}</div>
            </div>
            <div className="metric-item">
              <div className="metric-label">평균 응답 시간</div>
              <div className="metric-value info">{systemMetrics.averageResponseTime}</div>
            </div>
            <div className="metric-item">
              <div className="metric-label">데이터 처리율</div>
              <div className="metric-value info">{systemMetrics.dataProcessingRate}</div>
            </div>
          </div>
        </div>

        <div className="logs-panel">
          <h2>활동 기록</h2>
          <div className="logs-table">
            <div className="table-header">
              <div className="col-timestamp">시간</div>
              <div className="col-user">사용자</div>
              <div className="col-action">작업</div>
              <div className="col-details">상세 내용</div>
              <div className="col-ip">IP 주소</div>
              <div className="col-status">상태</div>
            </div>
            <div className="table-body">
              {activityLogs.map(log => (
                <div key={log.id} className="table-row">
                  <div className="col-timestamp">
                    {log.timestamp.toLocaleString('ko-KR')}
                  </div>
                  <div className="col-user">{log.user}</div>
                  <div className="col-action">{log.action}</div>
                  <div className="col-details">{log.details}</div>
                  <div className="col-ip">{log.ip}</div>
                  <div className="col-status">
                    <span className={`status-badge ${getStatusColor(log.status)}`}>
                      {log.status === 'success' ? '성공' :
                       log.status === 'warning' ? '경고' :
                       log.status === 'critical' ? '위험' : '정보'}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        <div className="audit-panel">
          <h2>감사 추적</h2>
          <div className="audit-list">
            {auditTrail.map(audit => (
              <div key={audit.id} className="audit-item">
                <div className="audit-header">
                  <span className="audit-event">{audit.event}</span>
                  <span className="audit-time">
                    {audit.timestamp.toLocaleString('ko-KR')}
                  </span>
                  <span className={`audit-severity ${getSeverityColor(audit.severity)}`}>
                    {audit.severity === 'critical' ? '위험' :
                     audit.severity === 'warning' ? '경고' : '정보'}
                  </span>
                </div>
                <div className="audit-details">
                  <div className="audit-user">사용자: {audit.user}</div>
                  <div className="audit-description">{audit.details}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default LogAudit;