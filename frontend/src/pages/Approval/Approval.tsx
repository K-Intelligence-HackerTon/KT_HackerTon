// frontend/src/pages/Approval/Approval.tsx
import React, { useState } from 'react';
import './Approval.css';

const Approval: React.FC = () => {
  const [approvalHistory, setApprovalHistory] = useState([
    {
      id: 1,
      recommendationId: 1,
      title: '긴급 화재 진압 및 구조 활동 권고안',
      agency: '소방청',
      status: 'approved',
      approver: '김소방',
      approvedAt: new Date(Date.now() - 180000),
      comments: '즉시 출동하여 화재 진압 및 주민 구조 활동을 시작하겠습니다.'
    },
    {
      id: 2,
      recommendationId: 2,
      title: '산불방지 및 진화 활동 권고안',
      agency: '산림청',
      status: 'pending',
      approver: '이산림',
      approvedAt: null,
      comments: '현재 검토 중입니다.'
    }
  ]);

  const [currentApproval, setCurrentApproval] = useState({
    id: 2,
    title: '산불방지 및 진화 활동 권고안',
    agency: '산림청',
    priority: 'high',
    confidence: 89.3,
    location: '가평군 청평면',
    description: '산불 신뢰도 89.3%로 높은 수준이며, 산림청 소관 지역이므로 산림보호법에 따라 즉시 진화활동을 시작해야 합니다.',
    immediateActions: [
      {
        action: '산불진화헬기 출동',
        details: '대형 헬기 2대를 동원하여 공중 진화',
        legalBasis: '산림보호법 제35조',
        estimatedTime: '15분 이내'
      },
      {
        action: '진화대원 투입',
        details: '산불진화대 20명을 현장에 투입',
        legalBasis: '산림청 소관 산불방지 및 진화업무 규정',
        estimatedTime: '20분 이내'
      }
    ],
    legalBasis: [
      {
        law: '산림보호법',
        article: '제35조 (산불의 진화)',
        content: '산림청장은 산불이 발생한 때에는 즉시 진화활동을 하여야 한다'
      }
    ],
    expectedCost: 25000000,
    requiredResources: [
      { type: '진화헬기', count: 2, details: '대형 헬기, 소형 헬기' },
      { type: '진화대원', count: 20, details: '산불진화대, 전문진화대' },
      { type: '진화장비', count: 1, details: '진화용 물탱크, 진화용 호스' }
    ]
  });

  const [approvalComments, setApprovalComments] = useState('');

  const handleApprove = () => {
    const newApproval = {
      id: approvalHistory.length + 1,
      recommendationId: currentApproval.id,
      title: currentApproval.title,
      agency: currentApproval.agency,
      status: 'approved',
      approver: '이산림',
      approvedAt: new Date(),
      comments: approvalComments
    };
    setApprovalHistory([newApproval, ...approvalHistory]);
    setApprovalComments('');
    alert('권고안이 승인되었습니다.');
  };

  const handleReject = () => {
    const newApproval = {
      id: approvalHistory.length + 1,
      recommendationId: currentApproval.id,
      title: currentApproval.title,
      agency: currentApproval.agency,
      status: 'rejected',
      approver: '이산림',
      approvedAt: new Date(),
      comments: approvalComments
    };
    setApprovalHistory([newApproval, ...approvalHistory]);
    setApprovalComments('');
    alert('권고안이 거부되었습니다.');
  };

  return (
    <div className="approval">
      <div className="approval-header">
        <h1>승인 프로세스 - 상위 기관 검토</h1>
        <div className="approval-status">
          <span className="status-badge pending">검토 중</span>
        </div>
      </div>

      <div className="approval-content">
        <div className="approval-main">
          <div className="approval-card">
            <div className="card-header">
              <h2>{currentApproval.title}</h2>
              <div className="card-meta">
                <span className="agency">{currentApproval.agency}</span>
                <span className="priority">{currentApproval.priority}</span>
                <span className="confidence">{currentApproval.confidence}%</span>
                <span className="location">{currentApproval.location}</span>
              </div>
            </div>

            <div className="card-content">
              <div className="description">
                <h3>권고안 설명</h3>
                <p>{currentApproval.description}</p>
              </div>

              <div className="immediate-actions">
                <h3>즉시 조치사항</h3>
                <div className="actions-list">
                  {currentApproval.immediateActions.map((action, index) => (
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
                <h3>법적 근거</h3>
                <div className="legal-list">
                  {currentApproval.legalBasis.map((legal, index) => (
                    <div key={index} className="legal-item">
                      <div className="legal-law">{legal.law}</div>
                      <div className="legal-article">{legal.article}</div>
                      <div className="legal-content">{legal.content}</div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="cost-resources">
                <div className="cost-info">
                  <h3>예상 비용</h3>
                  <div className="cost-value">
                    {currentApproval.expectedCost.toLocaleString('ko-KR')}원
                  </div>
                </div>
                <div className="resources-info">
                  <h3>필요 자원</h3>
                  <div className="resources-list">
                    {currentApproval.requiredResources.map((resource, index) => (
                      <div key={index} className="resource-item">
                        <span className="resource-type">{resource.type}</span>
                        <span className="resource-count">{resource.count}개</span>
                        <span className="resource-details">{resource.details}</span>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div className="card-actions">
              <div className="approval-comments">
                <label htmlFor="comments">승인/거부 사유</label>
                <textarea
                  id="comments"
                  value={approvalComments}
                  onChange={(e) => setApprovalComments(e.target.value)}
                  placeholder="승인 또는 거부 사유를 입력하세요..."
                />
              </div>
              <div className="action-buttons">
                <button className="btn-approve" onClick={handleApprove}>
                  <span className="btn-icon">✅</span>
                  승인
                </button>
                <button className="btn-reject" onClick={handleReject}>
                  <span className="btn-icon">❌</span>
                  거부
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="approval-sidebar">
          <div className="approval-history">
            <h3>승인 이력</h3>
            <div className="history-list">
              {approvalHistory.map(approval => (
                <div key={approval.id} className={`history-item ${approval.status}`}>
                  <div className="history-header">
                    <span className="history-title">{approval.title}</span>
                    <span className={`history-status ${approval.status}`}>
                      {approval.status === 'approved' ? '승인' : 
                       approval.status === 'rejected' ? '거부' : '대기'}
                    </span>
                  </div>
                  <div className="history-meta">
                    <span className="history-agency">{approval.agency}</span>
                    <span className="history-approver">{approval.approver}</span>
                    <span className="history-time">
                      {approval.approvedAt ? 
                        approval.approvedAt.toLocaleString('ko-KR') : 
                        '대기 중'}
                    </span>
                  </div>
                  <div className="history-comments">
                    {approval.comments}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Approval;