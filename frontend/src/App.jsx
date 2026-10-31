import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

import Dashboard from './pages/Dashboard';
import NewExperiment from './pages/NewExperiment';
import CVLab from './pages/CVLab';
import PromptLab from './pages/PromptLab';
import PromptComparison from './pages/PromptComparison';
import TeachMode from './pages/TeachMode';
import Research from './pages/Research';
import History from './pages/History';
import ModelManager from './pages/ModelManager';
import About from './pages/About';

import { checkHealth, getModels } from './services/api';

export default function App() {
  const [activePage, setActivePage] = useState('dashboard');
  const [health, setHealth] = useState({ connected: false, status: 'checking' });
  const [currentModel, setCurrentModel] = useState('qwen2.5vl:3b');
  const [activeExperimentId, setActiveExperimentId] = useState(null);

  async function refreshSystemStatus() {
    try {
      const h = await checkHealth();
      setHealth(h);
      if (h?.ollama?.current_model) {
        setCurrentModel(h.ollama.current_model);
      }
    } catch (err) {
      setHealth({ connected: false, error: err.message });
    }
  }

  useEffect(() => {
    refreshSystemStatus();
    const interval = setInterval(refreshSystemStatus, 15000);
    return () => clearInterval(interval);
  }, []);

  function handleExperimentCompleted(expId) {
    setActiveExperimentId(expId);
    setActivePage('compare');
  }

  function handleSelectExperiment(expId) {
    setActiveExperimentId(expId);
    setActivePage('compare');
  }

  return (
    <div className="app-container">
      {/* Left Navigation Sidebar */}
      <Sidebar 
        activePage={activePage} 
        onSelectPage={setActivePage} 
      />

      {/* Main Workspace Viewport */}
      <div className="main-content">
        <Navbar 
          health={health}
          currentModel={currentModel}
          onRefreshStatus={refreshSystemStatus}
        />

        <main className="page-body">
          {activePage === 'dashboard' && (
            <Dashboard 
              onNavigate={setActivePage}
              currentModel={currentModel}
              health={health}
            />
          )}

          {activePage === 'new-experiment' && (
            <NewExperiment 
              onNavigate={setActivePage}
              currentModel={currentModel}
              onExperimentCompleted={handleExperimentCompleted}
            />
          )}

          {activePage === 'cv-lab' && (
            <CVLab />
          )}

          {activePage === 'pe-lab' && (
            <PromptLab />
          )}

          {activePage === 'compare' && (
            <PromptComparison 
              activeExperimentId={activeExperimentId}
            />
          )}

          {activePage === 'teach' && (
            <TeachMode />
          )}

          {activePage === 'research' && (
            <Research />
          )}

          {activePage === 'history' && (
            <History 
              onSelectExperiment={handleSelectExperiment}
              onNavigate={setActivePage}
            />
          )}

          {activePage === 'models' && (
            <ModelManager 
              currentModel={currentModel}
              onModelChanged={setCurrentModel}
              onRefreshHealth={refreshSystemStatus}
            />
          )}

          {activePage === 'about' && (
            <About />
          )}
        </main>
      </div>
    </div>
  );
}
