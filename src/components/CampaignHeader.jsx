import React, { useState } from 'react';
import { campaignStyles as styles } from '../styles/campaignStyles';
import { DEFAULT_APP_DONATION_URL } from '../constants/translations';

export default function CampaignHeader({ t, lang, setLang, isAdmin, setIsAdmin, onClose }) {
  const [showAdminLogin, setShowAdminLogin] = useState(false);
  const [passwordInput, setPasswordInput] = useState('');

  const handleOpenDonation = (url) => {
    window.open(url || DEFAULT_APP_DONATION_URL, '_blank', 'noopener,noreferrer');
  };

  const handleAdminLogin = (e) => {
    e.preventDefault();
    if (passwordInput === '123456') {
      setIsAdmin(true);
      localStorage.setItem('merajIsAdmin', 'true');
      setShowAdminLogin(false);
      setPasswordInput('');
    } else {
      alert('❌ Password invalid');
    }
  };

  return (
    <>
      <div style={styles.header}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <h3 style={{ margin: 0, fontSize: '15px' }}>{t.title}</h3>
          <select value={lang} onChange={(e) => setLang(e.target.value)} style={styles.langSelect}>
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
            <button onClick={() => { setIsAdmin(false); localStorage.removeItem('merajIsAdmin'); }} style={{ ...styles.adminBtn, background: '#ef4444', color: '#fff' }}>
              {t.adminLogout}
            </button>
          )}
          <button onClick={onClose} style={styles.closeBtn}>✕</button>
        </div>
      </div>

      {showAdminLogin && !isAdmin && (
        <form onSubmit={handleAdminLogin} style={styles.adminForm}>
          <input type="password" placeholder="Pass: 123456" value={passwordInput} onChange={(e) => setPasswordInput(e.target.value)} style={styles.input} />
          <button type="submit" style={styles.submitBtn}>OK</button>
        </form>
      )}
    </>
  );
}