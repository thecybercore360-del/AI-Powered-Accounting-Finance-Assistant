"use client";

import React, { useState } from "react";
import { sendChatMessage } from "../lib/api";

interface Message {
  role: "user" | "ai";
  content: string;
}

export default function Chatbot() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "ai", content: "Hello! I am your AI Accounting Assistant. You can tell me to record expenses, income, or ask for account balances." }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim()) return;

    const userMessage = input.trim();
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setInput("");
    setLoading(true);

    try {
      const response = await sendChatMessage(userMessage);
      setMessages((prev) => [...prev, { role: "ai", content: response.response }]);
    } catch (error) {
      setMessages((prev) => [...prev, { role: "ai", content: "Sorry, I encountered an error communicating with the server." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel" style={{ display: 'flex', flexDirection: 'column', height: '600px' }}>
      <h2 style={{ marginBottom: '1rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>AI Agent Chat</h2>
      
      <div style={{ flex: 1, overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '1rem', paddingRight: '10px' }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ 
            alignSelf: msg.role === 'user' ? 'flex-end' : 'flex-start',
            background: msg.role === 'user' ? 'var(--accent-color)' : 'rgba(255,255,255,0.1)',
            padding: '10px 15px',
            borderRadius: '12px',
            maxWidth: '80%'
          }}>
            {msg.content}
          </div>
        ))}
        {loading && <div style={{ alignSelf: 'flex-start', fontStyle: 'italic', color: 'gray' }}>AI is thinking...</div>}
      </div>

      <form onSubmit={handleSend} style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
        <input 
          type="text" 
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="E.g., Added 500 Rs for internet expense..." 
          style={{ flex: 1, padding: '12px', borderRadius: '8px', border: 'none', outline: 'none', background: 'rgba(0,0,0,0.2)', color: 'white' }}
          disabled={loading}
        />
        <button type="submit" className="btn-primary" style={{ padding: '12px 20px', borderRadius: '8px' }} disabled={loading}>
          Send
        </button>
      </form>
    </div>
  );
}
