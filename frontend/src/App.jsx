import React, { useState, useEffect, Suspense } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Activity, 
  Search, 
  X, 
  ShieldAlert, 
  Home, 
  Globe, 
  AlertCircle,
  Heart,
  MessageCircle,
  Send,
  Languages
} from 'lucide-react';
import axios from 'axios';
import Antigravity from './Antigravity';
import './App.css';

// Localization Object
const UI_STRINGS = {
  en: {
    title: "HealthCare AI",
    assistant: "AI Diagnostic Assistant",
    placeholder: "Enter symptoms (e.g. headache, fever)",
    precautions: "PRECAUTIONS",
    remedies: "HOME REMEDIES",
    disclaimer_title: "MEDICAL DISCLAIMER",
    disclaimer_p1: "This AI assistant provides general information based on symptoms and is NOT a substitute for professional medical advice, diagnosis, or treatment.",
    disclaimer_p2: "Always consult a qualified doctor. Do not self-medicate or delay seeking professional help based on these results.",
    confidence: "CONFIDENCE LEVEL: HIGH",
    diagnosing: "Analyzing...",
    learn_more: "VIEW FULL REPORT →"
  },
  hi: {
    title: "स्वास्थ्य देखभाल AI",
    assistant: "AI नैदानिक सहायक",
    placeholder: "लक्षण दर्ज करें (जैसे सिरदर्द, बुखार)",
    precautions: "सावधानियां",
    remedies: "घरेलू उपचार",
    disclaimer_title: "चिकित्सा अस्वीकरण",
    disclaimer_p1: "यह AI सहायक लक्षणों के आधार पर सामान्य जानकारी प्रदान करता है और पेशेवर चिकित्सा सलाह, निदान या उपचार का विकल्प नहीं है।",
    disclaimer_p2: "हमेशा एक योग्य डॉक्टर से परामर्श करें। इन परिणामों के आधार पर स्व-दवा न करें या पेशेवर मदद लेने में देरी न करें।",
    diagnosing: "विश्लेषण कर रहा है...",
    learn_more: "पूरी रिपोर्ट देखें →"
  },
  te: {
    title: "హెల్త్ కేర్ AI",
    assistant: "AI డయాగ్నోస్టిక్ అసిస్టెంట్",
    placeholder: "లక్షణాలను నమోదు చేయండి (ఉదా. తలనొప్పి, జ్వరం)",
    precautions: "జాగ్రత్తలు",
    remedies: "ఇంటి నివారణలు",
    disclaimer_title: "వైద్య నిరాకరణ",
    disclaimer_p1: "ఈ AI అసిస్టెంట్ లక్షణాల ఆధారంగా సాధారణ సమాచారాన్ని అందిస్తుంది మరియు వృత్తిపరమైన వైద్య సలహా, రోగ నిర్ధారణ లేదా చికిత్సకు ప్రత్యామ్నాయం కాదు.",
    disclaimer_p2: "ఎల్లప్పుడూ అర్హత కలిగిన వైద్యుడిని సంప్రదించండి. ఈ ఫలితాల ఆధారంగా స్వంతంగా మందులు వాడకండి.",
    diagnosing: "విశ్లేషిస్తోంది...",
    learn_more: "పూర్తి నివేదికను చూడండి →"
  },
  es: {
    title: "Cuidado de la Salud AI",
    assistant: "Asistente de Diagnóstico AI",
    placeholder: "Ingrese síntomas (ej. dolor de cabeza, fiebre)",
    precautions: "PRECAUCIONES",
    remedies: "REMEDIOS CASEROS",
    disclaimer_title: "DESCARGO DE RESPONSABILIDAD MÉDICA",
    disclaimer_p1: "Este asistente de IA proporciona información general basada en los síntomas y NO sustituye el asesoramiento, diagnóstico o tratamiento médico profesional.",
    disclaimer_p2: "Consulte siempre a un médico calificado. No se automedique ni retrase la búsqueda de ayuda profesional basándose en estos resultados.",
    diagnosing: "Analizando...",
    learn_more: "VER INFORME COMPLETO →"
  }
};

const LANGUAGES = [
  { code: 'en', name: 'English' },
  { code: 'hi', name: 'हिन्दी' },
  { code: 'te', name: 'తెలుగు' },
  { code: 'es', name: 'Español' }
];

const HEALTH_TIPS = [
  { id: 1, name: 'Water', icon: '💧', text: 'Drink 8 glasses of water daily.' },
  { id: 2, name: 'Sleep', icon: '😴', text: 'Get at least 7-8 hours of sleep.' },
  { id: 3, name: 'Exercise', icon: '🏃', text: 'Walk for 30 mins every day.' },
  { id: 4, name: 'Diet', icon: '🥗', text: 'Eat more leafy greens.' },
  { id: 5, name: 'Sugar', icon: '🍭', text: 'Reduce refined sugar intake.' },
  { id: 6, name: 'Mental', icon: '🧘', text: 'Practice 5 mins of meditation.' },
];

function App() {
  const [loading, setLoading] = useState(true);
  const [lang, setLang] = useState('en');
  const [symptoms, setSymptoms] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [result, setResult] = useState(null);
  const [isDiagnosing, setIsDiagnosing] = useState(false);
  const [showStory, setShowStory] = useState(null);
  const [error, setError] = useState(null);

  const t = UI_STRINGS[lang] || UI_STRINGS.en;

  useEffect(() => {
    const initApp = async () => {
      try {
        const response = await axios.get(`/api/symptoms`);
        if (response.data && response.data.symptoms) {
          setSymptoms(response.data.symptoms);
        }
        setTimeout(() => setLoading(false), 1000);
      } catch (err) {
        setError("Connection error. Please check if the backend is running.");
        setLoading(false);
      }
    };
    initApp();
  }, []);

  useEffect(() => {
    if (searchTerm.trim().length > 1) {
      const filtered = symptoms.filter(s => 
        s.toLowerCase().includes(searchTerm.toLowerCase().replace(/ /g, '_')) && 
        !selectedSymptoms.includes(s)
      ).slice(0, 8);
      setSuggestions(filtered);
    } else {
      setSuggestions([]);
    }
  }, [searchTerm, symptoms, selectedSymptoms]);

  const addSymptom = (symptom) => {
    setSelectedSymptoms([...selectedSymptoms, symptom]);
    setSearchTerm('');
    setSuggestions([]);
  };

  const removeSymptom = (symptom) => {
    setSelectedSymptoms(selectedSymptoms.filter(s => s !== symptom));
  };

  const diagnose = async () => {
    if (selectedSymptoms.length === 0) return;
    setIsDiagnosing(true);
    setResult(null);
    setError(null);
    
    try {
      const response = await axios.post(`/api/predict`, {
        symptoms: selectedSymptoms,
        lang: lang
      });
      
      setTimeout(() => {
        setResult(response.data);
        setIsDiagnosing(false);
        const el = document.getElementById('results-section');
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 800);
    } catch (err) {
      setError("Analysis failed. Please try again.");
      setIsDiagnosing(false);
    }
  };

  if (loading) {
    return (
      <div className="loader-overlay">
        <motion.div initial={{ scale: 0.8, opacity: 0 }} animate={{ scale: 1, opacity: 1 }}>
          <div className="nav-logo" style={{ fontSize: '42px', marginBottom: '12px' }}>HealthCare AI</div>
        </motion.div>
        <div className="ig-spinner"></div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <div className="background-animation">
        <Suspense fallback={null}>
          <Antigravity
            count={150}
            magnetRadius={12}
            ringRadius={15}
            waveSpeed={0.3}
            waveAmplitude={0.5}
            particleSize={1}
            color={'#0095f6'}
            autoAnimate={true}
            rotationSpeed={0.02}
          />
        </Suspense>
      </div>

      <header className="nav-header">
        <div className="nav-logo">{t.title}</div>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center', color: '#fff' }}>
          <div className="lang-selector">
            <Languages size={18} style={{ marginRight: '6px', color: '#0095f6' }} />
            <select 
              value={lang} 
              onChange={(e) => setLang(e.target.value)}
              style={{
                background: 'transparent',
                border: 'none',
                color: 'white',
                fontSize: '13px',
                outline: 'none',
                cursor: 'pointer'
              }}
            >
              {LANGUAGES.map(l => <option key={l.code} value={l.code} style={{ background: '#121212' }}>{l.name}</option>)}
            </select>
          </div>
          <Heart size={20} cursor="pointer" />
          <MessageCircle size={20} cursor="pointer" />
        </div>
      </header>

      <main className="main-feed">
        <section className="stories-container">
          {HEALTH_TIPS.map(tip => (
            <div key={tip.id} className="story-item" onClick={() => setShowStory(tip)} style={{ cursor: 'pointer' }}>
              <div className="story-circle">
                <div className="story-inner">{tip.icon}</div>
              </div>
              <span className="story-name">{tip.name}</span>
            </div>
          ))}
        </section>

        <motion.div className="diag-card" initial={{ y: 20, opacity: 0 }} animate={{ y: 0, opacity: 1 }}>
          <div className="diag-title">
            <Activity size={18} color="#0095f6" />
            <span>{t.assistant}</span>
          </div>

          <div className="symptom-select-container">
            <div style={{ position: 'relative', display: 'flex', gap: '8px' }}>
              <div style={{ flex: 1, position: 'relative' }}>
                <input 
                  type="text" 
                  placeholder={t.placeholder} 
                  style={{
                    width: '100%',
                    background: '#262626',
                    border: '1px solid #363636',
                    borderRadius: '8px',
                    padding: '12px 12px 12px 36px',
                    color: 'white',
                    fontSize: '14px',
                    outline: 'none'
                  }}
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                />
                <Search size={16} style={{ position: 'absolute', left: '12px', top: '13px', color: '#737373' }} />
                
                <AnimatePresence>
                  {suggestions.length > 0 && (
                    <motion.div className="suggestions-box" initial={{ opacity: 0, y: -5 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -5 }}>
                      {suggestions.map(s => (
                        <div key={s} className="suggestion-item" onClick={() => addSymptom(s)}>
                          {s.replace(/_/g, ' ')}
                        </div>
                      ))}
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
              <button 
                className="primary-btn" 
                style={{ width: 'auto', padding: '0 20px', height: '44px' }}
                onClick={diagnose}
                disabled={selectedSymptoms.length === 0 || isDiagnosing}
              >
                {isDiagnosing ? t.diagnosing : <Send size={18} />}
              </button>
            </div>

            <div className="symptom-chips">
              {selectedSymptoms.map(s => (
                <div key={s} className="symptom-chip" onClick={() => removeSymptom(s)}>
                  {s.replace(/_/g, ' ')}
                  <X size={12} />
                </div>
              ))}
            </div>
          </div>
          {error && <div style={{ color: '#ff4b4b', fontSize: '12px', marginTop: '10px', textAlign: 'center' }}>{error}</div>}
        </motion.div>

        <div id="results-section">
          <AnimatePresence>
            {result && (
              <motion.div className="result-container" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
                <div className="result-header" style={{ borderTop: '4px solid #00f08f' }}>
                  <div className="result-disease" style={{ fontSize: '26px', color: '#00f08f', textTransform: 'uppercase', letterSpacing: '2px', fontWeight: '800' }}>
                    {result.disease}
                  </div>
                  {result.description && (
                    <p style={{ margin: '16px 0 0 0', fontSize: '14px', color: '#ccc', lineHeight: '1.5' }}>
                      {result.description}
                    </p>
                  )}
                </div>

                <div className="info-section">
                  <div className="info-card">
                    <h4><ShieldAlert size={14} color="#ff4b4b" /> {t.precautions}</h4>
                    <ul className="info-list">
                      {result.precautions.map((p, i) => <li key={i}>{p}</li>)}
                    </ul>
                  </div>

                  <div className="info-card">
                    <h4><Home size={14} color="#00f08f" /> {t.remedies}</h4>
                    <ul className="info-list">
                      {result.remedies.map((r, i) => <li key={i}>{r}</li>)}
                    </ul>
                  </div>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        <footer className="disclaimer">
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px', marginBottom: '12px' }}>
            <AlertCircle size={20} color="#ff4b4b" />
            <strong style={{ fontSize: '18px', color: '#ff4b4b' }}>{t.disclaimer_title}</strong>
          </div>
          <p>{t.disclaimer_p1}</p>
          <p style={{ marginTop: '12px' }}>{t.disclaimer_p2}</p>
          <div style={{ marginTop: '32px', opacity: 0.3, fontSize: '10px' }}>PROCESSED BY {t.title.toUpperCase()} • VERCEL SECURE</div>
        </footer>
      </main>

      <AnimatePresence>
        {showStory && (
          <motion.div className="loader-overlay" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} onClick={() => setShowStory(null)} style={{ padding: '40px', zIndex: 2000 }}>
            <div style={{ position: 'absolute', top: '20px', right: '20px' }}><X size={32} /></div>
            <div style={{ fontSize: '80px', marginBottom: '20px' }}>{showStory.icon}</div>
            <h2 style={{ fontSize: '28px', margin: '0 0 12px 0' }}>{showStory.name} Tip</h2>
            <p style={{ fontSize: '18px', textAlign: 'center', maxWidth: '300px' }}>{showStory.text}</p>
            <div style={{ position: 'absolute', bottom: '60px', width: '80%', height: '3px', background: '#333' }}>
              <motion.div initial={{ width: 0 }} animate={{ width: '100%' }} transition={{ duration: 4 }} onAnimationComplete={() => setShowStory(null)} style={{ height: '100%', background: '#fff' }} />
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}

export default App;
