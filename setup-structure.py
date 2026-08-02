import os

# تعریف ساختار کامل پوشه‌ها، فایل‌ها و محتوای آن‌ها
files = {
    # ۱. فایل ترجمه‌ها
    'src/locales/translations.js': """export const DEFAULT_APP_DONATION_URL = 'https://zarinp.al/your-app-donation';

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
      `السلام عليكم ورحمة الله وبركاته 🌸\\nأدعوك للمشاركة في حملة معراج القرآنية المباركة لنيل الأجر وثواب:\\n\\n✨ **العنوان:** ${title}\\n💡 **النية:** ${intention}\\n📌 **رمز الحملة:** ${id}\\n\\nللانضمام والمشاركة في معراج، انقر على الرابط التالي👇`
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
};""",

    # ۲. توابع کمکی
    'src/utils/campaignHelpers.js': """export function getOrCreateDeviceId() {
  let id = localStorage.getItem('merajDeviceId');
  if (!id) {
    id = 'DEV-' + Math.random().toString(36).substring(2, 11);
    localStorage.setItem('merajDeviceId', id);
  }
  return id;
}

export function processAndCleanupCampaigns(list, setBannedUsersCallback) {
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
    if (setBannedUsersCallback) {
      setBannedUsersCallback(updatedBanned);
    }
  }

  return cleanedList;
}""",

    # ۳. هوک مدیریت پویش‌ها
    'src/hooks/useCampaigns.js': """import { useState, useEffect } from 'react';
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
    const fullMessage = `${inviteBody}\\n🔗 ${shareUrl}`;

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
}""",

    # ۴. استایل‌ها
    'src/components/CampaignManager/CampaignManager.styles.js': """export const styles = {
  overlay: { position: 'fixed', top: 0, left: 0, right: 0, bottom: 0, background: 'rgba(0,0,0,0.6)', display: 'flex', justifyContent: 'center', alignItems: 'center', zIndex: 1400 },
  modal: { background: '#fff', borderRadius: '14px', width: '92%', maxWidth: '540px', maxHeight: '88vh', display: 'flex', flexDirection: 'column', fontFamily: 'Tahoma, sans-serif', boxSizing: 'border-box' },
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
  card: { background: '#f8fafc', border: '1px solid #e2e8f0', borderRadius: '8px', padding: '10px', fontSize: '12px', transition: 'all 0.3s ease', boxSizing: 'border-box' },
  activePlayingCard: { borderColor: '#10b981', boxShadow: '0 0 10px rgba(16, 185, 129, 0.2)' },
  badge: { background: '#10b981', color: '#fff', padding: '2px 6px', borderRadius: '4px', fontSize: '10px', fontWeight: 'bold' },
  desc: { color: '#64748b', fontSize: '11px', margin: '4px 0 8px 0' },
  shareBtn: { flex: 2, padding: '6px', background: '#0284c7', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '11px', fontWeight: 'bold' },
  campaignSupportBtn: { flex: 1, padding: '6px', background: '#10b981', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontSize: '11px', fontWeight: 'bold' },
  btn: { flex: 1, color: '#fff', border: 'none', padding: '6px', borderRadius: '4px', fontSize: '11px', cursor: 'pointer', fontWeight: 'bold' },
  form: { display: 'flex', flexDirection: 'column', gap: '8px', fontSize: '12px' },
  input: { padding: '8px', borderRadius: '6px', border: '1px solid #ccc', width: '100%', boxSizing: 'border-box' },
  textarea: { padding: '8px', borderRadius: '6px', border: '1px solid #ccc', fontFamily: 'sans-serif', width: '100%', boxSizing: 'border-box' },
  select: { padding: '8px', borderRadius: '6px', border: '1px solid #ccc', width: '100%', fontSize: '11px', boxSizing: 'border-box' },
  submitBtn: { padding: '10px', background: '#10b981', color: '#fff', border: 'none', borderRadius: '6px', cursor: 'pointer', fontWeight: 'bold', marginTop: '8px' },
  errorText: { color: '#dc2626', textAlign: 'center', fontSize: '12px', padding: '20px' },
  warningText: { color: '#d97706', textAlign: 'center', fontSize: '12px', padding: '20px' }
};""",

    # ۵. تب پویش‌های فعال
    'src/components/CampaignManager/components/ActiveCampaignsTab.jsx': """import React from 'react';

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
}""",

    # ۶. تب تأیید مدیر
    'src/components/CampaignManager/components/PendingAdminTab.jsx': """import React from 'react';

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
}""",

    # ۷. تب سابقه من
    'src/components/CampaignManager/components/CampaignHistoryTab.jsx': """import React from 'react';

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
}""",

    # ۸. تب ساخت پویش
    'src/components/CampaignManager/components/CreateCampaignTab.jsx': """import React, { useState } from 'react';

export default function CreateCampaignTab({ 
  isBanned, 
  hasActiveCampaign, 
  isTrusted, 
  deviceId, 
  t, 
  styles, 
  onCampaignCreated, 
  DEFAULT_APP_DONATION_URL 
}) {
  const [newTitle, setNewTitle] = useState('');
  const [newIntention, setNewIntention] = useState('');
  const [newDonationUrl, setNewDonationUrl] = useState('');
  const [assignmentType, setAssignmentType] = useState('pages');
  const [durationDays, setDurationDays] = useState(7);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (isBanned) {
      alert(t.statusBanned);
      return;
    }

    if (hasActiveCampaign) {
      alert(t.statusActiveLimit);
      return;
    }

    const total = assignmentType === 'pages' ? 604 : 6236;
    const deadlineDate = new Date(Date.now() + Number(durationDays) * 24 * 60 * 60 * 1000);
    const initialStatus = isTrusted ? 'active' : 'pending';

    const newCampaign = {
      id: `MRJ-${Math.floor(1000 + Math.random() * 9000)}`,
      creatorId: deviceId,
      title: newTitle,
      intention: newIntention,
      donationUrl: newDonationUrl.trim() || DEFAULT_APP_DONATION_URL,
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

    onCampaignCreated(newCampaign, isTrusted);
    setNewTitle('');
    setNewIntention('');
    setNewDonationUrl('');
  };

  if (isBanned) return <p style={styles.errorText}>{t.statusBanned}</p>;
  if (hasActiveCampaign) return <p style={styles.warningText}>{t.statusActiveLimit}</p>;

  return (
    <form onSubmit={handleSubmit} style={styles.form}>
      <label htmlFor="titleInput">{t.campaignTitle}:</label>
      <input id="titleInput" type="text" value={newTitle} onChange={e => setNewTitle(e.target.value)} required style={styles.input} />

      <label htmlFor="intentionInput">{t.intention}:</label>
      <textarea id="intentionInput" value={newIntention} onChange={e => setNewIntention(e.target.value)} required style={styles.textarea} />

      <label htmlFor="donationInput">{t.donationUrlLabel}:</label>
      <input id="donationInput" type="url" placeholder={t.donationUrlPlaceholder} value={newDonationUrl} onChange={e => setNewDonationUrl(e.target.value)} style={styles.input} />

      <div style={{ display: 'flex', gap: '8px' }}>
        <div style={{ flex: 1 }}>
          <label htmlFor="unitTypeSelect">{t.unitType}:</label>
          <select id="unitTypeSelect" value={assignmentType} onChange={e => setAssignmentType(e.target.value)} style={styles.select}>
            <option value="pages">{t.pages}</option>
            <option value="ayahs">{t.ayahs}</option>
          </select>
        </div>

        <div style={{ flex: 1 }}>
          <label htmlFor="durationSelect">{t.duration}:</label>
          <select id="durationSelect" value={durationDays} onChange={e => setDurationDays(e.target.value)} style={styles.select}>
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
}""",

    # ۹. کامپوننت اصلی CampaignManager
    'src/components/CampaignManager/CampaignManager.jsx': """import React, { useRef } from 'react';
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
}""",

    # ۱۰. فایل اصلاح‌شده App.jsx
    'src/App.jsx': """import React, { useState } from 'react';
import CampaignManager from './components/CampaignManager/CampaignManager';
import './App.css';

export default function App() {
  const [isCampaignOpen, setIsCampaignOpen] = useState(false);

  return (
    <div style={{ padding: '20px', textAlign: 'center', fontFamily: 'Tahoma, sans-serif' }}>
      <h1>🌐 برنامه آنلاین قرآن</h1>
      <button 
        onClick={() => setIsCampaignOpen(true)}
        style={{ 
          padding: '12px 20px', 
          fontSize: '14px', 
          background: '#10b981', 
          color: '#fff', 
          border: 'none', 
          borderRadius: '8px', 
          cursor: 'pointer',
          fontWeight: 'bold'
        }}
      >
        🌐 مدیریت پویش‌های قرآنی
      </button>

      {/* کامپوننت ماژولار مدیریت پویش */}
      <CampaignManager 
        isOpen={isCampaignOpen} 
        onClose={() => setIsCampaignOpen(false)} 
      />
    </div>
  );
}"""
}

print("🚀 در حال بازسازی ساختار پروژه و جایگزینی محتوا...")

for file_path, content in files.items():
    # ساخت اتوماتیک پوشه‌ها در صورت عدم وجود
    folder = os.path.dirname(file_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)
    
    # نوشتن فایل با انکودینگ UTF-8
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"✅ فایل ایجاد/به‌روزرسانی شد: {file_path}")

print("\n🎉 ساختار ماژولار با موفقیت اعمال و فایل App.jsx اصلاح شد!")