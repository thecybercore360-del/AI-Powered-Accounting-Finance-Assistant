"use client";

import React, { useEffect, useState } from "react";
import Chatbot from "../../components/Chatbot";
import { fetchPnLReport, fetchBalanceSheet } from "../../lib/api";

export default function Dashboard() {
  const [pl, setPl] = useState<any>(null);
  const [bs, setBs] = useState<any>(null);

  useEffect(() => {
    // Polling or initial fetch
    const loadData = async () => {
      try {
        const plData = await fetchPnLReport();
        const bsData = await fetchBalanceSheet();
        setPl(plData);
        setBs(bsData);
      } catch (err) {
        console.error(err);
      }
    };
    loadData();
    // Refresh every 5 seconds to show real-time changes
    const interval = setInterval(loadData, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <main style={{ minHeight: '100vh', position: 'relative' }}>
      <div className="bg-glow-1"></div>
      <div className="bg-glow-2"></div>
      
      <div className="container" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '2rem', textAlign: 'left' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
          
          <div className="glass-panel">
            <h2>Profit & Loss</h2>
            {pl ? (
              <div style={{ marginTop: '1rem' }}>
                <p><strong>Total Revenue:</strong> ${pl.total_revenue}</p>
                <p><strong>Total Expenses:</strong> ${pl.total_expenses}</p>
                <h3 style={{ marginTop: '10px', color: pl.net_profit >= 0 ? '#4ade80' : '#f87171' }}>
                  Net Profit: ${pl.net_profit}
                </h3>
              </div>
            ) : <p>Loading...</p>}
          </div>

          <div className="glass-panel">
            <h2>Balance Sheet</h2>
            {bs ? (
              <div style={{ marginTop: '1rem' }}>
                <p><strong>Assets:</strong> ${bs.total_assets}</p>
                <p><strong>Liabilities:</strong> ${bs.total_liabilities}</p>
                <p><strong>Equity:</strong> ${bs.total_equity}</p>
                <h3 style={{ marginTop: '10px', color: bs.is_balanced ? '#4ade80' : '#f87171' }}>
                  Balanced: {bs.is_balanced ? "Yes" : "No"}
                </h3>
              </div>
            ) : <p>Loading...</p>}
          </div>

        </div>

        <div>
          <Chatbot />
        </div>
      </div>
    </main>
  );
}
