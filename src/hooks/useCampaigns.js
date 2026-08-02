import { useState, useEffect } from 'react';
import { TRANSLATIONS, DEFAULT_APP_DONATION_URL } from '../locales/translations';
import { getOrCreateDeviceId, processAndCleanupCampaigns } from '../utils/campaignHelpers';

export function useCampaigns() {
  const [lang, setLang] = useState(() => localStorage.getItem('merajLang') || 'fa');
  const t = TRANSLATIONS[lang] || TRANSLATIONS.fa;

  const [deviceId] = useState(() => getOrCreateDeviceId());
  const [isAdmin, setIsAdmin] = useState(() => localStorage.getItem('merajIsAdmin') === 'true');
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const [adminPasswordInput, setAdminPasswordInput] = useState('');

  const [trustedUsers, setTrustedUsers] = useState(() => {
    return JSON.parse(localStorage.getItem('merajTrustedUsers') || '[]');
  });

  const [bannedUsers, setBannedUsers] = useState(() => {
    return JSON.parse(localStorage.getItem('merajBannedUsers') || '[]');
  });

  const [campaigns, setCampaigns] = useState(() => {
    const saved = localStorage.getItem('merajCampaigns') || localStorage.getItem('quranCampaigns');
    const initialList = saved ? JSON.parse(saved) : [];
    return processAndCleanupCampaigns(initialList, setBannedUsers);
  });

  const [activeTab, setActiveTab] = useState('active');

  useEffect(() => {
    localStorage.setItem('merajCampaigns', JSON.stringify(campaigns));
  }, [campaigns]);

  useEffect(() => {
    localStorage.setItem('merajTrustedUsers', JSON.stringify(trustedUsers));
  }, [trustedUsers]);

  const handleLangChange = (newLang) => {
    setLang(newLang);
    localStorage.setItem('merajLang', newLang);
  };

  const handleAdminLogin = (e) => {
    e.preventDefault();
    if (adminPasswordInput === '123456') {
      setIsAdmin(true);
      localStorage.setItem('merajIsAdmin', 'true');
      setShowAdminLogin(false);
      setAdminPasswordInput('');
    } else {
      alert('❌ Invalid password');
    }
  };

  const handleAdminLogout = () => {
    setIsAdmin(false);
    localStorage.removeItem('merajIsAdmin');
  };

  const handleApproveCampaign = (campaign) => {
    setCampaigns(prev => prev.map(c => c.id === campaign.id ? { ...c, status: 'active' } : c));
    if (!trustedUsers.includes(campaign.creatorId)) {
      setTrustedUsers(prev => [...prev, campaign.creatorId]);
    }
  };

  const handleRejectCampaign = (campaignId) => {
    setCampaigns(prev => prev.map(c => c.id === campaignId ? { ...c, status: 'rejected' } : c));
  };

  const handleShareCampaign = (campaign) => {
    const inviteBody = t.getInviteText(campaign.title, campaign.intention, campaign.id);
    const shareUrl = window.location.href;
    const fullMessage = `${inviteBody}\n🔗 ${shareUrl}`;

    if (navigator.share) {
      navigator.share({
        title: campaign.title,
        text: fullMessage,
        url: shareUrl
      }).catch(() => {});
    } else {
      navigator.clipboard.writeText(fullMessage);
      alert(t.copySuccess);
    }
  };

  const handleOpenDonation = (targetUrl) => {
    const url = targetUrl || DEFAULT_APP_DONATION_URL;
    window.open(url, '_blank', 'noopener,noreferrer');
  };

  return {
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
  };
}
