import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [surahs, setSurahs] = useState([]);
  const [selectedSurah, setSelectedSurah] = useState(null);
  const [ayahs, setAyahs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetch('https://api.alquran.cloud/v1/surah')
      .then((res) => res.json())
      .then((data) => setSurahs(data.data))
      .catch((err) => console.error('خطا در دریافت لیست سوره‌ها:', err));
  }, []);

  const handleSelectSurah = (surahNumber) => {
    setLoading(true);
    fetch(`https://api.alquran.cloud/v1/surah/${surahNumber}/ar.alafasy`)
      .then((res) => res.json())
      .then((data) => {
        setSelectedSurah(data.data);
        setAyahs(data.data.ayahs);
        setLoading(false);
      })
      .catch((err) => {
        console.error('خطا در دریافت آیات:', err);
        setLoading(false);
      });
  };

  const filteredSurahs = surahs.filter((surah) =>
    surah.name.includes(searchQuery) ||
    surah.englishName.toLowerCase().includes(searchQuery.toLowerCase()) ||
    surah.number.toString() === searchQuery
  );

  return (
    <div className="app-container" dir="rtl">
      <header className="header">
        <h1>📖 قرآن آنلاین PWA</h1>
        {selectedSurah && (
          <button className="back-btn" onClick={() => setSelectedSurah(null)}>
            ← بازگشت به لیست سوره‌ها
          </button>
        )}
      </header>

      {!selectedSurah ? (
        <main className="main-content">
          <input
            type="text"
            placeholder="جستجوی سوره (نام یا شماره)..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="search-input"
          />
          <div className="surah-grid">
            {filteredSurahs.map((surah) => (
              <div
                key={surah.number}
                className="surah-card"
                onClick={() => handleSelectSurah(surah.number)}
              >
                <div className="surah-number">{surah.number}</div>
                <div className="surah-info">
                  <h3>{surah.name}</h3>
                  <p>{surah.englishName} • {surah.numberOfAyahs} آیه</p>
                </div>
              </div>
            ))}
          </div>
        </main>
      ) : (
        <main className="surah-detail">
          <div className="surah-header">
            <h2>{selectedSurah.name}</h2>
            <p className="meta-info">
              {selectedSurah.englishName} | {selectedSurah.revelationType === 'Meccan' ? 'مکی' : 'مدنی'} | {selectedSurah.numberOfAyahs} آیه
            </p>
          </div>

          {loading ? (
            <div className="loading">در حال دریافت آیات...</div>
          ) : (
            <div className="ayahs-list">
              {ayahs.map((ayah) => (
                <div key={ayah.number} className="ayah-card">
                  <div className="ayah-top">
                    <span className="ayah-badge">آیه {ayah.numberInSurah}</span>
                    {ayah.audio && <audio controls src={ayah.audio} preload="none" />}
                  </div>
                  <p className="arabic-text">{ayah.text}</p>
                </div>
              ))}
            </div>
          )}
        </main>
      )}
    </div>
  );
}

export default App;