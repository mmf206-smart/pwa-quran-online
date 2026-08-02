import React, { useState } from 'react';
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