import React, { useState } from 'react';
import { useRepo } from '../context/RepoContext';

const RepoInput = () => {
  const { loadRepo, isIngesting, ingestError, repoName } = useRepo();
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url.trim()) {
      loadRepo(url.trim());
    }
  };

  return (
    <div className="repo-input-container">
      <div className="repo-input-wrapper">
        <form onSubmit={handleSubmit} className="repo-input-form">
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter public GitHub repository URL (e.g. https://github.com/octocat/Spoon-Knife)"
            disabled={isIngesting}
            className="repo-url-input"
            required
          />
          <button
            type="submit"
            disabled={isIngesting || !url.trim()}
            className={`repo-submit-btn ${isIngesting ? 'loading' : ''}`}
          >
            {isIngesting ? (
              <span className="ingest-loading-text">
                Ingesting
                <span className="dot-pulse-mini"></span>
              </span>
            ) : 'Load Repo'}
          </button>
        </form>
        
        {repoName && !isIngesting && !ingestError && (
          <div className="repo-success-indicator">
            <span className="success-icon">✅</span>
            <span className="success-text">Loaded: <strong className="success-repo-name">{repoName}</strong></span>
          </div>
        )}
      </div>
      
      {ingestError && (
        <div className="repo-error-box">
          <span className="error-icon">⚠️</span>
          <span className="error-message">{ingestError}</span>
        </div>
      )}
    </div>
  );
};

export default RepoInput;
