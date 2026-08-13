import React, { useState, useEffect } from 'react';

export default function CampaignManager({ isOpen, onClose }) {
  const [campaigns, setCampaigns] = useState(() => {
    const saved = localStorage.getItem('meraj_campaigns');
    return saved ? JSON.parse(saved) : [
      { id: 1, title: 'ختم سراسری قرآن کریم (دوره ۴۵)', target: 604, current: 412, unit: 'صفحه', icon: '📖' },
      { id: 2, title: 'پویش هدیه سوره یس به روح اموات', target: 1000, current: 680, unit: 'بار', icon: '✨' },
      { id: 3, title: 'پویش صلوات جهت تعجیل در فرج', target: 100000, current: 74200, unit: 'صلوات', icon: '📿' }
    ];
  });

  const [selectedCampaign, setSelectedCampaign] = useState(1);
  const [contribution, setContribution] = useState(1);
  const [successMsg, setSuccessMsg] = useState('');

  useEffect(() => {
    localStorage.setItem('meraj_campaigns', JSON.stringify(campaigns));
  }, [campaigns]);

  if (!isOpen) return null;

  const handleContribute = (e) => {
    e.preventDefault();
    const count = parseInt(contribution) || 1;
    setCampaigns(prev => prev.map(c => {
      if (c.id === selectedCampaign) {
        return { ...c, current: Math.min(c.target, c.current + count) };
      }
      return c;
    }));
    setSuccessMsg('✅ سهم شما با موفقیت ثبت شد. التماس دعا');
    setTimeout(() => setSuccessMsg(''), 3000);
  };

  const activeC = campaigns.find(c => c.id === selectedCampaign);

  return (
    <div style={{
      position: 'fixed',
      top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: 'rgba(15, 23, 42, 0.85)',
      backdropFilter: 'blur(4px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 9999,
      padding: '16px',
      direction: 'rtl'
    }}>
      <div style={{
        backgroundColor: '#1e293b',
        border: '1px solid #334155',
        borderRadius: '12px',
        width: '100%',
        maxWidth: '520px',
        color: '#f8fafc',
        boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.5)',
        overflow: 'hidden'
      }}>
        {/* هدر مودال */}
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '16px 20px',
          borderBottom: '1px solid #334155',
          backgroundColor: '#0f172a'
        }}>
          <h2 style={{ margin: 0, fontSize: '16px', color: '#38bdf8', display: 'flex', alignItems: 'center', gap: '8px' }}>
            <span>🌐</span> پویش‌های فعال معراج
          </h2>
          <button onClick={onClose} style={{
            background: 'none',
            border: 'none',
            color: '#94a3b8',
            fontSize: '20px',
            cursor: 'pointer'
          }}>✕</button>
        </div>

        {/* بدنه مودال */}
        <div style={{ padding: '20px' }}>
          {/* انتخاب پویش */}
          <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
            {campaigns.map(c => (
              <button
                key={c.id}
                onClick={() => setSelectedCampaign(c.id)}
                style={{
                  flex: 1,
                  padding: '8px',
                  borderRadius: '6px',
                  border: selectedCampaign === c.id ? '1px solid #38bdf8' : '1px solid #334155',
                  backgroundColor: selectedCampaign === c.id ? '#0284c7' : '#0f172a',
                  color: '#ffffff',
                  fontSize: '11px',
                  cursor: 'pointer',
                  fontWeight: selectedCampaign === c.id ? 'bold' : 'normal'
                }}
              >
                {c.icon} {c.title.split(' ')[0]} {c.title.split(' ')[1]}
              </button>
            ))}
          </div>

          {/* اطلاعات و درصد پیشرفت */}
          {activeC && (
            <div style={{ backgroundColor: '#0f172a', padding: '16px', borderRadius: '8px', marginBottom: '16px' }}>
              <h3 style={{ margin: '0 0 8px 0', fontSize: '14px', color: '#f1f5f9' }}>{activeC.title}</h3>
              <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '12px', color: '#94a3b8', marginBottom: '6px' }}>
                <span>پیشرفت پویش: {activeC.current.toLocaleString('fa-IR')} از {activeC.target.toLocaleString('fa-IR')} {activeC.unit}</span>
                <span>{Math.round((activeC.current / activeC.target) * 100)}٪</span>
              </div>
              <div style={{ width: '100%', height: '8px', backgroundColor: '#334155', borderRadius: '4px', overflow: 'hidden' }}>
                <div style={{
                  width: `${(activeC.current / activeC.target) * 100}%`,
                  height: '100%',
                  backgroundColor: '#10b981',
                  transition: 'width 0.3s ease'
                }} />
              </div>
            </div>
          )}

          {/* فرم ثبت مشارکت */}
          <form onSubmit={handleContribute} style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <label style={{ fontSize: '12px', color: '#cbd5e1' }}>تعداد سهم شما جهت مشارکت ({activeC?.unit}):</label>
            <div style={{ display: 'flex', gap: '8px' }}>
              <input
                type="number"
                min="1"
                value={contribution}
                onChange={(e) => setContribution(e.target.value)}
                style={{
                  flex: 1,
                  backgroundColor: '#0f172a',
                  border: '1px solid #334155',
                  borderRadius: '6px',
                  padding: '8px 12px',
                  color: '#ffffff',
                  fontSize: '14px'
                }}
              />
              <button type="submit" style={{
                backgroundColor: '#10b981',
                color: '#ffffff',
                border: 'none',
                borderRadius: '6px',
                padding: '8px 20px',
                fontWeight: 'bold',
                fontSize: '13px',
                cursor: 'pointer'
              }}>
                ثبت سهم
              </button>
            </div>
          </form>

          {successMsg && (
            <div style={{ marginTop: '12px', padding: '8px 12px', backgroundColor: 'rgba(16, 185, 129, 0.2)', border: '1px solid #10b981', borderRadius: '6px', color: '#34d399', fontSize: '12px', textAlign: 'center' }}>
              {successMsg}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
