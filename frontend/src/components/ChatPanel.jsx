import React, { useState, useEffect, useRef } from 'react';
import { useRepo } from '../context/RepoContext';
import { sendChatMessage } from '../api/axios';
import MessageBubble from './MessageBubble';

const ChatPanel = () => {
  const { repoName } = useRepo();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  
  const messagesEndRef = useRef(null);

  // Auto-scroll to the bottom of the list whenever messages or loading state changes
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, loading]);

  // Reset chat context when repoName changes
  useEffect(() => {
    setMessages([]);
    setInput('');
  }, [repoName]);

  const handleSend = async (e) => {
    e?.preventDefault();
    if (!input.trim() || loading || !repoName) return;

    const userQuestion = input.trim();
    setInput(''); // Clear input box
    setLoading(true);

    // Append user's question locally
    setMessages((prev) => [...prev, { role: 'user', content: userQuestion }]);

    try {
      const result = await sendChatMessage(repoName, userQuestion);
      // Append assistant's answer and sources returned by RAG
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: result.answer,
          sources: result.sources,
        },
      ]);
    } catch (err) {
      console.error('Chat error details:', err);
      const detailMsg = err.response?.data?.detail || 'Something went wrong answering that. Try again.';
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          content: detailMsg,
          sources: [],
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    // Send on Enter, allow line breaks on Shift+Enter
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="chat-panel-container">
      <div className="chat-panel-header">
        <span className="chat-panel-title">💬 CodeChat Dashboard</span>
        {repoName && <span className="chat-panel-repo-badge">{repoName}</span>}
      </div>

      <div className="chat-messages-viewport">
        {messages.length === 0 ? (
          <div className="chat-welcome-placeholder">
            <span className="welcome-icon">⚡</span>
            <h3>Ask questions about the repository</h3>
            <p>
              Once a repository is ingested, you can query its contents, inspect logic workflows, 
              and locate specific implementations.
            </p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <MessageBubble
              key={idx}
              role={msg.role}
              content={msg.content}
              sources={msg.sources}
            />
          ))
        )}
        {loading && (
          <div className="chat-loader-bubble">
            <span className="dot-pulse"></span>
            <span>Generating answer...</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSend} className="chat-input-form">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder={repoName ? "Ask a question about this repository..." : "Ingest a repository to start chatting"}
          disabled={!repoName || loading}
          className="chat-textarea-input"
          rows={1}
        />
        <button
          type="submit"
          disabled={!repoName || loading || !input.trim()}
          className="chat-send-btn"
        >
          Send
        </button>
      </form>
    </div>
  );
};

export default ChatPanel;
