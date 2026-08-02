import React, { useState, useRef } from 'react';
import { TRANSLATIONS } from './constants/translations';
import { campaignStyles as styles } from './styles/campaignStyles';
import { useCampaigns } from './hooks/useCampaigns';
import { useAutoScroll } from './hooks/useAutoScroll';
import CampaignHeader from './components/CampaignHeader';
import CampaignCard from './components/CampaignCard';
import CampaignForm from './components/CampaignForm';

export default function CampaignManager({ isOpen, onClose }) {
  const [lang, setLang] = useState(() => localStorage.getItem('merajLang') || 'fa');
  const t = TRANSLATIONS[lang] || TRANSLATIONS.fa;

  const [activeTab, setActiveTab] = useState('active');
  const bodyRef = useRef(null);
  const activeCardRef = useRef(null);

  const {
    deviceId,
    isAdmin,
    setIsAdmin,
    isBanned,
    isTrusted,
    hasActiveCampaign,
    campaigns,
    createCampaign,
    approveCampaign,
    rejectCampaign
  } = useCampaigns();

  const activePlayingCampaign = campaigns.find(c => c.status === 'active' && c.isPlaying);
  useAutoScroll(bodyRef, activeCardRef, !!activePlayingCampaign);

  const handleFormSubmit = (formData) => {
    const status = createCampaign(formData);
    if (status === 'active') {
      alert(t.statusTrusted);
      setActiveTab('active');
    } else {
      alert(t.statusFirstTime);
      setActiveTab('myHistory');
    }
  };

  if (!isOpen) return null;

  const activeCampaigns = campaigns.filter(c => c.status === 'active');
  const pendingCampaigns = campaigns.filter(c => c.status === 'pending');
  const myCampaigns = campaigns.filter(c => c.creatorId === deviceId);

  return (
    <div style={styles.overlay}>
      <div style={{ ...styles.modal, direction: t.dir }}>
        
        {/* ۱. هدر معراج */}
        <CampaignHeader 
          t={t} 
          lang={lang} 
          setLang={(l) => { setLang(l); localStorage.setItem('merajLang', l); }} 
          isAdmin={isAdmin} 
          setIsAdmin={setIsAdmin} 
          onClose={onClose} 
        />

        {/* ۲. نوار وضعیت */}
        <div style={styles.statusBar}>
          {isBanned && <span style={{ color: '#dc2626' }}>{t.statusBanned}</span>}
          {!isBanned && hasActiveCampaign && <span style={{ color: '#d97706' }}>{t.statusActiveLimit}</span>}
          {!isBanned && !hasActiveCampaign && isTrusted && <span style={{ color: '#16a34a' }}>{t.statusTrusted}</span>}
          {!isBanned && !hasActiveCampaign && !isTrusted && <span style={{ color: '#0284c7' }}>{t.statusFirstTime}</span>}
        </div>

        {/* ۳. تب‌ها */}
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

        {/* ۴. محتوای تب‌ها همراه با هوک اسکرول */}
        <div ref={bodyRef} style={styles.body}>

          {activeTab === 'active' && (
            <div style={styles.list}>
              {activeCampaigns.map(c => (
                <CampaignCard key={c.id} campaign={c} t={t} activeCardRef={activeCardRef} />
              ))}
            </div>
          )}

          {activeTab === 'pending' && isAdmin && (
            <div style={styles.list}>
              {pendingCampaigns.map(c => (
                <CampaignCard key={c.id} campaign={c} t={t} isAdmin={isAdmin} onApprove={approveCampaign} onReject={rejectCampaign} />
              ))}
            </div>
          )}

          {activeTab === 'myHistory' && (
            <div style={styles.list}>
              {myCampaigns.map(c => (
                <CampaignCard key={c.id} campaign={c} t={t} />
              ))}
            </div>
          )}

          {activeTab === 'create' && (
            <CampaignForm 
              t={t} 
              isBanned={isBanned} 
              hasActiveCampaign={hasActiveCampaign} 
              isTrusted={isTrusted} 
              onSubmitSuccess={handleFormSubmit} 
            />
          )}

        </div>
      </div>
    </div>
  );
}