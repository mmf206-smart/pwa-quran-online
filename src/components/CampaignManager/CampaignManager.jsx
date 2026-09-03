import React, { useState, useEffect } from 'react';

export default function CampaignManager({ isOpen, onClose }) {
  const [campaigns, setCampaigns] = useState(() => {
    const saved = localStorage.getItem('meraj_campaigns');
    return saved ? JSON.parse(saved) : [
      { id: 1, title: 'ختم سراسری قرآن کریم', target: 604, current: 420, unit: 'صفحه', icon: '📖' },
      { id: 2, title: 'پویش هدیه سوره یس', target: 1000, current: 730, unit: 'بار', icon: '✨' },
      { id: 3, title: 'پویش ذکر صلوات', target: 100000, current: 81500, unit: 'صلوات', icon: '📿' }
    ];
  });

  const [selectedId, setSelectedId] = useState(1);
  const [amount, setAmount] = useState(1);
  const [msg, setMsg] = useState('');

  useEffect(() => {
    localStorage.setItem('meraj_campaigns', JSON.stringify(campaigns));
  }, [campaigns]);

  if (!isOpen) return null;

  const handleSubmit = (e) => {
    e.preventDefault();
    const val = parseInt(amount) || 1;
    setCampaigns(prev => prev.map(c => c.id === selectedId ? { ...c, current: Math.min(c.target, c.current + val) } : c));
    setMsg('✅ سهم شما با موفقیت ثبت شد.');
    setTimeout(() => setMsg(''), 3000);
  };

  const activeC = campaigns.find(c => c.id === selectedId);

  return (
    <div style={{ position: 'fixed', inset: 0, backgroundColor: 'rgba(15, 23, 42, 0.85)', backdropFilter: 'blur(4px)', display: 'flex', alignItems: 'center', justifyContent: 'center', zIndex: 9999, padding: '16px', direction: 'rtl' }}>
      <div style={{ backgroundColor: '#1e293b', border: '1px solid #334155', borderRadius: '12px', width: '100%', maxWidth: '500px', color: '#f8fafc', padding: '20px', boxShadow: '0 20px 25px -5px rgba(0,0,0,0.5)' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px', borderBottom: '1px solid #334155', pb: '12px' }}>
          <h3 style={{ margin: 0, color: '#38bdf8', fontSize: '16px' }}>🌐 پویش‌های قرآنی معراج</h3>
          <button onClick={onClose} style={{ background: 'none', border: 'none', color: '#94a3b8', fontSize: '20px', cursor: 'pointer' }}>✕</button>
        </div>

        <div style={{ display: 'flex', gap: '8px', marginBottom: '16px' }}>
          {campaigns.map(c => (
            <button key={c.id} onClick={() => setSelectedId(c.id)} style={{ flex: 1, padding: '8px', borderRadius: '6px', border: selectedId === c.id ? '1px solid #38bdf8' : '1px solid #334155', backgroundColor: selectedId === c.id ? '#0284c7' : '#0f172a', color: '#fff', fontSize: '11px', cursor: 'pointer' }}>
              {c.icon} {c.title.split(' ')[0]} {c.title.split(' ')[1]}
            </button>
          ))}
        </div>

        {activeC && (
          <div style={{ backgroundColor: '#0f172a', padding: '12px', borderRadius: '8px', marginBottom: '16px' }}>
            <div style={{ fontSize: '13px', fontWeight: 'bold', marginBottom: '6px' }}>{activeC.title}</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '11px', color: '#94a3b8', marginBottom: '6px' }}>
              <span>پیشرفت: {activeC.current} از {activeC.target} {activeC.unit}</span>
              <span>{Math.round((activeC.current / activeC.target) * 100)}٪</span>
            </div>
            <div style={{ height: '8px', backgroundColor: '#334155', borderRadius: '4px', overflow: 'hidden' }}>
              <div style={{ width: `${(activeC.current / activeC.target) * 100}%`, height: '100%', backgroundColor: '#10b981', transition: 'width 0.3s' }} />
            </div>
          </div>
        )}

        <form onSubmit={handleSubmit} style={{ display: 'flex', gap: '8px' }}>
          <input type="number" min="1" value={amount} onChange={e => setAmount(e.target.value)} style={{ flex: 1, backgroundColor: '#0f172a', border: '1px solid #334155', borderRadius: '6px', padding: '8px', color: '#fff', fontSize: '13px' }} />
          <button type="submit" style={{ backgroundColor: '#10b981', color: '#fff', border: 'none', borderRadius: '6px', padding: '8px 16px', fontWeight: 'bold', cursor: 'pointer', fontSize: '12px' }}>ثبت مشارکت</button>
        </form>

        {msg && <div style={{ marginTop: '10px', color: '#34d399', fontSize: '12px', textAlign: 'center' }}>{msg}</div>}
      </div>
    </div>
  );
}
