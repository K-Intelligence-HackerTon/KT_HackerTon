import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { ConfigProvider } from 'antd';
import { Toaster } from 'react-hot-toast';
import { HelmetProvider } from 'react-helmet-async';
import koKR from 'antd/locale/ko_KR';

// Components
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import FireDetection from './pages/FireDetection/FireDetection';
import AIRecommendation from './pages/AIRecommendation/AIRecommendation';
import ApprovalProcess from './pages/ApprovalProcess/ApprovalProcess';
import LogAudit from './pages/LogAudit/LogAudit';

// Styles
import './App.css';

// React Query 설정
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
      staleTime: 5 * 60 * 1000, // 5분
    },
  },
});

// Ant Design 테마 설정
const theme = {
  token: {
    colorPrimary: '#1a66cc',
    colorSuccess: '#33b233',
    colorWarning: '#ff9500',
    colorError: '#ff4d1a',
    colorInfo: '#6633cc',
    borderRadius: 8,
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
  },
  components: {
    Layout: {
      headerBg: '#1a66cc',
      siderBg: '#f5f5f5',
    },
    Card: {
      borderRadius: 12,
    },
    Button: {
      borderRadius: 8,
    },
  },
};

function App() {
  return (
    <HelmetProvider>
      <QueryClientProvider client={queryClient}>
        <ConfigProvider locale={koKR} theme={theme}>
          <Router>
            <div className="App">
              <Layout>
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/fire-detection" element={<FireDetection />} />
                  <Route path="/ai-recommendation" element={<AIRecommendation />} />
                  <Route path="/approval-process" element={<ApprovalProcess />} />
                  <Route path="/log-audit" element={<LogAudit />} />
                </Routes>
              </Layout>
              <Toaster
                position="top-right"
                toastOptions={{
                  duration: 4000,
                  style: {
                    background: '#363636',
                    color: '#fff',
                  },
                  success: {
                    duration: 3000,
                    iconTheme: {
                      primary: '#33b233',
                      secondary: '#fff',
                    },
                  },
                  error: {
                    duration: 5000,
                    iconTheme: {
                      primary: '#ff4d1a',
                      secondary: '#fff',
                    },
                  },
                }}
              />
            </div>
          </Router>
        </ConfigProvider>
      </QueryClientProvider>
    </HelmetProvider>
  );
}

export default App;
