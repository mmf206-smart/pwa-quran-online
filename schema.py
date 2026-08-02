import os
from pathlib import Path

# تعریف فایل‌ها و محتوای آن‌ها
files_data = {
    # 1. Constants
    "src/constants/translations.js": """export const DEFAULT_APP_DONATION_URL = 'https://zarinp.al/your-app-donation';

export const TRANSLATIONS = {
  fa: {
    dir: 'rtl',
    title: "🌐 پویش‌های قرآنی معراج",
    activeCampaigns: "پویش‌های فعال",
    pendingAdmin: "⏳ نیازمند تأیید",
    myHistory: "📋 سابقه من",
    createCampaign: "➕ ساخت پویش معراج",
    statusBanned: "⛔ حساب شما به دلیل عدم تکمیل پویش قبلی مسدود شده است.",
    statusActiveLimit: "⏳ شما یک پویش فعال در جریان یا در انتظار بررسی دارید.",
    statusTrusted: "🌟 شما کاربر معتبر معراج هستید (تأیید خودکار پویش).",
    statusFirstTime: "🌱 پویش اول شما نیاز به تأیید اولیه مدیر دارد.",
    campaignTitle: "عنوان پویش معراج",
    intention: "منظور و نیت پویش",
    unitType: "مبنای تقسیم",
    duration: "مهلت پویش (روز)",
    pages: "صفحه‌ای (۶۰۴ صفحه)",
    ayahs: "آیه‌ای (۶۲۳۶ آیه)",
    submitBtnFirst: "🚀 ارسال جهت بررسی اولیه مدیر",
    submitBtnTrusted: "⚡ ثبت و انتشار خودکار پویش",
    shareBtn: "📲 دعوت دوستان به معراج",
    copySuccess: "✅ متن و لینک دعوت معراج کپی شد!",
    approvedText: "✔️ تأیید و معتبرسازی کاربر",
    rejectText: "❌ رد پویش",
    adminLogin: "🔐 ورود مدیر معراج",
    adminLogout: "خروج مدیر",
    progress: "پیشرفت",
    appSupportBtn: "☕ حمایت از معراج",
    campaignSupportBtn: "💳 حمایت مالی",
    donationUrlLabel: "لینک درگاه پرداخت/حمایت پویش (اختیاری)",
    donationUrlPlaceholder: "https://zarinp.al/...",
    getInviteText: (title, intention, id) => 
      `سلام 👋\\nشما را به پویش قرآنی معراج دعوت می‌کنم تا در این ثواب جاریه شریک باشید:\\n\\n✨ **عنوان:** ${title}\\n💡 **نیت:** ${intention}\\n📌 **کد پویش:** ${id}\\n\\nبرای پیوستن به معراج و شرکت در ختم، روی لینک زیر کلیک کنید👇`
  },
  en: {
    dir: 'ltr',
    title: "🌐 Meraj Quran Campaigns",
    activeCampaigns: "Active Campaigns",
    pendingAdmin: "⏳ Pending Approval",
    myHistory: "📋 My History",
    createCampaign: "➕ Create Meraj Campaign",
    statusBanned: "⛔ Account banned due to an uncompleted previous campaign.",
    statusActiveLimit: "⏳ You already have an active or pending campaign.",
    statusTrusted: "🌟 Trusted Meraj Creator (Auto-approved campaign).",
    statusFirstTime: "🌱 Your first campaign requires admin approval.",
    campaignTitle: "Meraj Campaign Title",
    intention: "Intention & Purpose",
    unitType: "Division Unit",
    duration: "Duration (Days)",
    pages: "Pages (604 Pages)",
    ayahs: "Verses (6236 Ayahs)",
    submitBtnFirst: "🚀 Submit for Admin Review",
    submitBtnTrusted: "⚡ Publish Automatically",
    shareBtn: "📲 Invite Friends to Meraj",
    copySuccess: "✅ Meraj invitation text & link copied!",
    approvedText: "✔️ Approve & Mark User Trusted",
    rejectText: "❌ Reject",
    adminLogin: "🔐 Meraj Admin Login",
    adminLogout: "Admin Logout",
    progress: "Progress",
    appSupportBtn: "☕ Support Meraj",
    campaignSupportBtn: "💳 Donate",
    donationUrlLabel: "Donation Gateway Link (Optional)",
    donationUrlPlaceholder: "https://...",
    getInviteText: (title, intention, id) => 
      `Peace be upon you! 🌟\\nI invite you to join this Meraj Quran Campaign and share in the blessings:\\n\\n✨ **Title:** ${title}\\n💡 **Purpose:** ${intention}\\n📌 **Campaign Code:** ${id}\\n\\nClick the link below to join Meraj and participate👇`
  },
  ar: {
    dir: 'rtl',
    title: "🌐 معراج - حملات القرآن العالمية",
    activeCampaigns: "الحملات النشطة",
    pendingAdmin: "⏳ قيد المراجعة",
    myHistory: "📋 سجلي",
    createCampaign: "➕ إنشاء حملة معراج",
    statusBanned: "⛔ حسابك محظور بسبب عدم إكمال الحملة السابقة.",
    statusActiveLimit: "⏳ لديك حملة نشطة أو قيد المراجعة حالياً.",
    statusTrusted: "🌟 منشئ معراج موثوق (موافقة تلقائية على الحملة).",
    statusFirstTime: "🌱 حملتك الأولى تتطلب موافقة المدير.",
    campaignTitle: "عنوان حملة معراج",
    intention: "النية والهدف",
    unitType: "وحدة التقسيم",
    duration: "المدة (أيام)",
    pages: "صفحات (٦٠٤ صفحة)",
    ayahs: "آيات (٦٢٣٦ آية)",
    submitBtnFirst: "🚀 إرسال للمراجعة",
    submitBtnTrusted: "⚡ نشر تلقائي",
    shareBtn: "📲 دعوة الأصدقاء لمعراج",
    copySuccess: "✅ تم نسخ نص ودعوة معراج!",
    approvedText: "✔️ موافقة وتوثيق المستخدم",
    rejectText: "❌ رفض",
    adminLogin: "🔐 دخول مدير معراج",
    adminLogout: "خروج المدير",
    progress: "التقدم",
    appSupportBtn: "☕ دعم معراج",
    campaignSupportBtn: "💳 دعم مالياً",
    donationUrlLabel: "رابط بوابة الدفع/التبرع (اختياري)",
    donationUrlPlaceholder: "https://...",
    getInviteText: (title, intention, id) => 
      `السلام عليكم ورحمة الله وبركاته 🌸\\nأدعوك للمشاركة في حملة معراج القرآنية المباركة لنيل الأجر والثواب:\\n\\n✨ **العنوان:** ${title}\\n💡 **النية:** ${intention}\\n📌 **رمز الحملة:** ${id}\\n\\nللانضمام والمشاركة في معراج، انقر على الرابط التالي👇`
  },
  id: {
    dir: 'ltr',
    title: "🌐 Meraj - Kampanye Quran Global",
    activeCampaigns: "Kampanye Aktif",
    pendingAdmin: "⏳ Menunggu Persetujuan",
    myHistory: "📋 Riwayat Saya",
    createCampaign: "➕ Buat Kampanye Meraj",
    statusBanned: "⛔ Akun diblokir karena kampanye sebelumnya tidak selesai.",
    statusActiveLimit: "⏳ Anda sudah memiliki kampanye aktif atau dalam peninjauan.",
    statusTrusted: "🌟 Pembuat Terpercaya Meraj (Otomatis Disetujui).",
    statusFirstTime: "🌱 Kampanye pertama Anda membutuhkan persetujuan admin.",
    campaignTitle: "Judul Kampanye Meraj",
    intention: "Niat & Tujuan",
    unitType: "Unit Pembagian",
    duration: "Durasi (Hari)",
    pages: "Halaman (604 Halaman)",
    ayahs: "Ayat (6236 Ayat)",
    submitBtnFirst: "🚀 Kirim untuk Peninjauan",
    submitBtnTrusted: "⚡ Publikasikan Otomatis",
    shareBtn: "📲 Undang Teman ke Meraj",
    copySuccess: "✅ Teks & tautan undangan Meraj berhasil disalin!",
    approvedText: "✔️ Setujui & Verifikasi Pengguna",
    rejectText: "❌ Tolak",
    adminLogin: "🔐 Login Admin Meraj",
    adminLogout: "Keluar Admin",
    progress: "Kemajuan",
    appSupportBtn: "☕ Dukung Meraj",
    campaignSupportBtn: "💳 Donasi",
    donationUrlLabel: "Tautan Gerbang Pembayaran/Donasi (Opsional)",
    donationUrlPlaceholder: "https://...",
    getInviteText: (title, intention, id) => 
      `Assalamu'alaikum Warahmatullahi Wabarakatuh 🌸\\nSaya mengundang Anda untuk bergabung dalam Kampanye Quran Meraj ini dan meraih keberkahan bersama:\\n\\n✨ **Judul:** ${title}\\n💡 **Niat:** ${intention}\\n📌 **Kode Kampanye:** ${id}\\n\\nKlik tautan di bawah ini untuk bergabung di Meraj👇`
  }
};
""",

    # 2. Styles
    "src/styles/campaignStyles.js": """export const campaignStyles = {
  overlay: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.6)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1400 },
  modal: { background: '#fff', borderRadius: '14px', width: '92%', maxWidth: '540px', maxHeight: '88vh', display: 'flex', flexDirection: 'column', fontFamily: 'Tahoma, sans-serif' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '12px 16px', borderBottom: '1px solid #eee' },
  closeBtn: { border: 'none', background: 'none', fontSize: '18px', cursor: 'pointer' },
  adminBtn: { background: '#f1f5f9', border: '1px solid #cbd5e1', padding: '4px 8px', borderRadius: '6px', fontSize: '11px', cursor: 'pointer' },
  appSupportHeaderBtn: { background: '#fef3c7', border: '1px solid #f59e0b', color: '#b45309', padding: '4px 8px', borderRadius: '6px', fontSize: '11px', fontWeight: 'bold', cursor: 'pointer' },
  langSelect: { padding: '3px 6px', borderRadius: '6px', border: '1px solid #cbd5e1', fontSize: '11px', background: '#f8fafc', cursor: 'pointer' },
  adminForm: { padding: '8px 15px', background: '#f8fafc', display: 'flex', gap: '8px' },
  statusBar: { padding: '8px 12px', fontSize: '11px', textAlign: 'center', fontWeight: 'bold', background: '#f8fafc', borderBottom: '1px solid #eee' },
  tabContainer: { display: 'flex', borderBottom: '1px solid #eee', background: '#f8fafc', overflowX: 'auto' },
  tab: { flex: 1, padding: '10px 4px', border: 'none', background: 'none', cursor: 'pointer', fontSize: '11px', fontWeight: 'bold', whiteSpace: 'nowrap' },
  body: { padding: '15px', overflowY: 'auto' },
  list: { display: 'flex', flexDirection: 'column', gap: '10px' },
  card: { background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '10px', fontSize: '12px', transition: 'all 0.3s ease' },
  activePlayingCard: { borderColor: '#10b981', boxShadow: '0 0 10px rgba(16, 185, 129, 0.2)' },
  badge: { background: '#10b981', color: '#fff', padding: '2px 6px', borderRadius: '4px', fontSize: '10px', fontWeight: 'bold' },
  desc: { color: '#64748b', fontSize: '11px', margin: '4px 0 8px 0' },
  shareBtn: { flex: 2, padding: '6px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '11px', fontWeight: 'bold' },
  campaignSupportBtn: { flex: 1, padding: '6px', background: '#10b981', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '11px', fontWeight: 'bold' },
  btn: { flex: 1, color: '#fff', border: 'none', padding: '6px', borderRadius: '4px', fontSize: '11px', cursor: 'pointer', fontWeight: 'bold' },
  form: { display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '12px' },
  input: { padding: '8px', borderRadius: '6px', border: '1px solid #ccc', width: '100%' },
  textarea: { padding: '8px', borderRadius: '6px', border: '1px solid #ccc', fontFamily: 'sans-serif', width: '100%' },
  select: { padding: '8px', borderRadius: '6px', border: '1px solid #ccc', width: '100%', fontSize: '11px' },
  submitBtn: { padding: '10px', background: '#10b981', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', marginTop: '8px' },
  errorText: { color: '#dc2626', textAlign: 'center', fontSize: '12px', padding: '20px' },
  warningText: { color: '#d97706', textAlign: 'center', fontSize: '12px', padding: '20px' }
};
""",

    # 3. Hooks
    "src/hooks/useAutoScroll.js": """import { useEffect } from 'react';

/**
 * فرمول اختصاصی: S_target = Y_card - (H_view - H_card) / 2
 */
export function useAutoScroll(containerRef, activeCardRef, isPlaying) {
  useEffect(() => {
    if (!isPlaying || !containerRef.current || !activeCardRef.current) return;

    const container = containerRef.current;
    const card = activeCardRef.current;

    const H_view = container.clientHeight;
    const H_card = card.offsetHeight;
    const Y_card = card.offsetTop;

    const S_target = Y_card - (H_view - H_card) / 2;

    container.scrollTo({
      top: Math.max(0, S_target),
      behavior: 'smooth'
    });
  }, [isPlaying, containerRef, activeCardRef]);
}
""",

    "src/hooks/useCampaigns.js": """import { useState, useEffect, useMemo } from 'react';
import { DEFAULT_APP_DONATION_URL } from '../constants/translations';

export function useCampaigns() {
  const deviceId = useMemo(() => {
    let id = localStorage.getItem('merajDeviceId');
    if (!id) {
      id = 'DEV-' + Math.random().toString(36).substr(2, 9);
      localStorage.setItem('merajDeviceId', id);
    }
    return id;
  }, []);

  const [isAdmin, setIsAdmin] = useState(() => localStorage.getItem('merajIsAdmin') === 'true');
  const [trustedUsers, setTrustedUsers] = useState(() => JSON.parse(localStorage.getItem('merajTrustedUsers') || '[]'));
  const [bannedUsers, setBannedUsers] = useState(() => JSON.parse(localStorage.getItem('merajBannedUsers') || '[]'));

  const [campaigns, setCampaigns] = useState(() => {
    const saved = localStorage.getItem('merajCampaigns') || localStorage.getItem('quranCampaigns');
    const initialList = saved ? JSON.parse(saved) : [];
    return processAndCleanupCampaigns(initialList);
  });

  function processAndCleanupCampaigns(list) {
    const now = new Date();
    let updatedBanned = JSON.parse(localStorage.getItem('merajBannedUsers') || '[]');
    let hasBannedChanged = false;

    const cleanedList = list.map(c => {
      let updatedC = { ...c };
      if (updatedC.assignedUnits >= updatedC.totalUnits && updatedC.status === 'active') {
        updatedC.status = 'completed';
      }
      if (updatedC.status === 'active' && new Date(updatedC.deadline) < now) {
        updatedC.status = 'expired';
        if (updatedC.creatorId && updatedC.creatorId !== 'SYSTEM' && !updatedBanned.includes(updatedC.creatorId)) {
          updatedBanned.push(updatedC.creatorId);
          hasBannedChanged = true;
        }
      }
      return updatedC;
    });

    if (hasBannedChanged) {
      localStorage.setItem('merajBannedUsers', JSON.stringify(updatedBanned));
      setBannedUsers(updatedBanned);
    }
    return cleanedList;
  }

  useEffect(() => {
    localStorage.setItem('merajCampaigns', JSON.stringify(campaigns));
  }, [campaigns]);

  useEffect(() => {
    localStorage.setItem('merajTrustedUsers', JSON.stringify(trustedUsers));
  }, [trustedUsers]);

  const isBanned = bannedUsers.includes(deviceId);
  const isTrusted = trustedUsers.includes(deviceId);
  const hasActiveCampaign = campaigns.some(c => c.creatorId === deviceId && (c.status === 'active' || c.status === 'pending'));

  const createCampaign = ({ title, intention, donationUrl, assignmentType, durationDays }) => {
    const total = assignmentType === 'pages' ? 604 : 6236;
    const deadlineDate = new Date(Date.now() + Number(durationDays) * 24 * 60 * 60 * 1000);
    const initialStatus = isTrusted ? 'active' : 'pending';

    const newCampaign = {
      id: `MRJ-${Math.floor(1000 + Math.random() * 9000)}`,
      creatorId: deviceId,
      title,
      intention,
      donationUrl: donationUrl.trim() || DEFAULT_APP_DONATION_URL,
      assignmentType,
      totalUnits: total,
      assignedUnits: 0,
      unitsPerPerson: 5,
      status: initialStatus,
      isPlaying: false,
      createdAt: new Date().toISOString(),
      deadline: deadlineDate.toISOString(),
      takenShares: []
    };

    setCampaigns(prev => [newCampaign, ...prev]);
    return initialStatus;
  };

  const approveCampaign = (campaign) => {
    setCampaigns(prev => prev.map(c => c.id === campaign.id ? { ...c, status: 'active' } : c));
    if (!trustedUsers.includes(campaign.creatorId)) {
      setTrustedUsers(prev => [...prev, campaign.creatorId]);
    }
  };

  const rejectCampaign = (campaignId) => {
    setCampaigns(prev => prev.map(c => c.id === campaignId ? { ...c, status: 'rejected' } : c));
  };

  return {
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
  };
}
""",

    # 4. Components
    "src/components/CampaignHeader.jsx": """import React, { useState } from 'react';
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
""",

    "src/components/CampaignCard.jsx": """import React from 'react';
import { campaignStyles as styles } from '../styles/campaignStyles';
import { DEFAULT_APP_DONATION_URL } from '../constants/translations';

export default function CampaignCard({ campaign, t, activeCardRef, isAdmin, onApprove, onReject }) {
  const percent = Math.round((campaign.assignedUnits / campaign.totalUnits) * 100);

  const handleShare = () => {
    const inviteBody = t.getInviteText(campaign.title, campaign.intention, campaign.id);
    const shareUrl = window.location.href;
    const fullMessage = `${inviteBody}\\n🔗 ${shareUrl}`;

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
""",

    "src/components/CampaignForm.jsx": """import React, { useState } from 'react';
import { campaignStyles as styles } from '../styles/campaignStyles';

export default function CampaignForm({ t, isBanned, hasActiveCampaign, isTrusted, onSubmitSuccess }) {
  const [title, setTitle] = useState('');
  const [intention, setIntention] = useState('');
  const [donationUrl, setDonationUrl] = useState('');
  const [assignmentType, setAssignmentType] = useState('pages');
  const [durationDays, setDurationDays] = useState(7);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmitSuccess({ title, intention, donationUrl, assignmentType, durationDays });
    setTitle('');
    setIntention('');
    setDonationUrl('');
  };

  if (isBanned) return <p style={styles.errorText}>{t.statusBanned}</p>;
  if (hasActiveCampaign) return <p style={styles.warningText}>{t.statusActiveLimit}</p>;

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <label>{t.campaignTitle}:</label>
      <input type="text" value={title} onChange={e => setTitle(e.target.value)} required style={styles.input} />

      <label>{t.intention}:</label>
      <textarea value={intention} onChange={e => setIntention(e.target.value)} required style={styles.textarea} />

      <label>{t.donationUrlLabel}:</label>
      <input type="url" placeholder={t.donationUrlPlaceholder} value={donationUrl} onChange={e => setDonationUrl(e.target.value)} style={styles.input} />

      <div style={{ display: 'flex', gap: '8px' }}>
        <div style={{ flex: 1 }}>
          <label>{t.unitType}:</label>
          <select value={assignmentType} onChange={e => setAssignmentType(e.target.value)} style={styles.select}>
            <option value="pages">{t.pages}</option>
            <option value="ayahs">{t.ayahs}</option>
          </select>
        </div>

        <div style={{ flex: 1 }}>
          <label>{t.duration}:</label>
          <select value={durationDays} onChange={e => setDurationDays(e.target.value)} style={styles.select}>
            <option value={3}>3</option>
            <option value={7}>7</option>
            <option value={14}>14</option>
          </select>
        </div>
      </div>

      <button type="submit" style={styles.submitBtn}>
        {isTrusted ? t.submitBtnTrusted : t.submitBtnFirst}
      </button>
    </form>
  );
}
""",

    # 5. Root Component
    "src/CampaignManager.jsx": """import React, { useState, useRef } from 'react';
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
"""
}

def create_project_structure():
    print("🚀 در حال ساخت ساختار فایل‌های پروژه معراج...\n")
    for filepath, content in files_data.items():
        path = Path(filepath)
        # ساخت فولدرهای والد در صورت عدم وجود
        path.parent.mkdir(parents=True, exist_ok=True)
        # نوشتن محتوا در فایل با انکودینگ utf-8
        path.write_text(content.strip(), encoding='utf-8')
        print(f"✅ فایل با موفقیت ساخته شد: {filepath}")
    
    print("\n🎉 ساختار ماژولار معراج با موفقیت کامل ایجاد گردید!")

if __name__ == "__main__":
    create_project_structure()