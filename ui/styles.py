"""
UI/UX Pro Max - Advanced Cyber-Dark Gaming Design System for EditorGIF.
Tailored for game developers, animators, and digital artists.
High contrast, OLED deep dark palette, modern typography, and glassmorphism.
"""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Outfit:wght@400;500;600;700;800;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

/* ==========================================================================
   Global Theme & Atmospheric Background
   ========================================================================== */
html, body, [class*="css"], .stApp {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: #e2e8f0;
}

.stApp {
    background: 
        radial-gradient(ellipse 60% 40% at 15% 10%, rgba(99, 102, 241, 0.14) 0%, transparent 70%),
        radial-gradient(ellipse 50% 30% at 85% 85%, rgba(6, 182, 212, 0.10) 0%, transparent 70%),
        radial-gradient(circle at 50% 50%, rgba(139, 92, 246, 0.04) 0%, transparent 100%),
        #090a10 !important;
    background-attachment: fixed !important;
}

/* Hide default streamlit decoration */
header[data-testid="stHeader"] {
    background: rgba(9, 10, 16, 0.7) !important;
    backdrop-filter: blur(14px) !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
}

/* ==========================================================================
   Typography Hierarchy
   ========================================================================== */
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif !important;
    letter-spacing: -0.02em !important;
    font-weight: 700 !important;
}

/* ==========================================================================
   Hero Header Section
   ========================================================================== */
.hero-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    flex-wrap: wrap;
    gap: 16px;
    padding: 6px 0 22px 0;
    margin-bottom: 12px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.07);
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 4px 12px;
    border-radius: 9999px;
    background: rgba(99, 102, 241, 0.14);
    border: 1px solid rgba(99, 102, 241, 0.35);
    color: #a5b4fc;
    font-size: 0.75rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
    margin-bottom: 8px;
}

.hero-badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #6366f1;
    box-shadow: 0 0 8px #6366f1;
    animation: pulse-dot 2s infinite ease-in-out;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.35; transform: scale(0.85); }
}

.hero-title {
    font-size: 2.6rem;
    font-weight: 800;
    background: linear-gradient(135deg, #ffffff 0%, #cbd5e1 35%, #a855f7 70%, #06b6d4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.25rem;
    letter-spacing: -0.03em;
    line-height: 1.15;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #94a3b8;
    max-width: 680px;
    line-height: 1.5;
}

.hero-badges-wrapper {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    align-items: center;
}

.badge-tech {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 6px 12px;
    font-size: 0.78rem;
    font-weight: 600;
    border-radius: 8px;
    background: rgba(18, 22, 36, 0.85);
    color: #cbd5e1;
    border: 1px solid rgba(255, 255, 255, 0.08);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
    transition: all 0.2s ease;
}

.badge-tech:hover {
    border-color: rgba(99, 102, 241, 0.45);
    background: rgba(26, 32, 52, 0.95);
    transform: translateY(-1px);
}

.badge-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
}
.dot-cyan { background: #06b6d4; box-shadow: 0 0 6px #06b6d4; }
.dot-purple { background: #a855f7; box-shadow: 0 0 6px #a855f7; }
.dot-emerald { background: #10b981; box-shadow: 0 0 6px #10b981; }

/* ==========================================================================
   Cards & Glass Containers
   ========================================================================== */
.glass-card {
    background: linear-gradient(180deg, rgba(20, 24, 38, 0.75) 0%, rgba(13, 16, 27, 0.85) 100%) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    backdrop-filter: blur(20px) !important;
    border-radius: 18px !important;
    padding: 24px !important;
    margin-bottom: 20px !important;
    box-shadow: 0 12px 36px 0 rgba(0, 0, 0, 0.4), inset 0 1px 0 0 rgba(255, 255, 255, 0.08) !important;
    transition: border-color 0.25s ease, box-shadow 0.25s ease;
}

.glass-card:hover {
    border-color: rgba(99, 102, 241, 0.25) !important;
    box-shadow: 0 14px 40px 0 rgba(0, 0, 0, 0.45), inset 0 1px 0 0 rgba(255, 255, 255, 0.12) !important;
}

/* Card Section Headers */
.glass-card h3, .glass-card [data-testid="stSubheader"] {
    font-size: 1.25rem !important;
    font-weight: 700 !important;
    color: #f1f5f9 !important;
    margin-bottom: 1rem !important;
    display: flex;
    align-items: center;
    gap: 8px;
}

/* ==========================================================================
   HUD Stats Grid
   ========================================================================== */
.stats-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: 10px;
    margin-bottom: 16px;
}

.stat-card {
    background: rgba(14, 17, 28, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-top: 2px solid #6366f1;
    border-radius: 10px;
    padding: 10px 14px;
    transition: all 0.2s ease;
}

.stat-card:hover {
    border-color: rgba(99, 102, 241, 0.4);
    background: rgba(20, 25, 40, 0.85);
    transform: translateY(-1px);
}

.stat-label {
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    margin-bottom: 2px;
}

.stat-value {
    color: #f8fafc;
    font-size: 1rem;
    font-weight: 700;
    font-family: 'JetBrains Mono', monospace;
}

.stat-sub {
    font-size: 0.8rem;
    color: #818cf8;
    font-weight: 500;
}

/* ==========================================================================
   Checkerboard Viewport (Cyber Canvas Frame)
   ========================================================================== */
.checkerboard-viewport {
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 14px;
    overflow: hidden;
    background: #0d101a;
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
    margin: 12px 0 20px 0;
}

.viewport-header {
    background: rgba(18, 22, 34, 0.95);
    padding: 8px 14px;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.viewport-dots {
    display: flex;
    gap: 6px;
    align-items: center;
}

.v-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
}
.v-red { background: #ef4444; }
.v-yellow { background: #f59e0b; }
.v-green { background: #10b981; }

.viewport-title {
    font-size: 0.7rem;
    font-weight: 700;
    color: #94a3b8;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.06em;
}

.viewport-status {
    font-size: 0.65rem;
    font-weight: 700;
    color: #10b981;
    background: rgba(16, 185, 129, 0.15);
    padding: 2px 8px;
    border-radius: 4px;
    font-family: 'JetBrains Mono', monospace;
}

.checkerboard-box {
    background-color: #0d0f18;
    background-image:
        linear-gradient(45deg, #181c2c 25%, transparent 25%),
        linear-gradient(-45deg, #181c2c 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #181c2c 75%),
        linear-gradient(-45deg, transparent 75%, #181c2c 75%);
    background-size: 20px 20px;
    background-position: 0 0, 0 10px, 10px -10px, -10px 0px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 280px;
}

.checkerboard-box img {
    border-radius: 8px;
    filter: drop-shadow(0 8px 16px rgba(0, 0, 0, 0.6));
    transition: transform 0.2s ease;
}

.checkerboard-box img:hover {
    transform: scale(1.02);
}

.empty-box {
    color: #64748b;
    text-align: center;
}

.empty-icon {
    font-size: 2.8rem;
    margin-bottom: 8px;
    filter: drop-shadow(0 0 12px rgba(99, 102, 241, 0.3));
}

.empty-text {
    font-size: 0.95rem;
    max-width: 320px;
    line-height: 1.4;
    color: #94a3b8;
}

/* ==========================================================================
   Streamlit Native Component Reskinning
   ========================================================================== */

/* File Uploader Dropzone */
[data-testid="stFileUploader"] section {
    background: rgba(15, 18, 29, 0.6) !important;
    border: 2px dashed rgba(99, 102, 241, 0.3) !important;
    border-radius: 14px !important;
    padding: 20px !important;
    transition: all 0.25s ease !important;
}

[data-testid="stFileUploader"] section:hover {
    border-color: #6366f1 !important;
    background: rgba(20, 25, 42, 0.8) !important;
    box-shadow: 0 0 18px rgba(99, 102, 241, 0.2) !important;
}

[data-testid="stFileUploader"] button {
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* Process Action Button */
.stButton > button {
    background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 50%, #d946ef 100%) !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    box-shadow: 0 4px 20px 0 rgba(99, 102, 241, 0.45) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px 0 rgba(99, 102, 241, 0.65) !important;
    filter: brightness(1.08) !important;
}

.stButton > button:active {
    transform: scale(0.98) !important;
}

/* Download Buttons */
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669 0%, #10b981 50%, #14b8a6 100%) !important;
    color: #ffffff !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 11px 22px !important;
    box-shadow: 0 4px 18px 0 rgba(16, 185, 129, 0.35) !important;
    transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    cursor: pointer !important;
    margin-bottom: 8px !important;
}

.stDownloadButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 25px 0 rgba(16, 185, 129, 0.55) !important;
    filter: brightness(1.08) !important;
}

.stDownloadButton > button:active {
    transform: scale(0.98) !important;
}

/* Streamlit Tabs */
button[data-baseweb="tab"] {
    background: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.06) !important;
    border-radius: 8px !important;
    padding: 8px 18px !important;
    font-family: 'Outfit', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
    margin-right: 8px !important;
    transition: all 0.2s ease !important;
}

button[data-baseweb="tab"]:hover {
    color: #f1f5f9 !important;
    border-color: rgba(99, 102, 241, 0.4) !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    background: rgba(99, 102, 241, 0.18) !important;
    border-color: #6366f1 !important;
    color: #ffffff !important;
    box-shadow: 0 2px 10px rgba(99, 102, 241, 0.25) !important;
}

div[data-baseweb="tab-highlight"] {
    display: none !important;
}

/* Streamlit Sliders */
.stSlider {
    padding-top: 8px !important;
    padding-bottom: 8px !important;
}

.stSlider [data-baseweb="slider"] div[role="slider"] {
    background: #6366f1 !important;
    border: 2px solid #ffffff !important;
    box-shadow: 0 0 10px rgba(99, 102, 241, 0.8) !important;
    width: 18px !important;
    height: 18px !important;
}

/* Expander */
[data-testid="stExpander"] {
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    background: rgba(14, 18, 29, 0.6) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
    margin-top: 12px !important;
}

[data-testid="stExpander"] summary {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    color: #e2e8f0 !important;
    padding: 12px 16px !important;
}

[data-testid="stExpander"] summary:hover {
    color: #6366f1 !important;
}

/* Alerts / Info Boxes */
.stAlert {
    background: rgba(18, 24, 38, 0.85) !important;
    border: 1px solid rgba(99, 102, 241, 0.25) !important;
    border-left: 4px solid #6366f1 !important;
    border-radius: 10px !important;
    color: #e2e8f0 !important;
}

/* Sidebar Customization */
[data-testid="stSidebar"] {
    background: #0a0c13 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.06) !important;
}

/* Scrollbar Polish */
::-webkit-scrollbar {
    width: 7px;
    height: 7px;
}
::-webkit-scrollbar-track {
    background: #090a10;
}
::-webkit-scrollbar-thumb {
    background: #1e2438;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #6366f1;
}
</style>
"""

