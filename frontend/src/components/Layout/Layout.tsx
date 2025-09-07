import React, { useState } from 'react';
import { Layout as AntLayout, Menu, Button, Avatar, Dropdown, Space, Badge } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  FireOutlined,
  RobotOutlined,
  CheckCircleOutlined,
  FileTextOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
  BellOutlined,
  UserOutlined,
  LogoutOutlined,
  SettingOutlined,
} from '@ant-design/icons';
import type { MenuProps } from 'antd';

const { Header, Sider, Content } = AntLayout;

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [collapsed, setCollapsed] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  // 메뉴 아이템 정의
  const menuItems: MenuProps['items'] = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: '메인 대시보드',
    },
    {
      key: '/fire-detection',
      icon: <FireOutlined />,
      label: '산불 탐지',
    },
    {
      key: '/ai-recommendation',
      icon: <RobotOutlined />,
      label: 'AI 권고안',
    },
    {
      key: '/approval-process',
      icon: <CheckCircleOutlined />,
      label: '승인 프로세스',
    },
    {
      key: '/log-audit',
      icon: <FileTextOutlined />,
      label: '로그 및 감사',
    },
  ];

  // 사용자 메뉴
  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '프로필',
    },
    {
      key: 'settings',
      icon: <SettingOutlined />,
      label: '설정',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '로그아웃',
    },
  ];

  const handleMenuClick = ({ key }: { key: string }) => {
    navigate(key);
  };

  const handleUserMenuClick = ({ key }: { key: string }) => {
    switch (key) {
      case 'profile':
        // 프로필 페이지로 이동
        break;
      case 'settings':
        // 설정 페이지로 이동
        break;
      case 'logout':
        // 로그아웃 처리
        console.log('로그아웃');
        break;
    }
  };

  return (
    <AntLayout style={{ minHeight: '100vh' }}>
      <Sider 
        trigger={null} 
        collapsible 
        collapsed={collapsed}
        width={250}
        style={{
          background: '#f5f5f5',
          borderRight: '1px solid #e8e8e8',
        }}
      >
        <div style={{ 
          padding: '16px', 
          textAlign: 'center',
          borderBottom: '1px solid #e8e8e8',
          marginBottom: '16px'
        }}>
          <h2 style={{ 
            margin: 0, 
            color: '#1a66cc',
            fontSize: collapsed ? '16px' : '20px',
            fontWeight: 'bold'
          }}>
            {collapsed ? '🔥' : '🔥 산불 대응 AI Agent'}
          </h2>
        </div>
        
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
          style={{
            background: 'transparent',
            border: 'none',
          }}
        />
      </Sider>
      
      <AntLayout>
        <Header style={{ 
          padding: '0 24px', 
          background: '#1a66cc',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
        }}>
          <div style={{ display: 'flex', alignItems: 'center' }}>
            <Button
              type="text"
              icon={collapsed ? <MenuUnfoldOutlined /> : <MenuFoldOutlined />}
              onClick={() => setCollapsed(!collapsed)}
              style={{
                fontSize: '16px',
                width: 64,
                height: 64,
                color: '#fff',
              }}
            />
            <h1 style={{ 
              color: '#fff', 
              margin: 0, 
              marginLeft: '16px',
              fontSize: '24px',
              fontWeight: '600'
            }}>
              산불 대응 AI Agent 시스템
            </h1>
          </div>
          
          <Space size="middle">
            <Badge count={5} size="small">
              <Button
                type="text"
                icon={<BellOutlined />}
                style={{ color: '#fff', fontSize: '18px' }}
              />
            </Badge>
            
            <Dropdown
              menu={{ 
                items: userMenuItems,
                onClick: handleUserMenuClick
              }}
              placement="bottomRight"
            >
              <Button type="text" style={{ color: '#fff' }}>
                <Space>
                  <Avatar icon={<UserOutlined />} />
                  <span>관리자</span>
                </Space>
              </Button>
            </Dropdown>
          </Space>
        </Header>
        
        <Content style={{ 
          margin: '24px',
          padding: '24px',
          background: '#fff',
          borderRadius: '8px',
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          minHeight: 'calc(100vh - 112px)'
        }}>
          {children}
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default Layout;
