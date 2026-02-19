import streamlit as st
from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import json
import time

# ======================================================
# PAGE CONFIG
# ======================================================
st.set_page_config(
    page_title="Early Metabolic Risk Assessment (Research Demo)",
    layout="centered"
)

# ======================================================
# MODERN UI STYLES - NEUMORPHISM + GRADIENTS
# ======================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Inter', sans-serif;
}

.main-title {
    font-size: 2.2rem;
    font-weight: 700;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

.caption-box {
    background: rgba(255, 255, 255, 0.85);
    backdrop-filter: blur(10px);
    padding: 14px 18px;
    border-radius: 24px;
    color: #555;
    font-size: 0.9rem;
    margin-bottom: 2rem;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.3);
    box-shadow: 
        0 8px 32px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);
}

.input-card {
    background: linear-gradient(145deg, #ffffff, #f5f7fa);
    padding: 22px;
    border-radius: 28px;
    margin-bottom: 26px;
    border: 1px solid rgba(229, 231, 235, 0.5);
    box-shadow: 
        20px 20px 60px rgba(0, 0, 0, 0.05),
        -20px -20px 60px rgba(255, 255, 255, 0.8);
    transition: transform 0.3s ease;
}

.input-card:hover {
    transform: translateY(-2px);
}

/* Modern Input Styling */
.stNumberInput > div > div > input {
    background: rgba(249, 250, 251, 0.9);
    border: 2px solid #e5e7eb;
    border-radius: 16px;
    padding: 0.75rem 1rem;
    font-size: 1rem;
    font-weight: 500;
    color: #111827;
    transition: all 0.3s ease;
}

.stNumberInput > div > div > input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
    background: white;
}

/* Animated Percentage Display */
.percent-container {
    position: relative;
    margin: 3rem 0;
    text-align: center;
}

.percent-value {
    font-size: 4.5rem;
    font-weight: 900;
    background: linear-gradient(135deg, #667eea, #764ba2);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    position: relative;
    display: inline-block;
    margin-bottom: 0.5rem;
}

.percent-value::after {
    content: '%';
    font-size: 2rem;
    font-weight: 600;
    color: #9ca3af;
    margin-left: 0.5rem;
}

/* Animated Ring Progress */
.progress-ring {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 200px;
    height: 200px;
}

.progress-ring svg {
    transform: rotate(-90deg);
}

.progress-ring-bg {
    fill: none;
    stroke: #f3f4f6;
    stroke-width: 12;
}

.progress-ring-fill {
    fill: none;
    stroke-width: 12;
    stroke-linecap: round;
    transition: stroke-dashoffset 1.5s cubic-bezier(0.4, 0, 0.2, 1);
    stroke-dasharray: 565;
    stroke-dashoffset: 565;
    animation: progressAnimation 1.5s ease-out forwards;
}

@keyframes progressAnimation {
    from { stroke-dashoffset: 565; }
}

/* Risk Category Cards */
.risk-card {
    background: linear-gradient(145deg, #ffffff, #f8fafc);
    padding: 2rem;
    border-radius: 24px;
    margin: 1.5rem 0;
    border-left: 6px solid;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}

.risk-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.4), transparent);
    transform: translateX(-100%);
}

.risk-card:hover::before {
    animation: shimmer 1.5s ease;
}

@keyframes shimmer {
    100% { transform: translateX(100%); }
}

.risk-card.low {
    border-left-color: #10b981;
    box-shadow: 0 10px 40px rgba(16, 185, 129, 0.15);
}

.risk-card.borderline {
    border-left-color: #f59e0b;
    box-shadow: 0 10px 40px rgba(245, 158, 11, 0.15);
}

.risk-card.elevated {
    border-left-color: #ef4444;
    box-shadow: 0 10px 40px rgba(239, 68, 68, 0.15);
}

.risk-card:hover {
    transform: translateX(8px);
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.12);
}

.risk-category {
    font-size: 1.5rem;
    font-weight: 700;
    color: #1f2937;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin-left: -50px;
}

.risk-icon {
    width: 36px;
    height: 36px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 600;
    font-size: 1.2rem;
    color: white;
}

.low .risk-icon {
    background: linear-gradient(135deg, #10b981, #34d399);
}

.borderline .risk-icon {
    background: linear-gradient(135deg, #f59e0b, #fbbf24);
}

.elevated .risk-icon {
    background: linear-gradient(135deg, #ef4444, #f87171);
}

/* Beautiful Scale/Progress Bar */
.scale-container {
    margin: 2rem 0;
    padding: 0 1rem;
}

.scale-labels {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.75rem;
    font-size: 0.9rem;
    font-weight: 600;
}

.scale-low { color: #10b981; }
.scale-borderline { color: #f59e0b; }
.scale-elevated { color: #ef4444; }

.scale-bar {
    height: 16px;
    background: linear-gradient(90deg, 
        #10b981 0%, 
        #10b981 30%, 
        #f59e0b 30%, 
        #f59e0b 60%, 
        #ef4444 60%, 
        #ef4444 100%);
    border-radius: 10px;
    position: relative;
    overflow: hidden;
}

.scale-marker {
    position: absolute;
    top: 50%;
    transform: translate(-50%, -50%);
    width: 28px;
    height: 28px;
    background: white;
    border: 3px solid #667eea;
    border-radius: 50%;
    box-shadow: 
        0 0 0 4px rgba(255, 255, 255, 0.9),
        0 4px 20px rgba(102, 126, 234, 0.4);
    z-index: 10;
    transition: left 1.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.scale-marker::after {
    content: '';
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 8px;
    height: 8px;
    background: #667eea;
    border-radius: 50%;
}

/* List Items */
.driver-list {
    list-style-type: none;
    padding-left: 0;
}

.driver-list li {
    padding: 0.5rem 0;
    padding-left: 1.8rem;
    position: relative;
    color: #4b5563;
    line-height: 1.6;
}

.driver-list li::before {
    content: "•";
    position: absolute;
    left: 0;
    color: #667eea;
    font-size: 1.5rem;
    line-height: 1;
}

/* Modern Button */
/* РЕШЕНИЕ: Принудительное центрирование кнопки */
.css-1x8cf1d, .css-1x8cf1d.edgvbvh3, div[data-testid="stButton"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    text-align: center !important;
}

div[data-testid="stButton"] {
    display: flex !important;
    justify-content: center !important;
    width: 100% !important;
    margin: 2rem 0 !important;
}

div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    padding: 0.85rem 2rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    border-radius: 16px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    width: auto !important;
    min-width: 240px !important;
    max-width: 100% !important;
    margin: 0 auto !important;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1) !important;
    position: relative !important;
    left: 50% !important;
    transform: translateX(-50%) !important;
}

div[data-testid="stButton"] > button:hover {
    transform: translateX(-50%) translateY(-2px) !important;
    box-shadow: 0 12px 25px rgba(102, 126, 234, 0.3) !important;
}

/* Медиа-запросы */
@media screen and (max-width: 768px) {
    div[data-testid="stButton"] > button {
        width: 90% !important;
        max-width: 90% !important;
        padding: 0.85rem 1rem !important;
    }
}

@media screen and (max-width: 480px) {
    div[data-testid="stButton"] > button {
        width: 100% !important;
        max-width: 100% !important;
        font-size: 0.9rem !important;
        padding: 0.75rem 1rem !important;
    }
}
            
/* Footer */
.footer {
    font-size: 0.85rem;
    color: #6b7280;
    margin-top: 2rem;
    padding: 1.5rem;
    background: rgba(249, 250, 251, 0.8);
    border-radius: 12px;
    text-align: center;
    border: 1px solid rgba(229, 231, 235, 0.5);
}

/* Glass Effect */
.glass {
    background: rgba(255, 255, 255, 0.7);
    backdrop-filter: blur(20px);
    -webkit-backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
}

/* Results Container */
.results-container {
    background: linear-gradient(145deg, #ffffff, #fcfdff);
    padding: 2.5rem;
    border-radius: 24px;
    margin-top: 2rem;
    border: 1px solid rgba(229, 231, 235, 0.8);
    box-shadow: 
        0 20px 40px rgba(0, 0, 0, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.6);
        
}
            
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD REAL MODEL (SSOT)
# ======================================================
MODELS_DIR = Path("models")
MODEL_PATH = MODELS_DIR / "emra_pipeline.joblib"
META_PATH  = MODELS_DIR / "emra_metadata.json"

@st.cache_resource
def load_model():
    return joblib.load(MODEL_PATH)

@st.cache_resource
def load_metadata():
    with open(META_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

model = load_model()
metadata = load_metadata()


# ======================================================
# LOAD REFERENCE DISTRIBUTION (SSOT)
# ======================================================
REFERENCE_PATH = MODELS_DIR / "reference_scores.npy"

@st.cache_resource
def load_reference_scores():
    return np.load(REFERENCE_PATH)

REFERENCE_SCORES = load_reference_scores()

# ======================================================
# CALIBRATION LAYER
# ======================================================

def score_to_percentile(score, reference_scores=REFERENCE_SCORES):
    pct = np.searchsorted(reference_scores, score, side="right") / len(reference_scores)
    pct = pct * 100
    pct = np.clip(pct, 20, 90)
    return int(round(pct))

# ======================================================
# INTERPRETATION LAYER (ВАШ ОРИГИНАЛЬНЫЙ ТЕКСТ)
# ======================================================
def percentile_to_demo_output(percentile: int) -> dict:

    if percentile < 30:
        return {
            "category": "Low Apparent Metabolic Risk",
            "card_class": "low",
            "icon": "✓",
            "interpretation": (
                "No meaningful combined metabolic risk pattern is detected "
                "based on population-level data."
            ),
            "drivers": [
                "All biomarkers fall well within typical reference ranges",
                "No clustering of borderline metabolic values",
                "Profile aligns with low-risk population patterns"
            ],
            "why_this_matters": (
                "In population-level data, profiles similar to this one are "
                "predominantly observed among individuals who maintain stable "
                "metabolic patterns over time."
            )
        }

    elif percentile < 45:
        return {
            "category": "Low Apparent Risk (with borderline signals)",
            "card_class": "low",
            "icon": "↗",
            "interpretation": (
                "Some biomarkers approach upper-normal ranges, but the overall "
                "pattern remains close to population norms."
            ),
            "drivers": [
                "Isolated borderline biomarker elevation",
                "Other markers remain within expected ranges",
                "No strong interaction between multiple metabolic signals"
            ],
            "why_this_matters": (
                "Population-level analysis shows that profiles like this occupy "
                "a transitional zone, where early metabolic shifts may be present "
                "without triggering clinical thresholds."
            )
        }

    elif percentile < 60:
        return {
            "category": "Borderline Metabolic Pattern Detected",
            "card_class": "borderline",
            "icon": "⚠",
            "interpretation": (
                "Mixed metabolic signals are observed, placing this profile "
                "above the population median."
            ),
            "drivers": [
                "Multiple biomarkers approach upper-normal ranges",
                "Subtle clustering across metabolic dimensions",
                "Overall pattern differs from the population center"
            ],
            "why_this_matters": (
                "In population-level cohorts, similar profiles are more frequently "
                "observed among individuals who later meet criteria for metabolic "
                "conditions, compared to lower-percentile groups."
            )
        }

    else:
        return {
            "category": "Elevated Early Metabolic Risk",
            "card_class": "elevated",
            "icon": "↑↑",
            "interpretation": (
                "The combined biomarker pattern shows a pronounced deviation "
                "from typical population profiles, despite individual values "
                "remaining near reference ranges."
            ),
            "drivers": [
                "Combined elevation of lipid and anthropometric markers",
                "Consistent upward shift across multiple biomarkers",
                "Pattern differs from the majority of the reference population"
            ],
            "why_this_matters": (
                "Population-level data indicate that profiles in this range are "
                "disproportionately represented among individuals who eventually "
                "exhibit clinically significant metabolic deterioration."
            )
        }


st.markdown('<div class="main-title">Early Metabolic Risk Assessment</div>', unsafe_allow_html=True)

st.markdown("""
<div class="caption-box glass">
Research demonstration.<br>
This tool visualizes population-level metabolic risk patterns
and is not intended for diagnosis or clinical decision-making.
</div>
""", unsafe_allow_html=True)

# ======================================================
# USER INPUTS 
# ======================================================
st.subheader("Enter biomarker values")

col1, col2 = st.columns(2)
with col1:
    glucose = st.number_input("Fasting glucose (mg/dL)", 50.0, 200.0, 90.0)
    hba1c   = st.number_input("HbA1c (%)", 4.0, 10.0, 5.4)
with col2:
    tg      = st.number_input("Triglycerides (mg/dL)", 50.0, 400.0, 120.0)
    bmi     = st.number_input("Body Mass Index (BMI)", 15.0, 45.0, 24.0)

# ======================================================
# RUN ANALYSIS
# ======================================================

if st.button("Assess metabolic pattern"):
    
    with st.spinner('Analyzing metabolic patterns...'):
        time.sleep(1)
        
        user_df = pd.DataFrame([{
            "LBXGLU": glucose,
            "LBXGH": hba1c,
            "LBXTR": tg,
            "BMXBMI": bmi
        }])

        raw_score = model.predict_proba(user_df)[0, 1]
        percentile = score_to_percentile(raw_score)
        demo = percentile_to_demo_output(percentile)
        
        
        # Animated Percentage Display
        if demo['card_class'] == 'low':
            ring_color = '#10b981'
        elif demo['card_class'] == 'borderline':
            ring_color = '#f59e0b'
        else:
            ring_color = '#ef4444'
        
        dashoffset = 565 - (percentile / 100 * 565)
        
        st.markdown(f'''
        <div class="percent-container">
            <div class="percent-value">{percentile}</div>
            <div class="progress-ring">
                <svg width="200" height="200">
                    <circle class="progress-ring-bg" cx="100" cy="100" r="90"></circle>
                    <circle class="progress-ring-fill" cx="100" cy="100" r="90" 
                            style="stroke: {ring_color}; stroke-dashoffset: {dashoffset}"></circle>
                </svg>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Beautiful Scale Bar
        st.markdown(f'''
        <div class="scale-container">
            <div class="scale-bar">
                <div class="scale-marker" style="left: {percentile}%;"></div>
            </div>
            <div class="scale-labels">
                <span class="scale-low">Low Risk</span>
                <span class="scale-borderline">Borderline</span>
                <span class="scale-elevated">Elevated Risk</span>
            </div>
        </div>
        ''', unsafe_allow_html=True)
        
       
        st.markdown(f'''
        <div class="risk-category">
            <span class="risk-icon">{demo["icon"]}</span>
            {demo["category"]}
        </div>
        ''', unsafe_allow_html=True)
        
       
        st.markdown(f'<p style="color: #4b5563; margin-bottom: 1.5rem; font-size: 1.1rem;">{demo["interpretation"]}</p>', unsafe_allow_html=True)
        
        # What drives this result
        st.markdown('''
        <div>
            <strong style="color: #1f2937; font-size: 1rem; display: block; margin-bottom: 1rem;">
                What drives this result:
            </strong>
            <ul class="driver-list">
        ''', unsafe_allow_html=True)
        
  
        for driver in demo['drivers']:
            st.markdown(f'<li>{driver}</li>', unsafe_allow_html=True)
        
        st.markdown('''
            </ul>
        </div>
        ''', unsafe_allow_html=True)
        
        
        st.markdown('''
        <div style="margin-top: 1.5rem;">
            <strong style="color: #1f2937; font-size: 1rem; display: block; margin-bottom: 0.75rem;">
                Why this signal matters:
            </strong>
            <p style="color: #4b5563; margin: 0; line-height: 1.6;">
        ''', unsafe_allow_html=True)
        
        st.markdown(f'{demo["why_this_matters"]}', unsafe_allow_html=False)
        
        st.markdown('''
            </p>
        </div>
        ''', unsafe_allow_html=True)
        
        
        st.markdown('</div>', unsafe_allow_html=True)
        
      
        st.markdown('''
        <div class="footer glass">
            Percentiles are computed relative to a fixed reference population used during model validation. 
            This output reflects population-level statistical patterns and is intended for research and 
            exploratory purposes only. It does not represent an individual diagnosis or prediction.
        </div>
        ''', unsafe_allow_html=True)
        
       
        st.markdown('</div>', unsafe_allow_html=True)


else:
    st.markdown('''
    <div style="text-align: center; padding: 3rem 2rem; color: #9ca3af; font-size: 1rem;">
        <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">⟳</div>
        <div style="font-weight: 500; margin-bottom: 0.5rem;">Ready for analysis</div>
        <div>Enter biomarker values and click "Assess metabolic pattern" to begin</div>
    </div>
    ''', unsafe_allow_html=True)

    