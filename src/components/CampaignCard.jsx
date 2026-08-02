import React from 'react';
import { campaignStyles as styles } from '../styles/campaignStyles';
import { DEFAULT_APP_DONATION_URL } from '../constants/translations';

export default function CampaignCard({ campaign, t, activeCardRef, isAdmin, onApprove, onReject }) {
  const percent = Math.round((campaign.assignedUnits / campaign.totalUnits) * 100);

  const handleShare = () => {
    const inviteBody = t.getInviteText(campaign.title, campaign.intention, campaign.id);
    const shareUrl = window.location.href;
    const fullMessage = `${inviteBody}\n🔗 ${shareUrl}`;

    if (navigator.share) {
      navigator.share({ title: campaign.title, text: fullMessage, url: shareUrl }).catch(() => {});
    } else {
      navigator.clipboard.writeText(fullMessage);
      alert(t.copySuccess);
    }
  };

  const handleOpenDonation = (targetUrl) => {
    window.open(targetUrl || DEFAULT_APP_DONATION_URL, '_blank', 'noopener,noreferrer');
  };

  return (
    <div 
      ref={campaign.isPlaying ? activeCardRef : null}
      style={{ ...styles.card, ...(campaign.isPlaying ? styles.activePlayingCard : {}) }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <strong>{campaign.title}</strong>
        <span style={styles.badge}>{t.progress}: {percent}%</span>
      </div>
      <p style={styles.desc}>💡 {campaign.intention}</p>

      {campaign.status === 'active' && (
        <div style={{ display: 'flex', gap: '6px' }}>
          <button onClick={handleShare} style={styles.shareBtn}>{t.shareBtn}</button>
          <button onClick={() => handleOpenDonation(campaign.donationUrl)} style={styles.campaignSupportBtn}>{t.campaignSupportBtn}</button>
        </div>
      )}

      {campaign.status === 'pending' && isAdmin && (
        <div style={{ display: 'flex', gap: '8px', marginTop: '8px' }}>
          <button onClick={() => onApprove(campaign)} style={{ ...styles.btn, background: '#10b981' }}>{t.approvedText}</button>
          <button onClick={() => onReject(campaign.id)} style={{ ...styles.btn, background: '#ef4444' }}>{t.rejectText}</button>
        </div>
      )}
    </div>
  );
}