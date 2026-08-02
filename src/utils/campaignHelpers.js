export function getOrCreateDeviceId() {
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
}
