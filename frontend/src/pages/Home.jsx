import React from 'react';
import RepoInput from '../components/RepoInput';
import FileTree from '../components/FileTree';
import CodeViewer from '../components/CodeViewer';
import ChatPanel from '../components/ChatPanel';

const Home = () => {
  return (
    <div className="home-layout">
      <header className="home-header">
        <div className="logo-section">
          <span className="logo-icon">⚡</span>
          <h1 className="logo-text">CodeChat RAG</h1>
        </div>
        <RepoInput />
      </header>
      <main className="home-main-grid">
        <div className="left-sidebar-pane">
          <FileTree />
          <CodeViewer />
        </div>
        <div className="right-chat-pane">
          <ChatPanel />
        </div>
      </main>
    </div>
  );
};

export default Home;
