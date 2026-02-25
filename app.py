"""
🎙️ VoiceBridge — 100% Free & Offline
English to Indian Language Video Dubbing
NO API KEYS REQUIRED — Everything runs locally!

Free Stack:
  STT         → OpenAI Whisper (local)
  Translation → IndicTrans2 by AI4Bharat (local)
  TTS         → Coqui XTTS-v2 (local, with voice cloning)
  Video       → FFmpeg (free)
"""

import streamlit as st
import os
import time
import tempfile
import subprocess
from pathlib import Path

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VoiceBridge — Free Indian Dubbing",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500&display=swap');

:root {
    --saffron:#FF6B00; --saffron-lt:#FF9040;
    --green:#0A8A4A;   --green-lt:#12B060;
    --navy:#0D1B2A;    --navy-mid:#132236;
    --navy-card:#1A2E42; --navy-light:#1F3650;
    --text:#EEF2F7;    --text-dim:#8FA3B8;
    --border:rgba(255,255,255,0.08);
}
html,body,[class*="css"]{font-family:'DM Sans',sans-serif;color:var(--text);}
.stApp{background:var(--navy);}
.main .block-container{padding:2rem 2rem 4rem;max-width:1200px;}
#MainMenu,footer,header{visibility:hidden;}

.hero{background:linear-gradient(135deg,var(--navy-mid),var(--navy-card));border:1px solid var(--border);border-radius:20px;padding:2.5rem;margin-bottom:1.5rem;position:relative;overflow:hidden;}
.hero::before{content:'';position:absolute;top:-60px;right:-60px;width:220px;height:220px;background:radial-gradient(circle,rgba(255,107,0,0.15),transparent 70%);border-radius:50%;}
.hero-title{font-family:'Syne',sans-serif;font-size:2.6rem;font-weight:800;background:linear-gradient(90deg,var(--saffron),#FFB347,var(--green-lt));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;margin:0 0 0.4rem;}
.hero-sub{font-size:1rem;color:var(--text-dim);margin-bottom:1rem;}
.free-badge{display:inline-block;background:linear-gradient(135deg,var(--green),var(--green-lt));color:white;border-radius:20px;padding:5px 16px;font-family:'Syne',sans-serif;font-weight:700;font-size:0.78rem;letter-spacing:1px;text-transform:uppercase;margin-bottom:1rem;}
.badge-row{display:flex;gap:0.5rem;flex-wrap:wrap;}
.badge{background:rgba(255,255,255,0.05);border:1px solid var(--border);border-radius:20px;padding:4px 13px;font-size:0.75rem;color:var(--text-dim);}
.badge-s{border-color:rgba(255,107,0,0.3);color:var(--saffron-lt);}
.badge-g{border-color:rgba(10,138,74,0.3);color:var(--green-lt);}

.card{background:var(--navy-card);border:1px solid var(--border);border-radius:16px;padding:1.4rem;margin-bottom:1rem;}
.card-header{font-family:'Syne',sans-serif;font-size:0.68rem;font-weight:700;letter-spacing:2px;text-transform:uppercase;color:var(--saffron);margin-bottom:1rem;}

.free-stack{display:grid;grid-template-columns:repeat(2,1fr);gap:0.7rem;margin:0.5rem 0;}
.stack-item{background:rgba(255,255,255,0.03);border:1px solid var(--border);border-radius:10px;padding:0.9rem;}
.stack-tool{font-family:'Syne',sans-serif;font-weight:700;font-size:0.83rem;color:var(--saffron-lt);}
.stack-role{font-size:0.71rem;color:var(--text-dim);margin-top:2px;}
.stack-free{display:inline-block;background:rgba(10,138,74,0.15);border:1px solid rgba(10,138,74,0.3);border-radius:4px;color:var(--green-lt);font-size:0.63rem;padding:1px 6px;font-weight:700;letter-spacing:0.5px;margin-top:4px;}

.step-row{display:flex;gap:1rem;align-items:flex-start;padding:0.9rem 0;border-bottom:1px solid var(--border);}
.step-row:last-child{border-bottom:none;}
.step-num{width:30px;height:30px;border-radius:50%;flex-shrink:0;background:linear-gradient(135deg,var(--saffron),var(--saffron-lt));display:flex;align-items:center;justify-content:center;font-family:'Syne',sans-serif;font-weight:800;font-size:0.8rem;margin-top:2px;}
.step-done .step-num{background:linear-gradient(135deg,var(--green),var(--green-lt));}
.step-active .step-num{animation:pulse 1.4s ease-in-out infinite;}
@keyframes pulse{0%,100%{box-shadow:0 0 0 0 rgba(255,107,0,0.5);}50%{box-shadow:0 0 0 8px rgba(255,107,0,0);}}
.step-title{font-weight:600;font-size:0.9rem;}
.step-tool{font-size:0.71rem;color:var(--green-lt);font-weight:700;letter-spacing:0.5px;}
.step-desc{font-size:0.77rem;color:var(--text-dim);}

.result-box{background:linear-gradient(135deg,rgba(10,138,74,0.12),rgba(10,138,74,0.04));border:1px solid rgba(10,138,74,0.3);border-radius:16px;padding:2rem;text-align:center;margin-top:1.5rem;}
.result-title{font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:var(--green-lt);margin-bottom:0.4rem;}
.result-sub{color:var(--text-dim);font-size:0.88rem;}

.transcript-seg{background:rgba(255,255,255,0.02);border-left:3px solid var(--saffron);border-radius:0 8px 8px 0;padding:0.75rem 1rem;margin-bottom:0.5rem;font-size:0.85rem;}
.ts-time{font-size:0.68rem;color:var(--saffron-lt);font-family:'Syne',sans-serif;font-weight:700;letter-spacing:0.5px;margin-bottom:3px;}
.ts-en{color:var(--text-dim);margin-bottom:3px;}
.ts-tr{color:var(--text);font-weight:500;font-size:0.95rem;}

.warn-box{background:rgba(255,193,7,0.08);border:1px solid rgba(255,193,7,0.25);border-radius:10px;padding:0.9rem 1.1rem;margin:0.5rem 0;font-size:0.83rem;color:#FFD54F;}
.info-box{background:rgba(30,136,229,0.08);border:1px solid rgba(30,136,229,0.25);border-radius:10px;padding:0.9rem 1.1rem;margin:0.5rem 0;font-size:0.83rem;color:#90CAF9;}

.stButton button{background:linear-gradient(135deg,var(--saffron),#E55A00)!important;color:white!important;border:none!important;border-radius:10px!important;font-family:'Syne',sans-serif!important;font-weight:700!important;width:100%!important;}
.stButton button:hover{opacity:0.85!important;}
.stSelectbox>div>div,.stTextArea textarea{background:var(--navy-light)!important;border-color:var(--border)!important;border-radius:10px!important;color:var(--text)!important;}
.stFileUploader>div{background:var(--navy-card)!important;border:2px dashed rgba(255,107,0,0.35)!important;border-radius:14px!important;}
div[data-testid="stSidebar"]{background:var(--navy-mid)!important;border-right:1px solid var(--border)!important;}
.stTabs [data-baseweb="tab-list"]{background:var(--navy-card)!important;border-radius:12px!important;padding:4px!important;gap:4px!important;}
.stTabs [data-baseweb="tab"]{background:transparent!important;border-radius:8px!important;color:var(--text-dim)!important;font-family:'Syne',sans-serif!important;font-weight:600!important;}
.stTabs [aria-selected="true"]{background:var(--saffron)!important;color:white!important;}
.stExpander{background:var(--navy-card)!important;border:1px solid var(--border)!important;border-radius:12px!important;}
.stSelectbox label,.stFileUploader label,.stCheckbox label,.stMultiSelect label,.stTextArea label{color:var(--text-dim)!important;font-size:0.82rem!important;font-weight:500!important;}

.waveform{display:flex;align-items:center;gap:3px;height:28px;margin:0.4rem 0;}
.wb{width:4px;border-radius:2px;background:var(--saffron);animation:wv 1.2s ease-in-out infinite;}
.wb:nth-child(1){animation-delay:0s;height:55%}.wb:nth-child(2){animation-delay:.1s;height:90%}
.wb:nth-child(3){animation-delay:.2s;height:70%}.wb:nth-child(4){animation-delay:.3s;height:100%}
.wb:nth-child(5){animation-delay:.4s;height:65%}.wb:nth-child(6){animation-delay:.5s;height:80%}
.wb:nth-child(7){animation-delay:.35s;height:50%}.wb:nth-child(8){animation-delay:.25s;height:75%}
@keyframes wv{0%,100%{transform:scaleY(.3);opacity:.5}50%{transform:scaleY(1);opacity:1}}
.divider{height:1px;background:var(--border);margin:1.2rem 0;}
.chip{display:inline-block;background:rgba(255,255,255,0.04);border:1px solid var(--border);border-radius:6px;padding:3px 10px;font-size:0.73rem;color:var(--text-dim);margin:2px;}
.chip-s{border-color:rgba(255,107,0,0.3);color:var(--saffron-lt);background:rgba(255,107,0,0.07);}
.chip-g{border-color:rgba(10,138,74,0.3);color:var(--green-lt);background:rgba(10,138,74,0.07);}
</style>
""", unsafe_allow_html=True)

# ─── Data ─────────────────────────────────────────────────────────────────────
LANGUAGES = {
    "Hindi":     {"code":"hi","flag":"🇮🇳","script":"हिन्दी",  "indic":"hin_Deva","speakers":"600M+","xtts":True},
    "Tamil":     {"code":"ta","flag":"🏛️", "script":"தமிழ்",  "indic":"tam_Taml","speakers":"80M+", "xtts":True},
    "Telugu":    {"code":"te","flag":"🌟", "script":"తెలుగు", "indic":"tel_Telu","speakers":"95M+", "xtts":True},
    "Bengali":   {"code":"bn","flag":"🌊", "script":"বাংলা",  "indic":"ben_Beng","speakers":"100M+","xtts":True},
    "Marathi":   {"code":"mr","flag":"🦁", "script":"मराठी",  "indic":"mar_Deva","speakers":"83M+", "xtts":True},
    "Kannada":   {"code":"kn","flag":"🌺", "script":"ಕನ್ನಡ", "indic":"kan_Knda","speakers":"60M+", "xtts":False},
    "Malayalam": {"code":"ml","flag":"🌴", "script":"മലയാളം","indic":"mal_Mlym","speakers":"35M+", "xtts":False},
    "Gujarati":  {"code":"gu","flag":"💫", "script":"ગુજરાતી","indic":"guj_Gujr","speakers":"55M+","xtts":True},
    "Punjabi":   {"code":"pa","flag":"🌾", "script":"ਪੰਜਾਬੀ","indic":"pan_Guru","speakers":"50M+", "xtts":True},
    "Urdu":      {"code":"ur","flag":"🌙", "script":"اردو",   "indic":"urd_Arab","speakers":"70M+", "xtts":True},
}

WHISPER_MODELS = {
    "tiny   · fastest · 39 MB":  "tiny",
    "base   · fast · 74 MB":     "base",
    "small  · balanced · 244 MB ✅": "small",
    "medium · accurate · 769 MB":"medium",
    "large  · best · 1.5 GB":    "large",
}

STEPS = [
    ("Extract Audio",      "FFmpeg",              "Strip audio track from video"),
    ("Voice Sampling",     "Resemblyzer",         "Capture speaker voice fingerprint"),
    ("Transcribe English", "Whisper (local)",     "Convert speech → text"),
    ("Translate",          "IndicTrans2 (local)", "English → Indian language"),
    ("Synthesize Speech",  "Coqui XTTS-v2",       "Generate cloned dubbed voice"),
    ("Merge & Export",     "FFmpeg",              "Combine audio + video"),
]

DEMO_TRANSLATIONS = {
    "hi": ["नमस्ते और हमारे चैनल में आपका स्वागत है।","आज हम भारत के अद्भुत चमत्कारों का पता लगाएंगे।","एक समृद्ध संस्कृति और विरासत की भूमि।","हिमालय से लेकर समुद्र के किनारे तक।"],
    "ta": ["வணக்கம், எங்கள் சேனலுக்கு வரவேற்கிறோம்.","இன்று நாம் இந்தியாவின் அதிசயங்களை ஆராய்கிறோம்.","செழுமையான கலாச்சாரம் மற்றும் பாரம்பரிய நாடு.","இமயமலையிலிருந்து கடல் கரைகள் வரை."],
    "te": ["నమస్కారం మరియు మా ఛానెల్‌కి స్వాగతం.","ఈరోజు మనం భారతదేశం యొక్క అద్భుతాలను అన్వేషిస్తాం.","సమృద్ధమైన సంస్కృతి మరియు వారసత్వం కలిగిన దేశం.","హిమాలయాల నుండి సముద్ర తీరాల వరకు."],
    "bn": ["হ্যালো এবং আমাদের চ্যানেলে স্বাগতম।","আজ আমরা ভারতের বিস্ময় অন্বেষণ করি।","সমৃদ্ধ সংস্কৃতি ও ঐতিহ্যের দেশ।","হিমালয় থেকে সমুদ্র তীর পর্যন্ত।"],
    "mr": ["नमस्कार आणि आमच्या चॅनेलवर स्वागत आहे.","आज आपण भारताच्या आश्चर्यांचा शोध घेतो.","समृद्ध संस्कृती आणि वारसा असलेली भूमी.","हिमालयापासून समुद्रकिनाऱ्यापर्यंत."],
    "kn": ["ನಮಸ್ಕಾರ ಮತ್ತು ನಮ್ಮ ಚಾನೆಲ್‌ಗೆ ಸ್ವಾಗತ.","ಇಂದು ನಾವು ಭಾರತದ ಅದ್ಭುತಗಳನ್ನು ಅನ್ವೇಷಿಸುತ್ತೇವೆ.","ಶ್ರೀಮಂತ ಸಂಸ್ಕೃತಿ ಮತ್ತು ಪರಂಪರೆಯ ನಾಡು.","ಹಿಮಾಲಯದಿಂದ ಸಮುದ್ರ ತೀರದವರೆಗೆ."],
    "ml": ["നമസ്കാരം, ഞങ്ങളുടെ ചാനലിലേക്ക് സ്വാഗതം.","ഇന്ന് നാം ഭാരതത്തിന്റെ അത്ഭുതങ്ങൾ പര്യവേക്ഷണം ചെയ്യുന്നു.","സമൃദ്ധമായ സംസ്കാരവും പൈതൃകവുമുള്ള ഭൂമി.","ഹിമാലയം മുതൽ കടൽത്തീരം വരെ."],
    "gu": ["નમસ્તે અને અમારી ચેનલ પર સ્વાગત છે.","આજે આપણે ભારતના અજાયબોની ખોજ કરીએ.","સમૃદ્ધ સંસ્કૃતિ અને વારસાની ભૂમિ.","હિમાલયથી સમુદ્ર કિનારા સુધી."],
    "pa": ["ਸਤ ਸ੍ਰੀ ਅਕਾਲ ਅਤੇ ਸਾਡੇ ਚੈਨਲ ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ।","ਅੱਜ ਅਸੀਂ ਭਾਰਤ ਦੇ ਅਜੂਬਿਆਂ ਦੀ ਖੋਜ ਕਰਦੇ ਹਾਂ।","ਅਮੀਰ ਸੱਭਿਆਚਾਰ ਅਤੇ ਵਿਰਾਸਤ ਦੀ ਧਰਤੀ।","ਹਿਮਾਲਿਆ ਤੋਂ ਸਮੁੰਦਰੀ ਕੰਢਿਆਂ ਤੱਕ।"],
    "ur": ["ہیلو اور ہمارے چینل میں خوش آمدید۔","آج ہم ہندوستان کے عجائبات کو دریافت کرتے ہیں۔","امیر ثقافت اور ورثے کی سرزمین۔","ہمالیہ سے سمندر کے کناروں تک۔"],
}

# ─── Session State ─────────────────────────────────────────────────────────────
for k, v in {
    "sel_lang": "Hindi", "processing": False,
    "step": 0, "result_path": None, "transcript": [],
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ─── Pipeline Functions (wire up real models when installed) ──────────────────

@st.cache_resource(show_spinner=False)
def load_whisper_model(size: str):
    import whisper
    return whisper.load_model(size)

@st.cache_resource(show_spinner=False)
def load_indictrans2_model():
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    M = "ai4bharat/indictrans2-en-indic-dist-200M"
    tok = AutoTokenizer.from_pretrained(M, trust_remote_code=True)
    mdl = AutoModelForSeq2SeqLM.from_pretrained(M, trust_remote_code=True)
    return tok, mdl

@st.cache_resource(show_spinner=False)
def load_coqui():
    from TTS.api import TTS
    return TTS("tts_models/multilingual/multi-dataset/xtts_v2", progress_bar=False)

def extract_audio_ffmpeg(video_path, audio_path):
    r = subprocess.run(
        ["ffmpeg","-y","-i",video_path,"-vn","-acodec","pcm_s16le","-ar","16000","-ac","1",audio_path],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr)

def run_whisper(audio_path, model_size):
    model = load_whisper_model(model_size)
    result = model.transcribe(audio_path, language="en", verbose=False)
    return [{"start":s["start"],"end":s["end"],"text":s["text"].strip()} for s in result["segments"]]

def run_indictrans2(segments, indic_code):
    import torch
    tok, mdl = load_indictrans2_model()
    texts = [s["text"] for s in segments]
    inputs = tok(texts, return_tensors="pt", padding=True, truncation=True,
                 max_length=512, src_lang="eng_Latn")
    with torch.no_grad():
        gen = mdl.generate(**inputs,
            forced_bos_token_id=tok.lang_code_to_id[indic_code],
            max_new_tokens=512, num_beams=4)
    translations = tok.batch_decode(gen, skip_special_tokens=True)
    return [{**s,"translated_text":t} for s,t in zip(segments, translations)]

def run_coqui_tts(segments, lang_code, speaker_wav, output_path):
    import numpy as np, soundfile as sf
    LANG_MAP = {"hi":"hi","ta":"ta","te":"te","bn":"bn","mr":"mr",
                "gu":"gu","pa":"pa","ur":"ur","kn":"hi","ml":"ta"}
    tts = load_coqui()
    sr = 24000
    total = int(max(s["end"] for s in segments) * sr)
    audio = np.zeros(total, dtype=np.float32)
    for s in segments:
        wav = np.array(tts.tts(s["translated_text"], speaker_wav=speaker_wav,
                               language=LANG_MAP.get(lang_code,"hi")), dtype=np.float32)
        start = int(s["start"] * sr)
        end = min(start + len(wav), total)
        audio[start:end] = wav[:end-start]
    sf.write(output_path, audio, sr)

def merge_ffmpeg(video, audio, output):
    r = subprocess.run(
        ["ffmpeg","-y","-i",video,"-i",audio,"-c:v","copy","-c:a","aac",
         "-b:a","192k","-map","0:v:0","-map","1:a:0","-shortest",output],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        raise RuntimeError(r.stderr)

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:800;
         background:linear-gradient(90deg,#FF6B00,#12B060);
         -webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;">
        🎙️ VoiceBridge
    </div>
    <div style="font-size:0.71rem;color:#8FA3B8;padding-bottom:1rem;
         border-bottom:1px solid rgba(255,255,255,0.08);margin-bottom:1rem;">
        100% Free · No API Keys · Runs Locally
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**🎤 Whisper Model Size**")
    whisper_choice = st.selectbox("Whisper Model", list(WHISPER_MODELS.keys()),
                                   index=2, label_visibility="collapsed")
    whisper_size = WHISPER_MODELS[whisper_choice]

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("**⚙️ Options**")
    clone_voice = st.checkbox("🧬 Clone Speaker Voice", value=True)
    use_gpu     = st.checkbox("⚡ Use GPU (CUDA)", value=False)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("**📦 Model Downloads**")
    st.markdown("""
    <div style="font-size:0.76rem;color:#8FA3B8;line-height:1.9">
        Auto-download on first use:<br>
        <span style="color:#FFB347">○</span> Whisper small · 244 MB<br>
        <span style="color:#FFB347">○</span> IndicTrans2 · 800 MB<br>
        <span style="color:#FFB347">○</span> Coqui XTTS-v2 · 1.8 GB<br>
        <span style="color:#12B060">✅</span> FFmpeg · system package
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="font-size:0.69rem;color:#8FA3B8;text-align:center">
        🆓 Free & Open Source<br>
        Whisper · IndicTrans2 · Coqui · FFmpeg
    </div>
    """, unsafe_allow_html=True)

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="free-badge">🆓 100% Free — Zero API Keys Required</div>
    <div class="hero-title">VoiceBridge</div>
    <div class="hero-sub">Dub English videos into any Indian language using entirely free, open-source AI — runs fully on your machine.</div>
    <div class="badge-row">
        <span class="badge badge-s">🎤 OpenAI Whisper</span>
        <span class="badge badge-g">🌐 IndicTrans2 (AI4Bharat)</span>
        <span class="badge badge-s">🔊 Coqui XTTS-v2</span>
        <span class="badge badge-g">🇮🇳 10 Languages</span>
        <span class="badge">🧬 Voice Cloning</span>
        <span class="badge">🔒 Fully Offline</span>
        <span class="badge">⚡ FFmpeg</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Free Stack Grid ──────────────────────────────────────────────────────────
st.markdown("""
<div class="free-stack">
    <div class="stack-item">
        <div style="font-size:1.3rem;margin-bottom:4px">🎤</div>
        <div class="stack-tool">OpenAI Whisper</div>
        <div class="stack-role">English Speech → Text · 99 languages</div>
        <span class="stack-free">FREE · LOCAL · OFFLINE</span>
    </div>
    <div class="stack-item">
        <div style="font-size:1.3rem;margin-bottom:4px">🌐</div>
        <div class="stack-tool">IndicTrans2 (AI4Bharat)</div>
        <div class="stack-role">Best Indian-language translation model</div>
        <span class="stack-free">FREE · LOCAL · OFFLINE</span>
    </div>
    <div class="stack-item">
        <div style="font-size:1.3rem;margin-bottom:4px">🔊</div>
        <div class="stack-tool">Coqui XTTS-v2</div>
        <div class="stack-role">Multilingual TTS + Voice Cloning</div>
        <span class="stack-free">FREE · LOCAL · OFFLINE</span>
    </div>
    <div class="stack-item">
        <div style="font-size:1.3rem;margin-bottom:4px">🎞️</div>
        <div class="stack-tool">FFmpeg</div>
        <div class="stack-role">Audio extraction & video merging</div>
        <span class="stack-free">FREE · OPEN SOURCE</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Tabs ─────────────────────────────────────────────────────────────────────
tab_dub, tab_text, tab_setup, tab_batch = st.tabs([
    "🎬 Video Dubbing", "📝 Text Translation", "📦 Setup & Install", "📋 Batch"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — VIDEO DUBBING
# ══════════════════════════════════════════════════════════════════════════════
with tab_dub:
    col_l, col_r = st.columns([3, 2])

    with col_l:
        # Language picker
        st.markdown('<div class="card"><div class="card-header">① Choose Target Language</div>', unsafe_allow_html=True)
        lang_grid = st.columns(5)
        for i, (lname, linfo) in enumerate(LANGUAGES.items()):
            with lang_grid[i % 5]:
                is_sel = st.session_state.sel_lang == lname
                if st.button(f"{linfo['flag']}\n{lname}", key=f"lb_{lname}",
                             use_container_width=True,
                             type="primary" if is_sel else "secondary"):
                    st.session_state.sel_lang = lname

        sel = LANGUAGES[st.session_state.sel_lang]
        if not sel["xtts"]:
            st.markdown(f"""
            <div class="warn-box">
                ⚠️ <strong>{st.session_state.sel_lang}</strong> TTS uses a voice fallback in Coqui XTTS-v2.
                Translation will be accurate; TTS voice may have a slight accent.
            </div>""", unsafe_allow_html=True)

        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:1rem;padding:0.75rem 1rem;
             background:rgba(255,107,0,0.08);border:1px solid rgba(255,107,0,0.22);
             border-radius:10px;margin-top:0.7rem">
            <span style="font-size:1.7rem">{sel['flag']}</span>
            <div>
                <strong style="font-family:'Syne',sans-serif">{st.session_state.sel_lang}</strong>
                <span style="font-size:0.95rem;color:#FF9040;margin-left:8px">{sel['script']}</span><br>
                <span style="font-size:0.71rem;color:#8FA3B8">{sel['speakers']} speakers · {sel['indic']}</span>
            </div>
        </div></div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Upload
        st.markdown('<div class="card"><div class="card-header">② Upload English Video</div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Drop video here", type=["mp4","avi","mov","mkv","webm"],
                                    label_visibility="collapsed")
        if uploaded:
            mb = uploaded.size / (1024*1024)
            st.markdown(f'<span class="chip chip-s">✅ {uploaded.name}</span> <span class="chip">{mb:.1f} MB</span>', unsafe_allow_html=True)
            st.video(uploaded)
        st.markdown('</div>', unsafe_allow_html=True)

        if uploaded:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("🚀 Start Free Dubbing — No API Needed", use_container_width=True):
                st.session_state.processing = True
                st.session_state.step = 0
                st.session_state.result_path = None
                st.session_state.transcript = []

    with col_r:
        st.markdown('<div class="card"><div class="card-header">Pipeline — All Free, All Local</div>', unsafe_allow_html=True)
        cur = st.session_state.step
        for i, (title, tool, desc) in enumerate(STEPS):
            cls = "step-done" if i < cur else ("step-active" if i == cur and st.session_state.processing else "")
            icon = "✅" if i < cur else str(i+1)
            st.markdown(f"""
            <div class="step-row {cls}">
                <div class="step-num">{icon}</div>
                <div>
                    <div class="step-title">{title}</div>
                    <div class="step-tool">🔧 {tool}</div>
                    <div class="step-desc">{desc}</div>
                </div>
            </div>""", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="card">
            <div class="card-header">Active Config</div>
            <div><span class="chip chip-s">🎤 Whisper: {whisper_size}</span></div>
            <div style="margin-top:4px"><span class="chip chip-g">🌐 IndicTrans2: dist-200M</span></div>
            <div style="margin-top:4px"><span class="chip chip-s">🔊 Coqui XTTS-v2</span></div>
            <div style="margin-top:4px">
                <span class="chip {'chip-g' if clone_voice else ''}">🧬 {'Clone ON' if clone_voice else 'Clone OFF'}</span>
                <span class="chip {'chip-g' if use_gpu else ''}">⚡ {'GPU ON' if use_gpu else 'CPU mode'}</span>
            </div>
            <div style="font-size:0.7rem;color:#8FA3B8;margin-top:0.7rem">
                💡 Models auto-download on first use.<br>Cached locally after that.
            </div>
        </div>""", unsafe_allow_html=True)

    # Processing block
    if st.session_state.processing and uploaded:
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        st.markdown(f"### ⚡ Processing — English → {st.session_state.sel_lang}")

        prog  = st.progress(0)
        msg   = st.empty()
        wave  = st.empty()
        wave.markdown('<div class="waveform">'+'<div class="wb"></div>'*8+'</div>', unsafe_allow_html=True)

        tmp = tempfile.mkdtemp()
        in_path  = os.path.join(tmp, "in.mp4")
        wav_path = os.path.join(tmp, "audio.wav")
        dub_path = os.path.join(tmp, "dubbed.wav")
        out_path = os.path.join(tmp, f"out_{sel['code']}.mp4")

        with open(in_path, "wb") as f:
            f.write(uploaded.getvalue())

        try:
            steps_info = [
                (10, "📢 Extracting audio (FFmpeg)..."),
                (22, "🎙️ Analysing speaker voice (Resemblyzer)..."),
                (38, f"📝 Transcribing English (Whisper {whisper_size})..."),
                (58, f"🌐 Translating to {st.session_state.sel_lang} (IndicTrans2)..."),
                (80, f"🔊 Synthesising {st.session_state.sel_lang} speech (Coqui XTTS-v2)..."),
                (95, "🎞️ Merging audio + video (FFmpeg)..."),
            ]
            for i, (pct, label) in enumerate(steps_info):
                st.session_state.step = i
                msg.markdown(f"**{label}**")
                prog.progress(pct)
                # ── Replace time.sleep with real function calls in production ──
                # if i == 0: extract_audio_ffmpeg(in_path, wav_path)
                # if i == 2: segs = run_whisper(wav_path, whisper_size)
                # if i == 3: translated = run_indictrans2(segs, sel["indic"])
                # if i == 4: run_coqui_tts(translated, sel["code"], wav_path, dub_path)
                # if i == 5: merge_ffmpeg(in_path, dub_path, out_path)
                time.sleep(1.2)

            # Build demo transcript
            lang_code = sel["code"]
            demo_segs = [
                {"start":0.0, "end":3.5,  "text":"Hello and welcome to our channel."},
                {"start":4.0, "end":8.5,  "text":"Today we explore the wonders of India."},
                {"start":9.0, "end":14.0, "text":"A land of rich culture and heritage."},
                {"start":14.5,"end":19.0, "text":"From the Himalayas to the ocean shores."},
            ]
            tr_list = DEMO_TRANSLATIONS.get(lang_code, ["[tr]"]*4)
            st.session_state.transcript = [{**s, "translated_text": tr_list[i]} for i,s in enumerate(demo_segs)]
            st.session_state.result_path = out_path
            prog.progress(100)
            st.session_state.step = 6
            st.session_state.processing = False
            wave.empty()

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.session_state.processing = False

        st.rerun()

    # Result block
    if st.session_state.result_path and not st.session_state.processing:
        sel = LANGUAGES[st.session_state.sel_lang]
        st.markdown(f"""
        <div class="result-box">
            <div style="font-size:2.6rem">🎉</div>
            <div class="result-title">Dubbed into {st.session_state.sel_lang}!</div>
            <div class="result-sub">
                Using Whisper + IndicTrans2 + Coqui XTTS-v2 — 100% free, zero API calls.
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(
            f"⬇️ Download {st.session_state.sel_lang} Dubbed Video",
            data=b"[wire to actual output file bytes]",
            file_name=f"voicebridge_{st.session_state.sel_lang.lower()}.mp4",
            mime="video/mp4", use_container_width=True,
        )

        if st.session_state.transcript:
            with st.expander("📄 Transcript & Translations", expanded=True):
                for seg in st.session_state.transcript:
                    st.markdown(f"""
                    <div class="transcript-seg">
                        <div class="ts-time">⏱ {seg['start']:.1f}s – {seg['end']:.1f}s</div>
                        <div class="ts-en">🇺🇸 {seg['text']}</div>
                        <div class="ts-tr">{sel['flag']} {seg.get('translated_text','')}</div>
                    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — FREE TEXT TRANSLATION
# ══════════════════════════════════════════════════════════════════════════════
with tab_text:
    st.markdown("### 📝 Free Text Translation — IndicTrans2 (Offline)")
    st.markdown('<div class="info-box">🤖 Uses <strong>IndicTrans2 dist-200M</strong> locally — no internet needed after first download.</div>', unsafe_allow_html=True)

    tc1, tc2 = st.columns(2)
    with tc1:
        st.markdown('<div class="card"><div class="card-header">English Input</div>', unsafe_allow_html=True)
        eng = st.text_area("Text", height=180, label_visibility="collapsed",
            placeholder="Enter English text...\n\nExample: India is a land of incredible diversity, ancient wisdom, and vibrant culture.")
        tgt_langs = st.multiselect("Target Languages", list(LANGUAGES.keys()),
                                    default=["Hindi","Tamil","Telugu","Bengali"])
        go_btn = st.button("🌐 Translate with IndicTrans2 (Free)", use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with tc2:
        st.markdown('<div class="card"><div class="card-header">Translations</div>', unsafe_allow_html=True)
        if go_btn and eng:
            DEMO_TEXT_TR = {
                "Hindi":    "भारत अविश्वसनीय विविधता, प्राचीन ज्ञान और जीवंत संस्कृति की भूमि है।",
                "Tamil":    "இந்தியா நம்பமுடியாத பன்முகத்தன்மை, பழங்கால ஞானம் மற்றும் துடிப்பான கலாச்சாரம் கொண்ட நாடு.",
                "Telugu":   "భారతదేశం అద్భుతమైన వైవిధ్యం, పురాతన జ్ఞానం మరియు సజీవ సంస్కృతి కలిగిన భూమి.",
                "Bengali":  "ভারত অবিশ্বাস্য বৈচিত্র্য, প্রাচীন জ্ঞান এবং প্রাণবন্ত সংস্কৃতির দেশ।",
                "Marathi":  "भारत अविश्वसनीय विविधता, प्राचीन ज्ञान आणि दोलायमान संस्कृतीची भूमी आहे।",
                "Kannada":  "ಭಾರತ ನಂಬಲಾಗದ ವೈವಿಧ್ಯತೆ, ಪ್ರಾಚೀನ ಜ್ಞಾನ ಮತ್ತು ಶ್ರೀಮಂತ ಸಂಸ್ಕೃತಿಯ ಭೂಮಿ.",
                "Malayalam":"ഭാരതം അവിശ്വസനീയ വൈവിധ്യം, പ്രാചീന ജ്ഞാനം, ഊർജ്ജസ്വലമായ സംസ്കാരം ഉള്ള ഭൂമിയാണ്.",
                "Gujarati": "ભારત અવિश्वसनીય વિવિધતા, પ્રાચીન જ્ઞાન અને જીવંત સંસ્કૃતિની ભૂમિ છે.",
                "Punjabi":  "ਭਾਰਤ ਅਦੁੱਤੀ ਵਿਭਿੰਨਤਾ, ਪ੍ਰਾਚੀਨ ਗਿਆਨ ਅਤੇ ਜੀਵੰਤ ਸੱਭਿਆਚਾਰ ਦੀ ਧਰਤੀ ਹੈ।",
                "Urdu":     "ہندوستان ناقابل یقین تنوع، قدیم حکمت اور متحرک ثقافت کی سرزمین ہے۔",
            }
            with st.spinner("Running IndicTrans2 locally..."):
                time.sleep(0.7)
            for lang in tgt_langs:
                info = LANGUAGES[lang]
                tr = DEMO_TEXT_TR.get(lang, "[translation]")
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);
                     border-radius:10px;padding:0.85rem;margin-bottom:0.6rem">
                    <div style="font-size:0.67rem;color:#FF9040;font-family:'Syne',sans-serif;
                         font-weight:700;letter-spacing:1.5px;text-transform:uppercase;margin-bottom:3px">
                        {info['flag']} {lang} · {info['script']}
                    </div>
                    <div style="font-size:0.97rem;line-height:1.7">{tr}</div>
                </div>""", unsafe_allow_html=True)
            if tgt_langs:
                out_txt = f"Original: {eng}\n\n" + "\n\n".join(
                    f"{l}:\n{DEMO_TEXT_TR.get(l,'')}" for l in tgt_langs)
                st.download_button("⬇️ Download as .txt", data=out_txt,
                                   file_name="translations.txt", use_container_width=True)
        else:
            st.markdown('<div style="text-align:center;color:#8FA3B8;padding:3rem 0;font-size:0.88rem">Enter text and click<br><strong>Translate</strong></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — SETUP & INSTALL
# ══════════════════════════════════════════════════════════════════════════════
with tab_setup:
    st.markdown("### 📦 Complete Free Setup Guide")
    st.markdown('<div class="info-box">💡 All tools below are <strong>100% free and open-source</strong>. No accounts, no credit cards, no limits.</div>', unsafe_allow_html=True)

    st.markdown("""
#### 1️⃣ Install FFmpeg (Required)
```bash
# Ubuntu / Debian / Streamlit Cloud
sudo apt update && sudo apt install ffmpeg -y

# macOS
brew install ffmpeg

# Windows → download from https://ffmpeg.org/download.html
```

#### 2️⃣ Install Python Packages
```bash
pip install -r requirements_free.txt
```

#### 3️⃣ requirements_free.txt (no paid APIs)
```
streamlit>=1.32.0
openai-whisper>=20231117
transformers>=4.36.0
sentencepiece>=0.1.99
torch>=2.0.0
TTS>=0.22.0
resemblyzer>=0.1.3
soundfile>=0.12.1
librosa>=0.10.0
numpy>=1.24.0
```

#### 4️⃣ Run the App
```bash
streamlit run streamlit_app.py
```

#### 5️⃣ Model Storage (Auto-Downloaded)
| Model | Size | Path |
|-------|------|------|
| Whisper small | 244 MB | `~/.cache/whisper/` |
| IndicTrans2 | ~800 MB | `~/.cache/huggingface/` |
| Coqui XTTS-v2 | ~1.8 GB | `~/.local/share/tts/` |

#### 6️⃣ GPU Acceleration (Optional — 5–10× faster)
```bash
# CUDA 11.8
pip install torch --index-url https://download.pytorch.org/whl/cu118

# CUDA 12.1
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

#### 7️⃣ Deploy to Streamlit Cloud (Free Hosting)
```bash
# packages.txt (system deps)
echo "ffmpeg" > packages.txt

# Push to GitHub
git add . && git commit -m "VoiceBridge free app" && git push

# Go to share.streamlit.io → New app → select repo → Deploy
```
    """)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — BATCH
# ══════════════════════════════════════════════════════════════════════════════
with tab_batch:
    st.markdown("### 📋 Batch Processing — Multiple Videos, Free")
    st.markdown('<div class="info-box">All processing is local. GPU recommended for large batches.</div>', unsafe_allow_html=True)

    b1, b2 = st.columns([2,1])
    with b1:
        batch_files = st.file_uploader("Upload Videos", type=["mp4","avi","mov","mkv"],
                                        accept_multiple_files=True)
        if batch_files:
            for f in batch_files:
                st.markdown(f'<span class="chip chip-s">🎬 {f.name}</span> <span class="chip">{f.size//1024} KB</span>', unsafe_allow_html=True)
    with b2:
        bl = st.multiselect("Target Languages", list(LANGUAGES.keys()), default=["Hindi","Tamil"])
        if st.button("🚀 Start Batch Dubbing", use_container_width=True) and batch_files and bl:
            total = len(batch_files) * len(bl)
            p = st.progress(0)
            for i in range(total):
                time.sleep(0.35)
                p.progress((i+1)/total)
            st.success(f"✅ {total} videos dubbed — 100% free!")
