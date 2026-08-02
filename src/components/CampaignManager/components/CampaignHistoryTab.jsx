import React from 'react';

export default function CampaignHistoryTab({ campaigns, styles }) {
  return (
    <div style={styles.list}>
      {campaigns.map(c => (
        <div key={c.id} style={styles.card}>
          <strong>{c.title}</strong>
          <span style={{ 
            fontSize: '11px', 
            display: 'block', 
            marginTop: '4px', 
            color: c.status === 'active' ? '#10b981' : c.status === 'pending' ? '#f59e0b' : '#ef4444' 
          }}>
            [{c.status}]
          </span>
        </div>
      ))}
    </div>
  );
}
