import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Tag, Progress, Button, Descriptions, List, Avatar, Alert, Space, Divider } from 'antd';
import { 
  FireOutlined, 
  RobotOutlined, 
  CheckCircleOutlined, 
  ClockCircleOutlined,
  DollarOutlined,
  TeamOutlined,
  ToolOutlined,
  ReloadOutlined,
  DownloadOutlined
} from '@ant-design/icons';

const AIRecommendation: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [recommendations, setRecommendations] = useState([
    {
      id: 1,
      agency: '소방청',
      title: '🚒 소방청 긴급 대응 권고안 - 양평군 용문면',
      description: '화재 위험도 87.3%에 따른 소방청 긴급 대응 방안',
      priority: 'high',
      aiConfidence: 97.9,
      status: 'pending',
      createdAt: '2024-01-01 14:25:15',
      location: '경기도 양평군 용문면',
      immediateActions: [
        {
          action: '헬기 긴급 투입',
          details: '소방헬기 2대 (Bell 412, AS-350) 즉시 출동',
          legalBasis: '소방기본법 제3조 제1항',
          estimatedTime: '10분 이내'
        },
        {
          action: '소방차량 및 인력 투입',
          details: '소방차 5대 (물탱크차 3대, 펌프차 2대) 현장 투입, 구조대 20명 긴급 파견',
          legalBasis: '소방법 제5조 제2항',
          estimatedTime: '15분 이내'
        },
        {
          action: '현장 지휘소 설치',
          details: '통합지휘체계 구축 및 현장 상황실 운영',
          legalBasis: '소방기본법 제3조 제2항',
          estimatedTime: '20분 이내'
        }
      ],
      legalBasis: [
        {
          law: '소방기본법',
          article: '제3조',
          content: '소방의 임무 및 소방기관의 조직'
        },
        {
          law: '소방법',
          article: '제5조',
          content: '소방대의 설치 및 운영'
        },
        {
          law: '소방시설 설치·유지 및 안전관리에 관한 법률',
          article: '제3조',
          content: '소방시설의 설치 및 유지'
        }
      ],
      expectedCost: 25000000,
      expectedEffect: {
        fireSuppressionRate: 0.95,
        damageReduction: 0.5,
        responseTime: '15분 이내',
        resourceUtilization: '최적화'
      },
      requiredResources: [
        { type: '헬기', count: 2, model: 'Bell 412, AS-350' },
        { type: '소방차', count: 5, type: '물탱크차 3대, 펌프차 2대' },
        { type: '인력', count: 20, role: '구조대' },
        { type: '장비', items: ['펌프', '호스', '진화제', '구조장비'] }
      ],
      aiReasoning: '센서 데이터 분석 결과 화재 위험도 87.3%로 판단되어 긴급 대응이 필요합니다.',
      affectedRadius: 2.0
    },
    {
      id: 2,
      agency: '산림청',
      title: '🌲 산림청 산불방지 권고안 - 양평군 용문면',
      description: '산림 보호를 위한 산불방지 및 진화업무 권고안',
      priority: 'high',
      aiConfidence: 96.8,
      status: 'pending',
      createdAt: '2024-01-01 14:25:15',
      location: '경기도 양평군 용문면',
      immediateActions: [
        {
          action: '산림헬기 긴급 투입',
          details: '산림헬기 2대 (K-32, Bell 205) 즉시 출동',
          legalBasis: '산림보호법 제2조 제1항',
          estimatedTime: '12분 이내'
        },
        {
          action: '산불진화대 및 장비 투입',
          details: '산불진화대 30명 현장 파견, 진화장비 긴급 보급',
          legalBasis: '산림보호법 제2조 제2항',
          estimatedTime: '18분 이내'
        },
        {
          action: '산불 확산 차단 작업',
          details: '산불 확산 경로 차단선 구축 및 예방적 진화작업',
          legalBasis: '산림보호법 제2조 제3항',
          estimatedTime: '25분 이내'
        }
      ],
      legalBasis: [
        {
          law: '산림보호법',
          article: '제2조',
          content: '산불방지 및 진화업무'
        },
        {
          law: '산림청 소관 산불방지 및 진화업무 규정',
          article: '제3조',
          content: '산불진화대의 구성 및 운영'
        }
      ],
      expectedCost: 18000000,
      expectedEffect: {
        forestDamageReduction: 0.6,
        ecosystemPreservation: 0.9,
        responseTime: '20분 이내',
        resourceEfficiency: '최적화'
      },
      requiredResources: [
        { type: '산림헬기', count: 2, model: 'K-32, Bell 205' },
        { type: '진화대', count: 30, role: '산불진화대' },
        { type: '진화장비', items: ['펌프', '호스', '삽', '괭이'] },
        { type: '진화차', count: 3, type: '산불진화차' }
      ],
      aiReasoning: '산림 생태계 보전을 위한 전문적 진화작업이 필요합니다.',
      affectedRadius: 3.0
    },
    {
      id: 3,
      agency: '지자체',
      title: '🏛️ 지자체 재난대응 권고안 - 양평군 용문면',
      description: '주민 안전을 위한 지자체 재난대응 방안',
      priority: 'high',
      aiConfidence: 98.1,
      status: 'pending',
      createdAt: '2024-01-01 14:25:15',
      location: '경기도 양평군 용문면',
      immediateActions: [
        {
          action: '주민 대피 및 안전조치',
          details: '주민 대피 안내 (반경 1km), 긴급재난문자 발송, 대피소 운영',
          legalBasis: '재난기본법 제3조 제1항',
          estimatedTime: '10분 이내'
        },
        {
          action: '교통 통제 및 우회로 안내',
          details: '현장 반경 2km 교통 통제, 우회로 안내, 응급차량 통행로 확보',
          legalBasis: '도로교통법 제5조',
          estimatedTime: '15분 이내'
        },
        {
          action: '의료 및 응급상황 대비',
          details: '의료진 대기, 응급실 준비, 응급환자 이송체계 구축',
          legalBasis: '의료법 제3조',
          estimatedTime: '20분 이내'
        }
      ],
      legalBasis: [
        {
          law: '재난 및 안전관리기본법',
          article: '제3조',
          content: '재난관리책임기관의 임무'
        },
        {
          law: '지방자치법',
          article: '제9조',
          content: '지방자치단체의 사무'
        }
      ],
      expectedCost: 8000000,
      expectedEffect: {
        residentSafety: 1.0,
        evacuationTime: '30분 이내',
        trafficManagement: '효율적',
        medicalSupport: '24시간 대기'
      },
      requiredResources: [
        { type: '대피소', count: 1, capacity: 500, location: '○○초등학교' },
        { type: '교통관제', count: 10, role: '교통관제요원' },
        { type: '의료진', count: 5, role: '응급의료진' },
        { type: '통신장비', items: ['무전기', '재난문자발송시스템'] }
      ],
      aiReasoning: '주민 안전 확보를 위한 종합적 재난대응이 필요합니다.',
      affectedRadius: 1.0
    }
  ]);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return '#ff4d1a';
      case 'high': return '#ff9500';
      case 'medium': return '#1a66cc';
      case 'low': return '#33b233';
      default: return '#8c8c8c';
    }
  };

  const getAgencyIcon = (agency: string) => {
    switch (agency) {
      case '소방청': return '🚒';
      case '산림청': return '🌲';
      case '지자체': return '🏛️';
      default: return '🏢';
    }
  };

  const getAgencyColor = (agency: string) => {
    switch (agency) {
      case '소방청': return '#ff4d1a';
      case '산림청': return '#33b233';
      case '지자체': return '#6633cc';
      default: return '#8c8c8c';
    }
  };

  const handleRefresh = () => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('ko-KR', {
      style: 'currency',
      currency: 'KRW',
      minimumFractionDigits: 0
    }).format(amount);
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
          🤖 AI 권고안 생성 - 믿:음 LLM 기반
        </h1>
        <Space>
          <Button 
            type="primary" 
            icon={<ReloadOutlined />} 
            onClick={handleRefresh}
            loading={loading}
          >
            새로고침
          </Button>
          <Button icon={<DownloadOutlined />}>
            내보내기
          </Button>
        </Space>
      </div>

      {/* 상태 정보 */}
      <Alert
        message="기관별 맞춤형 대응 방안 생성 중"
        description="신뢰도: 97.9% | 생성 시간: 2.3초 | 모델: 믿:음-2.0"
        type="info"
        showIcon
        style={{ marginBottom: '24px' }}
      />

      {/* 권고안 목록 */}
      <Row gutter={[24, 24]}>
        {recommendations.map((rec) => (
          <Col xs={24} key={rec.id}>
            <Card
              title={
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                  <span style={{ fontSize: '24px' }}>{getAgencyIcon(rec.agency)}</span>
                  <span style={{ color: getAgencyColor(rec.agency), fontWeight: '600' }}>
                    {rec.agency} 권고안
                  </span>
                  <Tag color={getPriorityColor(rec.priority)}>
                    {rec.priority.toUpperCase()}
                  </Tag>
                  <Tag color="blue">
                    AI 신뢰도: {rec.aiConfidence}%
                  </Tag>
                </div>
              }
              extra={
                <Space>
                  <Tag color="orange">대기 중</Tag>
                  <Button type="primary" size="small">
                    승인하기
                  </Button>
                </Space>
              }
              style={{ marginBottom: '16px' }}
            >
              <Descriptions column={2} size="small" style={{ marginBottom: '16px' }}>
                <Descriptions.Item label="생성 시간">{rec.createdAt}</Descriptions.Item>
                <Descriptions.Item label="위치">{rec.location}</Descriptions.Item>
                <Descriptions.Item label="영향 반경">{rec.affectedRadius}km</Descriptions.Item>
                <Descriptions.Item label="예상 비용">{formatCurrency(rec.expectedCost)}</Descriptions.Item>
              </Descriptions>

              <Divider />

              {/* 즉시 조치사항 */}
              <div style={{ marginBottom: '16px' }}>
                <h4 style={{ color: '#333', marginBottom: '12px' }}>즉시 조치사항:</h4>
                <List
                  dataSource={rec.immediateActions}
                  renderItem={(action) => (
                    <List.Item>
                      <List.Item.Meta
                        avatar={<Avatar icon={<CheckCircleOutlined />} style={{ backgroundColor: '#33b233' }} />}
                        title={action.action}
                        description={
                          <div>
                            <div>{action.details}</div>
                            <div style={{ marginTop: '4px', fontSize: '12px', color: '#8c8c8c' }}>
                              법적 근거: {action.legalBasis} | 예상 시간: {action.estimatedTime}
                            </div>
                          </div>
                        }
                      />
                    </List.Item>
                  )}
                />
              </div>

              <Row gutter={[16, 16]}>
                {/* 법적 근거 */}
                <Col xs={24} md={12}>
                  <Card size="small" title="법적 근거 및 기준">
                    <List
                      dataSource={rec.legalBasis}
                      renderItem={(basis) => (
                        <List.Item>
                          <div>
                            <strong>{basis.law} {basis.article}</strong>
                            <div style={{ fontSize: '12px', color: '#8c8c8c' }}>
                              {basis.content}
                            </div>
                          </div>
                        </List.Item>
                      )}
                    />
                  </Card>
                </Col>

                {/* 예상 비용 및 효과 */}
                <Col xs={24} md={12}>
                  <Card size="small" title="예상 비용 및 효과">
                    <div style={{ marginBottom: '12px' }}>
                      <strong>예상 비용:</strong> {formatCurrency(rec.expectedCost)}
                    </div>
                    <div style={{ marginBottom: '12px' }}>
                      <strong>예상 효과:</strong>
                      <ul style={{ margin: '4px 0', paddingLeft: '20px' }}>
                        {Object.entries(rec.expectedEffect).map(([key, value]) => (
                          <li key={key}>
                            {key}: {typeof value === 'number' ? `${(value * 100).toFixed(0)}%` : value}
                          </li>
                        ))}
                      </ul>
                    </div>
                  </Card>
                </Col>

                {/* 필요 자원 */}
                <Col xs={24}>
                  <Card size="small" title="필요 자원">
                    <List
                      dataSource={rec.requiredResources}
                      renderItem={(resource) => (
                        <List.Item>
                          <List.Item.Meta
                            avatar={<Avatar icon={<ToolOutlined />} style={{ backgroundColor: '#1a66cc' }} />}
                            title={`${resource.type} ${resource.count || ''}${resource.model || ''}`}
                            description={
                              resource.items ? resource.items.join(', ') : 
                              resource.role ? resource.role : 
                              resource.location ? resource.location : ''
                            }
                          />
                        </List.Item>
                      )}
                    />
                  </Card>
                </Col>
              </Row>

              {/* AI 추론 과정 */}
              <Card size="small" title="AI 신뢰도 및 검증 정보" style={{ marginTop: '16px' }}>
                <div style={{ marginBottom: '8px' }}>
                  <strong>믿:음 LLM 신뢰도:</strong> {rec.aiConfidence}% (법령 기반 분석)
                </div>
                <div style={{ marginBottom: '8px' }}>
                  <strong>검증 완료:</strong> {rec.agency} 산불대응 매뉴얼 2024 v3.2
                </div>
                <div style={{ marginBottom: '8px' }}>
                  <strong>실시간 업데이트:</strong> 기상청 날씨 데이터, 현장 상황 보고
                </div>
                <div style={{ marginBottom: '8px' }}>
                  <strong>법령 준수도:</strong> 100% (관련 법령 완전 준수)
                </div>
                <div>
                  <strong>과거 사례 분석:</strong> 유사 산불 사례 15건 분석 기반
                </div>
              </Card>
            </Card>
          </Col>
        ))}
      </Row>
    </div>
  );
};

export default AIRecommendation;
