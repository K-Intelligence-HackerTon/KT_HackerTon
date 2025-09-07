// frontend/src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Layout from './components/Layout/Layout';
import Dashboard from './pages/Dashboard/Dashboard';
import AIRecommendation from './pages/AIRecommendation/AIRecommendation';
import Approval from './pages/Approval/Approval';
import LogAudit from './pages/LogAudit/LogAudit';
import './App.css';

const App: React.FC = () => {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/ai-recommendation" element={<AIRecommendation />} />
          <Route path="/approval" element={<Approval />} />
          <Route path="/log-audit" element={<LogAudit />} />
        </Routes>
      </Layout>
    </Router>
  );
};

export default App;