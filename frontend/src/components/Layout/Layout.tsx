// frontend/src/components/Layout/Layout.tsx
import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const location = useLocation();

  const menuItems = [
    { path: '/dashboard', label: '대시보드', icon: '📊' },
    { path: '/ai-recommendation', label: 'AI 권고안', icon: '🤖' },
    { path: '/approval', label: '승인 프로세스', icon: '✅' },
    { path: '/log-audit', label: '로그 및 감사', icon: '📋' }
  ];

  return (
    <div className="layout">
      <div className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <div className="logo">
            <div className="logo-icon">🚨</div>
            {sidebarOpen && (
              <div className="logo-text">
                <h2>산불 대응 AI</h2>
                <p>믿:음 2.0</p>
              </div>
            )}
          </div>
          <button 
            className="sidebar-toggle"
            onClick={() => setSidebarOpen(!sidebarOpen)}
          >
            {sidebarOpen ? '◀' : '▶'}
          </button>
        </div>
        <nav className="sidebar-nav">
          {menuItems.map(item => (
            <Link
              key={item.path}
              to={item.path}
              className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
            >
              <div className="nav-icon">{item.icon}</div>
              {sidebarOpen && <span className="nav-label">{item.label}</span>}
            </Link>
          ))}
        </nav>
        {sidebarOpen && (
          <div className="sidebar-footer">
            <div className="system-info">
              <div className="status-indicator active"></div>
              <span>시스템 정상</span>
            </div>
          </div>
        )}
      </div>
      
      <div className="main-content">
        <header className="header">
          <div className="header-left">
            <div className="breadcrumb">
              <span className="breadcrumb-item">홈</span>
              <span className="breadcrumb-separator">/</span>
              <span className="breadcrumb-current">
                {menuItems.find(item => item.path === location.pathname)?.label || '대시보드'}
              </span>
            </div>
          </div>
          <div className="header-right">
            <div className="header-actions">
              <div className="notification-bell">
                <span className="bell-icon">🔔</span>
                <div className="notification-badge">3</div>
              </div>
              <div className="user-info">
                <div className="user-avatar">👨‍💼</div>
                <div className="user-details">
                  <span className="user-name">관리자</span>
                  <span className="user-role">시스템 관리자</span>
                </div>
              </div>
            </div>
          </div>
        </header>
        
        <main className="content">
          {children}
        </main>
      </div>
    </div>
  );
};

export default Layout;