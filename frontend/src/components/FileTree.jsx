import React from 'react';
import { useRepo } from '../context/RepoContext';

const FileTree = () => {
  const { files, selectedFile, setSelectedFile } = useRepo();

  if (!files || files.length === 0) {
    return (
      <div className="file-tree-empty">
        <span className="info-icon">📁</span>
        <p>No repository loaded yet. Enter a GitHub link above to get started.</p>
      </div>
    );
  }

  return (
    <div className="file-tree-container">
      <h3 className="file-tree-header">Repository Files</h3>
      <ul className="file-tree-list">
        {files.map((path) => {
          // MVP Design Choice:
          // A flat, sorted list of relative file paths is used here as a clean, reliable v1 layout.
          // While a nested tree structure (with collapsible directory folders) is a "nice-to-have" 
          // visual polish element for the future, a flat scrollable list works perfectly for MVP testing 
          // and keeps component state simpler.
          const isSelected = selectedFile === path;
          return (
            <li
              key={path}
              onClick={() => setSelectedFile(path)}
              className={`file-tree-item ${isSelected ? 'selected' : ''}`}
              title={path}
            >
              <span className="file-icon">📄</span>
              <span className="file-name">{path}</span>
            </li>
          );
        })}
      </ul>
    </div>
  );
};

export default FileTree;
