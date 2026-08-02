import React from 'react';

export default function ActiveCampaignsTab({ campaigns, activeCardRef, t, styles, onShare, onDonate }) {
  return (
    <div style={styles.list}>
      {campaigns.map(c => {
        const percent = Math.round((c.assignedUnits / c.totalUnits) * 100);
        return (
          <div 
            key={c.id} 
            ref={c.isPlaying ? activeCardRef : null}
            style={{ ...styles.card, ...(c.isPlaying ? styles.activePlayingCard : {}) }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
              <strong>{c.title}</strong>
              <span style={styles.badge}>{t.progress}: {percent}%</span>
            </div>
            <p style={styles.desc}>💡 {c.intention}</p>
            
            <div style={{ display: 'flex', gap: '6px' }}>
              <button onClick={() => onShare(c)} style={styles.shareBtn}>
                {t.shareBtn}
              </button>
              <button onClick={() => onDonate(c.donationUrl)} style={styles.campaignSupportBtn}>
                {t.campaignSupportBtn}
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
}
