// frontend/src/pages/AIRecommendation/AIRecommendation.tsx - 수정
import React, { useState, useEffect } from 'react';
import './AIRecommendation.css';

const AIRecommendation: React.FC = () => {
  const [recommendations, setRecommendations] = useState([
    {
      id: 1,
      agency: '소방청',
      title: '긴급 화재 진압 및 구조 활동 권고안',
      confidence: 97.9,
      priority: 'critical',
      status: 'pending',
      createdAt: new Date(Date.now() - 300000),
      location: '양평군 용문면',
      immediateActions: [
        {
          action: '119 신고 및 긴급 출동',
          details: '화재 현장으로 즉시 소방차량 3대 출동',
          legalBasis: '소방기본법 제3조',
          estimatedTime: '5분 이내'
        },
        {
          action: '주민 대피소 확보',
          details: '용문초등학교를 임시 대피소로 지정',
          legalBasis: '재난 및 안전관리기본법 제38조',
          estimatedTime: '10분 이내'
        }
      ],
      legalBasis: [
        {
          law: '소방기본법',
          article: '제3조 (소방활동)',
          content: '소방서장은 화재가 발생한 때에는 즉시 소방활동을 하여야 한다'
        },
        {
          law: '재난 및 안전관리기본법',
          article: '제38조 (긴급대피명령)',
          content: '시장·군수·구청장은 재난이 발생하거나 발생할 우려가 있는 경우 긴급대피명령을 발할 수 있다'
        }
      ],
      expectedCost: 15000000,
      expectedEffect: {
        '화재 진압 시간': '30분 이내',
        '주민 대피율': '95% 이상',
        '재산 피해 최소화': '80% 이상'
      },
      requiredResources: [
        { type: '소방차량', count: 3, details: '물탱크차, 구조차, 구급차' },
        { type: '소방관', count: 12, details: '구조대, 진압대, 구급대' },
        { type: '장비', count: 1, details: '고압수포, 소화기, 구조장비' }
      ],
      aiReasoning: '화재 신뢰도 95.2%로 매우 높은 수준이며, 풍속 12.4m/s로 화재 확산 위험이 크므로 즉시 대응이 필요합니다. 소방기본법에 따라 119 신고 후 5분 이내 출동하여 화재를 진압하고, 재난 및 안전관리기본법에 따라 주민을 안전한 장소로 대피시켜야 합니다.'
    }
  ]);

  const [selectedRecommendation, setSelectedRecommendation] = useState<number | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);

  // 시연용 권고안 생성 시뮬레이션
  useEffect(() => {
    const timer = setInterval(() => {
      if (Math.random() < 0.3) { // 30% 확률로 새 권고안 생성
        setIsGenerating(true);
        
        setTimeout(() => {
          const newRecommendation = {
            id: Date.now(),
            agency: ['소방청', '산림청', '지자체'][Math.floor(Math.random() * 3)],
            title: [
              '긴급 화재 진압 및 구조 활동 권고안',
              '산불방지 및 진화 활동 권고안',
              '주민 안전 및 대피 활동 권고안'
            ][Math.floor(Math.random() * 3)],
            confidence: Math.random() * 20 + 80,
            priority: Math.random() > 0.5 ? 'critical' : 'high',
            status: 'pending',
            createdAt: new Date(),
            location: ['양평군 용문면', '가평군 청평면', '포천군 내촌면'][Math.floor(Math.random() * 3)],
            immediateActions: [
              {
                action: '긴급 출동',
                details: '현장으로 즉시 출동',
                legalBasis: '관련 법령',
                estimatedTime: '5분 이내'
              }
            ],
            legalBasis: [
              {
                law: '관련 법령',
                article: '제1조',
                content: '긴급상황 시 즉시 대응'
              }
            ],
            expectedCost: Math.floor(Math.random() * 20000000) + 10000000,
            expectedEffect: {
              '대응 시간': '30분 이내',
              '성공률': '90% 이상'
            },
            requiredResources: [
              { type: '인력', count: 10, details: '전문가, 현장요원' },
              { type: '장비', count: 5, details: '필수 장비' }
            ],
            aiReasoning: 'AI 분석 결과에 따른 권고안입니다.'
          };
          
          setRecommendations(prev => [newRecommendation, ...prev.slice(0, 4)]);
          setIsGenerating(false);
        }, 2000);
      }
    }, 5000);

    return () => clearInterval(timer);
  }, []);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical': return 'critical';
      case 'high': return 'warning';
      case 'medium': return 'normal';
      default: return 'normal';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'pending': return 'pending';
      case 'approved': return 'approved';
      case 'rejected': return 'rejected';
      default: return 'pending';
    }
  };

  const handleApprove = (id: number) => {
    setRecommendations(prev => 
      prev.map(rec => 
        rec.id === id ? { ...rec, status: 'approved' } : rec
      )
    );
  };

  const handleReject = (id: number) => {
    setRecommendations(prev => 
      prev.map(rec => 
        rec.id === id ? { ...rec, status: 'rejected' } : rec
      )
    );
  };

  return (
    <div className="ai-recommendation">
      <div className="recommendation-header">
        <div className="header-content">
          <div className="header-title">
            <div className="title-icon">🤖</div>
            <div className="title-text">
              <h1>AI 권고안 생성</h1>
              <p>믿:음 2.0 LLM 기반 지능형 권고 시스템</p>
            </div>
          </div>
          <div className="header-info">
            <div className="llm-status">
              <div className="status-indicator active"></div>
              <span>믿:음 2.0 LLM 활성</span>
            </div>
            <div className="confidence-display">
              <span className="confidence-label">신뢰도</span>
              <span className="confidence-value">97.9%</span>
            </div>
            {isGenerating && (
              <div className="generating-indicator">
                <div className="loading-spinner"></div>
                <span>생성 중...</span>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="recommendation-list">
        {recommendations.map(rec => (
          <div key={rec.id} className={`recommendation-card ${getPriorityColor(rec.priority)}`}>
            <div className="card-header">
              <div className="card-title">
                <h3>{rec.title}</h3>
                <div className="card-meta">
                  <span className="agency">{rec.agency}</span>
                  <span className="location">{rec.location}</span>
                  <span className="created-at">
                    {rec.createdAt.toLocaleString('ko-KR')}
                  </span>
                </div>
              </div>
              <div className="card-badges">
                <span className={`priority-badge ${getPriorityColor(rec.priority)}`}>
                  {rec.priority === 'critical' ? '긴급' : 
                   rec.priority === 'high' ? '높음' : '보통'}
                </span>
                <span className={`status-badge ${getStatusColor(rec.status)}`}>
                  {rec.status === 'pending' ? '대기' : 
                   rec.status === 'approved' ? '승인' : '거부'}
                </span>
                <span className="confidence-badge">
                  {rec.confidence.toFixed(1)}%
                </span>
              </div>
            </div>

            <div className="card-content">
              <div className="immediate-actions">
                <h4>즉시 조치사항</h4>
                <div className="actions-list">
                  {rec.immediateActions.map((action, index) => (
                    <div key={index} className="action-item">
                      <div className="action-title">{action.action}</div>
                      <div className="action-details">{action.details}</div>
                      <div className="action-meta">
                        <span className="legal-basis">법적 근거: {action.legalBasis}</span>
                        <span className="estimated-time">예상 시간: {action.estimatedTime}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="legal-basis">
                <h4>법적 근거</h4>
                <div className="legal-list">
                  {rec.legalBasis.map((legal, index) => (
                    <div key={index} className="legal-item">
                      <div className="legal-law">{legal.law}</div>
                      <div className="legal-article">{legal.article}</div>
                      <div className="legal-content">{legal.content}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="cost-effect">
                <div className="cost-info">
                  <h4>예상 비용</h4>
                  <div className="cost-value">
                    {rec.expectedCost.toLocaleString('ko-KR')}원
                  </div>
                </div>
                <div className="effect-info">
                  <h4>예상 효과</h4>
                  <div className="effect-list">
                    {Object.entries(rec.expectedEffect).map(([key, value]) => (
                      <div key={key} className="effect-item">
                        <span className="effect-key">{key}</span>
                        <span className="effect-value">{value}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              <div className="required-resources">
                <h4>필요 자원</h4>
                <div className="resources-list">
                  {rec.requiredResources.map((resource, index) => (
                    <div key={index} className="resource-item">
                      <span className="resource-type">{resource.type}</span>
                      <span className="resource-count">{resource.count}개</span>
                      <span className="resource-details">{resource.details}</span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="ai-reasoning">
                <h4>AI 추론 과정</h4>
                <div className="reasoning-content">
                  {rec.aiReasoning}
                </div>
              </div>
            </div>

            <div className="card-actions">
              <button 
                className="btn-approve"
                onClick={() => handleApprove(rec.id)}
                disabled={rec.status !== 'pending'}
              >
                승인
              </button>
              <button 
                className="btn-reject"
                onClick={() => handleReject(rec.id)}
                disabled={rec.status !== 'pending'}
              >
                거부
              </button>
              <button className="btn-details">상세보기</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default AIRecommendation;