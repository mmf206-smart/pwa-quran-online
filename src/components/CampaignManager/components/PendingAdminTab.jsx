import React from 'react';

export default function PendingAdminTab({ campaigns, t, styles, onApprove, onReject }) {
  return (
    <div style={styles.list}>
      {campaigns.map(c => (
        <div key={c.id} style={{ ...styles.card, background: '#fffbeb', borderColor: '#f59e0b' }}>
          <strong>{c.title}</strong>
          <p style={styles.desc}>💡 {c.intention}</p>
          <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
            <button onClick={() => onApprove(c)} style={{ ...styles.btn, background: '#10b981' }}>
              {t.approvedText}
            </button>
            <button onClick={() => onReject(c.id)} style={{ ...styles.btn, background: '#ef4444' }}>
              {t.rejectText}
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}
