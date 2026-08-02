import React, { useState } from 'react';

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
}
