import React from 'react';

export default function Home() {
  return (
    <main style={{ position: 'relative', overflow: 'hidden', minHeight: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <div className="bg-glow-1"></div>
      <div className="bg-glow-2"></div>
      
      <div className="container">
        <div className="glass-panel" style={{ maxWidth: '800px', margin: '0 auto', textAlign: 'center' }}>
          <h1>AI-Powered Accounting</h1>
          <p className="subtitle">
            Welcome to the future of finance. Seamless double-entry bookkeeping, anomaly audits, and dynamic reports—all powered by Groq AI.
          </p>
          
          <button className="btn-primary">
            Enter Dashboard
          </button>
        </div>
      </div>
    </main>
  );
}
