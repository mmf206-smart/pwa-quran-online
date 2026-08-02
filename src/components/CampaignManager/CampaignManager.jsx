import React, { useRef } from 'react';
import { useAutoScroll } from '../../hooks/useAutoScroll';
import { useCampaigns } from '../../hooks/useCampaigns';
import { DEFAULT_APP_DONATION_URL } from '../../locales/translations';
import { styles } from './CampaignManager.styles';

import ActiveCampaignsTab from './components/ActiveCampaignsTab';
import PendingAdminTab from './components/PendingAdminTab';
import CampaignHistoryTab from './components/CampaignHistoryTab';
import CreateCampaignTab from './components/CreateCampaignTab';

export default function CampaignManager({ isOpen, onClose }) {
  const bodyRef = useRef(null);
  const activeCardRef = useRef(null);

  const {
    lang,
    t,
    deviceId,
    isAdmin,
    showAdminLogin,
    setShowAdminLogin,
    adminPasswordInput,
    setAdminPasswordInput,
    campaigns,
    setCampaigns,
    activeTab,
    setActiveTab,
    trustedUsers,
    bannedUsers,
    handleLangChange,
    handleAdminLogin,
    handleAdminLogout,
    handleApproveCampaign,
    handleRejectCampaign,
    handleShareCampaign,
    handleOpenDonation
  } = useCampaigns();

  const activePlayingCampaign = campaigns.find(c => c.status === 'active' && c.isPlaying);
  useAutoScroll(bodyRef, activeCardRef, !!activePlayingCampaign);

  if (!isOpen) return null;

  const isBanned = bannedUsers.includes(deviceId);
  const isTrusted = trustedUsers.includes(deviceId);
  const hasActiveCampaign = campaigns.some(c => c.creatorId === deviceId && (c.status === 'active' || c.status === 'pending'));

  const activeCampaigns = campaigns.filter(c => c.status === 'active');
  const pendingCampaigns = campaigns.filter(c => c.status === 'pending');
  const myCampaigns = campaigns.filter(c => c.creatorId === deviceId);

  const handleCampaignCreated = (newCampaign, isUserTrusted) => {
    setCampaigns(prev => [newCampaign, ...prev]);
    if (isUserTrusted) {
      alert(t.statusTrusted);
      setActiveTab('active');
    } else {
      alert(t.statusFirstTime);
      setActiveTab('myHistory');
    }
  };

  return (
    <div style={styles.overlay}>
      <div style={{ ...styles.modal, direction: t.dir }}>
        <div style={styles.header}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <h3 style={{ margin: 0, fontSize: '15px' }}>{t.title}</h3>
            <select value={lang} onChange={(e) => handleLangChange(e.target.value)} style={styles.langSelect}>
              <option value="fa">🇮🇷 فارسی</option>
              <option value="en">🇬🇧 English</option>
              <option value="ar">🇸🇦 العربية</option>
              <option value="id">🇮🇩 Bahasa</option>
            </select>
          </div>

          <div style={{ display: 'flex', gap: '6px', alignItems: 'center' }}>
            <button onClick={() => handleOpenDonation(DEFAULT_APP_DONATION_URL)} style={styles.appSupportHeaderBtn}>
              {t.appSupportBtn}
            </button>

            {!isAdmin ? (
              <button onClick={() => setShowAdminLogin(!showAdminLogin)} style={styles.adminBtn}>{t.adminLogin}</button>
            ) : (
              <button onClick={handleAdminLogout} style={{ ...styles.adminBtn, background: '#ef4444', color: '#fff' }}>{t.adminLogout}</button>
            )}
            <button onClick={onClose} style={styles.closeBtn}>✕</button>
          </div>
        </div>

        {showAdminLogin && !isAdmin && (
          <form onSubmit={handleAdminLogin} style={styles.adminForm}>
            <input 
              type="password" 
              placeholder="Pass: 123456" 
              value={adminPasswordInput} 
              onChange={(e) => setAdminPasswordInput(e.target.value)} 
              style={styles.input} 
            />
            <button type="submit" style={styles.submitBtn}>OK</button>
          </form>
        )}

        <div style={styles.statusBar}>
          {isBanned && <span style={{ color: '#dc2626' }}>{t.statusBanned}</span>}
          {!isBanned && hasActiveCampaign && <span style={{ color: '#d97706' }}>{t.statusActiveLimit}</span>}
          {!isBanned && !hasActiveCampaign && isTrusted && <span style={{ color: '#16a34a' }}>{t.statusTrusted}</span>}
          {!isBanned && !hasActiveCampaign && !isTrusted && <span style={{ color: '#0284c7' }}>{t.statusFirstTime}</span>}
        </div>

        <div style={styles.tabContainer}>
          <button style={{ ...styles.tab, borderBottom: activeTab === 'active' ? '3px solid #10b981' : 'none' }} onClick={() => setActiveTab('active')}>
            {t.activeCampaigns} ({activeCampaigns.length})
          </button>
          {isAdmin && (
            <button style={{ ...styles.tab, borderBottom: activeTab === 'pending' ? '3px solid #f59e0b' : 'none', color: '#d97706' }} onClick={() => setActiveTab('pending')}>
              {t.pendingAdmin} ({pendingCampaigns.length})
            </button>
          )}
          <button style={{ ...styles.tab, borderBottom: activeTab === 'myHistory' ? '3px solid #10b981' : 'none' }} onClick={() => setActiveTab('myHistory')}>
            {t.myHistory}
          </button>
          <button style={{ ...styles.tab, borderBottom: activeTab === 'create' ? '3px solid #10b981' : 'none' }} onClick={() => setActiveTab('create')}>
            {t.createCampaign}
          </button>
        </div>

        <div ref={bodyRef} style={styles.body}>
          {activeTab === 'active' && (
            <ActiveCampaignsTab 
              campaigns={activeCampaigns} 
              activeCardRef={activeCardRef} 
              t={t} 
              styles={styles} 
              onShare={handleShareCampaign} 
              onDonate={handleOpenDonation} 
            />
          )}

          {activeTab === 'pending' && isAdmin && (
            <PendingAdminTab 
              campaigns={pendingCampaigns} 
              t={t} 
              styles={styles} 
              onApprove={handleApproveCampaign} 
              onReject={handleRejectCampaign} 
            />
          )}

          {activeTab === 'myHistory' && (
            <CampaignHistoryTab 
              campaigns={myCampaigns} 
              styles={styles} 
            />
          )}

          {activeTab === 'create' && (
            <CreateCampaignTab 
              isBanned={isBanned} 
              hasActiveCampaign={hasActiveCampaign} 
              isTrusted={isTrusted} 
              deviceId={deviceId} 
              t={t} 
              styles={styles} 
              onCampaignCreated={handleCampaignCreated} 
              DEFAULT_APP_DONATION_URL={DEFAULT_APP_DONATION_URL} 
            />
          )}
        </div>

      </div>
    </div>
  );
}
