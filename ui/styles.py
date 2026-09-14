"""
Cyber-dark gamer styling and custom CSS components for EditorGIF.
"""

CUSTOM_CSS = """
<style>
/* Global Dark Cyber Theme */
.stApp {
    background: radial-gradient(circle at 10% 20%, #0f1016 0%, #08080d 90%);
    color: #e2e8f0;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Header Styling */
.hero-title {
    font-size: 2.3rem;
    font-weight: 800;
    background: linear-gradient(135deg, #a855f7 0%, #06b6d4 50%, #10b981 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 0.2rem;
    letter-spacing: -0.5px;
}
.hero-subtitle {
    font-size: 1rem;
    color: #94a3b8;
    margin-bottom: 1.5rem;
}

/* Card Container */
.glass-card {
    background: rgba(22, 23, 34, 0.7);
    border: 1px solid rgba(255, 255, 255, 0.08);
    backdrop-filter: blur(12px);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
}

/* Transparency Checkerboard Box */
.checkerboard-box {
    background-color: #12131c;
    background-image:
        linear-gradient(45deg, #1e202f 25%, transparent 25%),
        linear-gradient(-45deg, #1e202f 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #1e202f 75%),
        linear-gradient(-45deg, transparent 75%, #1e202f 75%);
    background-size: 24px 24px;
    background-position: 0 0, 0 12px, 12px -12px, -12px 0px;
    border: 2px dashed rgba(168, 85, 247, 0.4);
    border-radius: 14px;
    padding: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 280px;
    margin-top: 10px;
    margin-bottom: 20px;
}

/* Status Badges */
.badge-tech {
    display: inline-block;
    padding: 3px 10px;
    font-size: 0.75rem;
    font-weight: 600;
    border-radius: 9999px;
    background: rgba(168, 85, 247, 0.15);
    color: #c084fc;
    border: 1px solid rgba(168, 85, 247, 0.3);
    margin-right: 6px;
}

/* Buttons Polish */
.stButton > button {
    background: linear-gradient(135deg, #7c3aed 0%, #4f46e5 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 14px 0 rgba(124, 58, 237, 0.4) !important;
    transition: all 0.2s ease-in-out !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px 0 rgba(124, 58, 237, 0.6) !important;
}

/* Download Buttons Polish */
.stDownloadButton > button {
    background: linear-gradient(135deg, #059669 0%, #0d9488 100%) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 24px !important;
    box-shadow: 0 4px 14px 0 rgba(5, 150, 105, 0.4) !important;
    transition: all 0.2s ease-in-out !important;
}
.stDownloadButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px 0 rgba(5, 150, 105, 0.6) !important;
}
</style>
"""
