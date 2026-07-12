import React from 'react';

const MessageBubble = ({ role, content, sources }) => {
  const isUser = role === 'user';
  
  return (
    <div className={`message-bubble-wrapper ${isUser ? 'user' : 'assistant'}`}>
      <div className={`message-bubble ${isUser ? 'user' : 'assistant'}`}>
        <div className="message-sender-tag">
          {isUser ? 'You' : 'Antigravity CodeAssistant'}
        </div>
        <div className="message-content">
          {content}
        </div>
        {!isUser && sources && sources.length > 0 && (
          <div className="message-sources-container">
            <div className="message-sources-title">📁 Ground-Truth Citations:</div>
            <div className="message-sources-list">
              {sources.map((src, i) => (
                <span key={i} className="message-source-badge" title={src}>
                  {src.split('/').pop()} {/* Show file basename, full path on hover */}
                </span>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default MessageBubble;
