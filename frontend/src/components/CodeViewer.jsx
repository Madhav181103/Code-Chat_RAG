import React, { useEffect, useState } from 'react';
import { useRepo } from '../context/RepoContext';
import { getFileContent } from '../api/axios';

const CodeViewer = () => {
  const { repoName, selectedFile } = useRepo();
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!selectedFile || !repoName) {
      setContent('');
      setError(null);
      return;
    }

    const fetchFileContent = async () => {
      setLoading(true);
      setError(null);
      try {
        const result = await getFileContent(repoName, selectedFile);
        setContent(result.content);
      } catch (err) {
        console.error('Error fetching file content:', err);
        setError('Failed to load file content.');
      } finally {
        setLoading(false);
      }
    };

    fetchFileContent();
  }, [selectedFile, repoName]);

  if (!selectedFile) {
    return (
      <div className="code-viewer-placeholder">
        <p>Select a file from the list to view its code content.</p>
      </div>
    );
  }

  return (
    <div className="code-viewer-container">
      <div className="code-viewer-header">
        <span className="code-viewer-filepath">{selectedFile}</span>
      </div>
      <div className="code-viewer-body">
        {loading ? (
          <div className="code-viewer-loader">Loading file content...</div>
        ) : error ? (
          <div className="code-viewer-error">{error}</div>
        ) : (
          /* MVP Design Choice:
             Rendering raw file text inside a standard <pre><code> block satisfies 
             the requirement of displaying file content. Syntax highlighting (using 
             libraries like Prism.js or react-syntax-highlighter) is a highly visual 
             improvement left for future roadmap phases and is not required for MVP. */
          <pre className="code-viewer-pre">
            <code className="code-viewer-code">{content}</code>
          </pre>
        )}
      </div>
    </div>
  );
};

export default CodeViewer;
