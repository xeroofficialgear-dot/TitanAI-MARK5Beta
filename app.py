import streamlit as st
import time
import re
import io
import os
import zipfile
from groq import Groq

# =====================================================================
# ⚙️ TITANAI STUDIO CONFIGURATION (Official Links & Branding)
# =====================================================================
TEAM_NAME = "TitanAI studio"
DISCORD_URL = "https://discord.com/invite/pXfXFWbu3T"
YOUTUBE_URL = "https://youtube.com/@titanaioffcial?si=lW9nsnLVebbwVSvD"
TIKTOK_URL = "https://www.tiktok.com/@titanaiofficial?is_from_webapp=1&sender_device=pc"
# =====================================================================

# Set up page layout with wide orientation
st.set_page_config(
    page_title=f"Titan // {TEAM_NAME}", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# =====================================================================
# 🎨 HIGH-FIDELITY VECTOR SVG GRAPHICS
# =====================================================================
SVG_BOLT_LOGO = """
<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 8px;">
    <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" fill="url(#bolt_grad)" stroke="#111" stroke-width="1" stroke-linejoin="round"/>
    <defs>
        <linearGradient id="bolt_grad" x1="0%" y1="0%" x2="100%" y2="100%">
            <stop offset="0%" stop-color="#FFD000" />
            <stop offset="100%" stop-color="#FF6A00" />
        </linearGradient>
    </defs>
</svg>
"""

SVG_WORKSPACE_ICON = """
<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 8px;">
    <rect x="2" y="3" width="20" height="14" rx="2" stroke="currentColor" stroke-width="2" fill="rgba(255, 208, 0, 0.05)"/>
    <path d="M6 21H18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M12 17V21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M7 8L10 10L7 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M12 12H16" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

SVG_INTEGRATION_ICON = """
<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 8px;">
    <path d="M10 19V15H14V19M19 12H21M12 3V5M3 12H5M19 8L21 6M5 8L3 6M19 16L21 18M5 16L3 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
    <rect x="6" y="8" width="12" height="12" rx="2" stroke="currentColor" stroke-width="2" fill="rgba(0, 255, 204, 0.05)"/>
</svg>
"""

SVG_NEWS_ICON = """
<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 8px;">
    <path d="M19 3H5C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
    <path d="M7 7H17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M7 11H17" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M7 15H13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

SVG_ADMIN_ICON = """
<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 8px;">
    <circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="2" fill="rgba(255, 208, 0, 0.05)"/>
    <circle cx="12" cy="12" r="3" stroke="currentColor" stroke-width="2"/>
    <path d="M12 5V9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M12 15V19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M5 12H9" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M15 12H19" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
</svg>
"""

SVG_SUPPORT_ICON = """
<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 8px;">
    <path d="M21 11.5C21 16.75 16.75 21 11.5 21C9.37 21 7.42 20.3 5.85 19.12L3 20L3.88 17.15C2.7 15.58 2 13.63 2 11.5C2 6.25 6.25 2 11.5 2C16.75 2 21 6.25 21 11.5Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round" fill="rgba(255, 208, 0, 0.05)"/>
    <circle cx="8" cy="11.5" r="1.5" fill="currentColor"/>
    <circle cx="11.5" cy="11.5" r="1.5" fill="currentColor"/>
    <circle cx="15" cy="11.5" r="1.5" fill="currentColor"/>
</svg>
"""

SVG_LEGAL_ICON = """
<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; margin-right: 8px;">
    <path d="M12 3V21" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M19 13C19 16.87 15.87 20 12 20C8.13 20 5 16.87 5 13" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M4 7H20" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
    <path d="M6 7L9 14H3L6 7Z" fill="rgba(255, 208, 0, 0.1)" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
    <path d="M18 7L21 14H15L18 7Z" fill="rgba(255, 208, 0, 0.1)" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/>
</svg>
"""

# =====================================================================
# 🎨 BRAND DESIGN THEMES (System State Cache & Styles Configuration)
# =====================================================================
if "active_theme" not in st.session_state:
    st.session_state.active_theme = "Premium Gold"

THEME_STYLES = {
    "Premium Gold": {
        "sidebar_grad": "linear-gradient(180deg, #FFD100 0%, #FF6200 100%)",
        "app_bg": "#0b0b0c",
        "sidebar_text": "#111111",
        "primary_btn_grad": "linear-gradient(135deg, #FFD100 0%, #FF6200 100%)",
        "primary_btn_text": "#0b0b0c",
        "accent_glow": "rgba(255, 98, 0, 0.25)",
        "accent_glow_hover": "rgba(255, 98, 0, 0.45)"
    },
    "Vaporwave Neon": {
        "sidebar_grad": "linear-gradient(180deg, #FF007F 0%, #00F0FF 100%)",
        "app_bg": "#120136",
        "sidebar_text": "#ffffff",
        "primary_btn_grad": "linear-gradient(135deg, #FF007F 0%, #00F0FF 100%)",
        "primary_btn_text": "#120136",
        "accent_glow": "rgba(0, 240, 255, 0.3)",
        "accent_glow_hover": "rgba(255, 0, 127, 0.6)"
    },
    "8-Bit Arcade": {
        "sidebar_grad": "linear-gradient(180deg, #00FF66 0%, #000000 100%)",
        "app_bg": "#000000",
        "sidebar_text": "#00FF66",
        "primary_btn_grad": "linear-gradient(135deg, #00FF66 0%, #009933 100%)",
        "primary_btn_text": "#000000",
        "accent_glow": "rgba(0, 255, 102, 0.25)",
        "accent_glow_hover": "rgba(0, 255, 102, 0.5)"
    },
    "Cyberpunk Core": {
        "sidebar_grad": "linear-gradient(180deg, #FFE600 0%, #1a1a1d 100%)",
        "app_bg": "#1a1a1d",
        "sidebar_text": "#00ffcc",
        "primary_btn_grad": "linear-gradient(135deg, #00ffcc 0%, #ff0055 100%)",
        "primary_btn_text": "#ffffff",
        "accent_glow": "rgba(0, 255, 204, 0.3)",
        "accent_glow_hover": "rgba(255, 0, 85, 0.5)"
    },
    "Steampunk Brass": {
        "sidebar_grad": "linear-gradient(180deg, #B5651D 0%, #3D2314 100%)",
        "app_bg": "#1f140e",
        "sidebar_text": "#f5deb3",
        "primary_btn_grad": "linear-gradient(135deg, #e5a93b 0%, #8b5a2b 100%)",
        "primary_btn_text": "#1f140e",
        "accent_glow": "rgba(229, 169, 59, 0.2)",
        "accent_glow_hover": "rgba(229, 169, 59, 0.45)"
    }
}

current_theme = THEME_STYLES[st.session_state.active_theme]
st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {current_theme["app_bg"]} !important;
        color: #f3f4f6 !important;
    }}
    [data-testid="stSidebar"] {{
        background: {current_theme["sidebar_grad"]} !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05) !important;
    }}
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3, 
    [data-testid="stSidebar"] h4, 
    [data-testid="stSidebar"] p, 
    [data-testid="stSidebar"] span, 
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] small {{
        color: {current_theme["sidebar_text"]} !important;
        font-weight: 600 !important;
    }}
    [data-testid="stSidebar"] .stSlider label {{
        color: {current_theme["sidebar_text"]} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stSidebar"] .stSelectbox label {{
        color: {current_theme["sidebar_text"]} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stSidebar"] .stTextArea label {{
        color: {current_theme["sidebar_text"]} !important;
        font-weight: 700 !important;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"] label {{
        background-color: rgba(255, 255, 255, 0.12) !important;
        border-radius: 8px !important;
        padding: 8px 12px !important;
        margin-bottom: 6px !important;
        border: 1px solid rgba(0, 0, 0, 0.08) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background-color: rgba(255, 255, 255, 0.28) !important;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
        transform: translateX(3px) !important;
    }}
    [data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {{
        background-color: #ffffff !important;
        color: #111111 !important;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
        border: 1px solid rgba(0, 0, 0, 0.2) !important;
    }}
    
    /* Code Editor, Input Fields, and Workspace styling */
    div[data-testid="stTextInput"] input, 
    div[data-testid="stTextArea"] textarea {{
        background-color: rgba(20, 20, 22, 0.8) !important;
        color: #f3f4f6 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
        padding: 12px !important;
    }}

    /* FIXED VISUAL CONTRAST FOR SYSTEM INSTRUCTIONS TEXT AREA IN SIDEBAR */
    [data-testid="stSidebar"] div[data-testid="stTextArea"] textarea {{
        background-color: #121214 !important;
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.85em !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 8px !important;
    }}
    [data-testid="stSidebar"] div[data-testid="stTextArea"] textarea:focus {{
        border-color: #00ffcc !important;
        box-shadow: 0 0 10px rgba(0, 255, 204, 0.2) !important;
    }}
    
    button[kind="primary"] {{
        background: {current_theme["primary_btn_grad"]} !important;
        color: {current_theme["primary_btn_text"]} !important;
        font-weight: 700 !important;
        border: none !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px {current_theme["accent_glow"]} !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}
    button[kind="primary"]:hover {{
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 22px {current_theme["accent_glow_hover"]} !important;
    }}
    [data-testid="stSidebar"] button[kind="secondary"] {{
        background-color: rgba(0, 0, 0, 0.2) !important;
        color: {current_theme["sidebar_text"]} !important;
        border: 1px solid rgba(0, 0, 0, 0.3) !important;
        font-weight: 700 !important;
    }}
    [data-testid="stSidebar"] button[kind="secondary"]:hover {{
        background-color: rgba(0, 0, 0, 0.4) !important;
        color: #ffffff !important;
    }}
    [data-testid="stSidebar"] .stSlider [data-baseweb="slider"] {{
        background-color: rgba(0, 0, 0, 0.15) !important;
    }}
    [data-testid="stSidebar"] .stSlider [data-testid="stTickBar"] {{
        color: {current_theme["sidebar_text"]} !important;
    }}
    [data-testid="stSidebar"] .stSlider div[role="slider"] {{
        background-color: #111111 !important;
        border: 2px solid #ffffff !important;
    }}
    </style>
    """, 
    unsafe_allow_html=True
)

# =====================================================================
# ⚙️ DEFINE HELPER FUNCTIONS AT THE TOP TO GUARANTEE COMPILATION
# =====================================================================
def render_logo(width=100, align="center"):
    """Renders either the brand titanlogo.png image or the vector SVG bolt."""
    if os.path.exists("titanlogo.png"):
        if align == "center":
            _, logo_col, _ = st.columns([1, 2, 1])
            with logo_col:
                st.image("titanlogo.png", width=width)
        else:
            st.image("titanlogo.png", width=width)
    else:
        if align == "center":
            st.markdown(f"<div style='text-align: center; margin-bottom: 15px;'>{SVG_BOLT_LOGO}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='display: inline-block; vertical-align: middle; margin-right: 5px;'>{SVG_BOLT_LOGO}</div>", unsafe_allow_html=True)

def render_footer():
    """Renders a elegant centered brand footer at the page base."""
    st.write("##")
    st.write("---")
    _, center_col, _ = st.columns([1.5, 1, 1.5])
    with center_col:
        if os.path.exists("titanlogo.png"):
            st.image("titanlogo.png", width=60)
        else:
            st.markdown(f"<div style='text-align: center; margin-bottom: 8px;'>{SVG_BOLT_LOGO}</div>", unsafe_allow_html=True)
        st.markdown(
            f"<p style='text-align: center; font-size: 0.8em; opacity: 0.5; margin-top: 5px; color: #f3f4f6;'>Powered by <b>{TEAM_NAME}</b><br>© 2026. All rights reserved.</p>",
            unsafe_allow_html=True
        )

def unlock_achievement(achievement_id, name):
    """Safely adds an unlocked badge to local session trophy room."""
    if "unlocked_achievements" not in st.session_state:
        st.session_state.unlocked_achievements = []
    if achievement_id not in st.session_state.unlocked_achievements:
        st.session_state.unlocked_achievements.append(achievement_id)
        st.toast(f"🏆 Achievement Unlocked: {name}!")

def get_merged_sandbox_html(files_dict):
    """Merges your HTML, CSS, and JS workspace structures into a preview frame."""
    html_content = ""
    for name, data in files_dict.items():
        if name.endswith(".html"):
            html_content = data["content"]
            break
            
    if not html_content:
        file_list_html = "<ul>" + "".join([f"<li><b>{name}</b> ({data['language']})</li>" for name, data in files_dict.items()]) + "</ul>"
        return f"""
        <div style="background-color: #121214; color: #f3f4f6; font-family: sans-serif; padding: 30px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05); text-align: center;">
            <h3>🎮 Live Preview Sandbox Ready</h3>
            <p style="opacity: 0.8;">To view a live rendered app, make sure Titan compiles an <b>HTML file</b> in your directory tree.</p>
            <div style="text-align: left; max-width: 300px; margin: 20px auto; opacity: 0.9;">
                <b>Currently Compiled Files:</b>
                {file_list_html}
            </div>
        </div>
        """
        
    css_content = files_dict.get("style.css", {}).get("content", "")
    if css_content:
        html_content = re.sub(r'<link[^>]*href=["\']style\.css["\'][^>]*>', '', html_content)
        style_block = f"<style>\n{css_content}\n</style>"
        if "</head>" in html_content:
            html_content = html_content.replace("</head>", f"{style_block}\n</head>")
        else:
            html_content = f"{style_block}\n{html_content}"
            
    js_content = files_dict.get("script.js", {}).get("content", "")
    if js_content:
        html_content = re.sub(r'<script[^>]*src=["\']script\.js["\'][^>]*>[\s\S]*?</script>', '', html_content)
        script_block = f"<script>\n{js_content}\n</script>"
        if "</body>" in html_content:
            html_content = html_content.replace("</body>", f"{script_block}\n</body>")
        else:
            html_content = f"{html_content}\n{script_block}"
            
    return html_content

# =====================================================================
# 📦 GAME BLUEPRINTS CATALOGUE (Fully written and closed templates)
# =====================================================================
BLUEPRINT_CATALOG = {
    "🌌 Galactic Cosmic Sweeper (2D Shooter)": {
        "index.html": """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Galactic Cosmic Sweeper</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="game-container">
        <div id="hud">
            <span>Score: <span id="score-val">0</span></span>
            <span>Energy: <span id="energy-val">100</span>%</span>
        </div>
        <canvas id="gameCanvas"></canvas>
        <div id="controls-info">Press Arrow Keys to move, Spacebar to release Clean-up beams. Clear the space debris!</div>
        <div id="game-over-screen" class="hidden">
            <h2>Sweeping Mission Complete!</h2>
            <p>Debris Cleaned: <span id="final-score">0</span></p>
            <button id="restart-btn" onclick="resetGame()">Deploy New Sweeper</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>""",
        "style.css": """* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}
body {
    background-color: #050508;
    color: #00ffff;
    font-family: 'Courier New', monospace;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    overflow: hidden;
}
#game-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    max-width: 600px;
    max-height: 500px;
    border: 2px solid #00f0ff;
    border-radius: 10px;
    box-shadow: 0 0 25px rgba(0, 240, 255, 0.2);
    overflow: hidden;
    background: radial-gradient(circle at center, #0a0a18 0%, #030308 100%);
}
#hud {
    position: absolute;
    top: 10px;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    padding: 0 20px;
    font-size: 1.1em;
    font-weight: bold;
    text-shadow: 0 0 8px #00f0ff;
    z-index: 10;
}
canvas {
    display: block;
    width: 100%;
    height: 100%;
}
#controls-info {
    position: absolute;
    bottom: 10px;
    width: 100%;
    text-align: center;
    font-size: 0.8em;
    opacity: 0.8;
    color: #ff00ff;
    text-shadow: 0 0 4px #ff00ff;
    z-index: 10;
}
#game-over-screen {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(5, 5, 10, 0.95);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 20;
}
#game-over-screen h2 {
    font-size: 1.8em;
    margin-bottom: 15px;
    text-shadow: 0 0 10px #ff00ff;
    color: #ff00ff;
}
#game-over-screen p {
    font-size: 1.2em;
    margin-bottom: 25px;
}
button {
    background-color: #00ffff;
    color: #000;
    border: none;
    border-radius: 5px;
    padding: 10px 20px;
    font-family: inherit;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 0 10px rgba(0, 240, 255, 0.4);
    transition: all 0.2s;
}
button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 18px rgba(0, 240, 255, 0.7);
}
.hidden {
    display: none !important;
}""",
        "script.js": """const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

function resize() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
}
window.onload = function() {
    resize();
    initGame();
};

let ship, lasers, debris, particles, score, energy, gameOver, keys;

function initGame() {
    ship = {
        x: canvas.width / 2,
        y: canvas.height - 40,
        size: 20,
        speed: 5
    };
    lasers = [];
    debris = [];
    particles = [];
    score = 0;
    energy = 100;
    gameOver = false;
    keys = {};
    
    window.addEventListener('keydown', e => { keys[e.code] = true; });
    window.addEventListener('keyup', e => { keys[e.code] = false; });
    
    requestAnimationFrame(gameLoop);
}

function spawnDebris() {
    if (Math.random() < 0.03 && debris.length < 8) {
        debris.push({
            x: Math.random() * (canvas.width - 20) + 10,
            y: -20,
            speed: Math.random() * 2 + 1.5,
            size: Math.random() * 15 + 10,
            angle: Math.random() * Math.PI * 2,
            rotSpeed: Math.random() * 0.05 - 0.025
        });
    }
}

function triggerExplosion(x, y, color) {
    for (let i = 0; i < 12; i++) {
        particles.push({
            x: x,
            y: y,
            vx: (Math.random() - 0.5) * 6,
            vy: (Math.random() - 0.5) * 6,
            size: Math.random() * 3 + 1,
            life: 30,
            maxLife: 30,
            color: color
        });
    }
}

function update() {
    if (gameOver) return;
    
    if (keys['ArrowLeft'] && ship.x > ship.size) ship.x -= ship.speed;
    if (keys['ArrowRight'] && ship.x < canvas.width - ship.size) ship.x += ship.speed;
    
    if (keys['Space']) {
        keys['Space'] = false;
        lasers.push({
            x: ship.x,
            y: ship.y - 15,
            speed: 7,
            size: 3
        });
    }
    
    for (let i = lasers.length - 1; i >= 0; i--) {
        lasers[i].y -= lasers[i].speed;
        if (lasers[i].y < 0) {
            lasers.splice(i, 1);
        }
    }
    
    spawnDebris();
    
    for (let i = debris.length - 1; i >= 0; i--) {
        let d = debris[i];
        d.y += d.speed;
        d.angle += d.rotSpeed;
        
        if (d.y > canvas.height + 20) {
            debris.splice(i, 1);
            energy = Math.max(0, energy - 10);
            if (energy <= 0) endGame();
            continue;
        }
        
        for (let j = lasers.length - 1; j >= 0; j--) {
            let l = lasers[j];
            let dist = Math.hypot(d.x - l.x, d.y - l.y);
            if (dist < d.size + l.size) {
                triggerExplosion(d.x, d.y, '#00ffff');
                debris.splice(i, 1);
                lasers.splice(j, 1);
                score += 10;
                document.getElementById('score-val').innerText = score;
                break;
            }
        }
        
        if (d) {
            let shipDist = Math.hypot(d.x - ship.x, d.y - ship.y);
            if (shipDist < d.size + ship.size) {
                triggerExplosion(ship.x, ship.y, '#ff00ff');
                debris.splice(i, 1);
                energy = Math.max(0, energy - 20);
                if (energy <= 0) endGame();
            }
        }
    }
    
    for (let i = particles.length - 1; i >= 0; i--) {
        let p = particles[i];
        p.x += p.vx;
        p.y += p.vy;
        p.life--;
        if (p.life <= 0) particles.splice(i, 1);
    }
    
    document.getElementById('energy-val').innerText = energy;
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = 'rgba(255, 255, 255, 0.15)';
    for(let i = 0; i < 30; i++) {
        let x = (Math.sin(i) * 0.5 + 0.5) * canvas.width;
        let y = ((i * 17) % canvas.height);
        ctx.fillRect(x, y, 1.5, 1.5);
    }
    
    ctx.fillStyle = '#ff00ff';
    ctx.strokeStyle = '#00ffff';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(ship.x, ship.y - 15);
    ctx.lineTo(ship.x - 15, ship.y + 10);
    ctx.lineTo(ship.x + 15, ship.y + 10);
    ctx.closePath();
    ctx.fill();
    ctx.stroke();
    
    ctx.fillStyle = '#00ffff';
    for (let l of lasers) {
        ctx.beginPath();
        ctx.arc(l.x, l.y, l.size, 0, Math.PI * 2);
        ctx.fill();
    }
    
    ctx.strokeStyle = '#00f0ff';
    ctx.fillStyle = 'rgba(0, 240, 255, 0.05)';
    ctx.lineWidth = 1.5;
    for (let d of debris) {
        ctx.save();
        ctx.translate(d.x, d.y);
        ctx.rotate(d.angle);
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {
            let angle = (i * Math.PI) / 3;
            let radius = d.size * (0.8 + Math.sin(i * 3) * 0.15);
            let px = Math.cos(angle) * radius;
            let py = Math.sin(angle) * radius;
            if (i === 0) ctx.moveTo(px, py);
            else ctx.lineTo(px, py);
        }
        ctx.closePath();
        ctx.fill();
        ctx.stroke();
        ctx.restore();
    }
    
    for (let p of particles) {
        ctx.fillStyle = p.color;
        ctx.globalAlpha = p.life / p.maxLife;
        ctx.fillRect(p.x, p.y, p.size, p.size);
    }
    ctx.globalAlpha = 1.0;
}

function gameLoop() {
    update();
    draw();
    if (!gameOver) {
        requestAnimationFrame(gameLoop);
    }
}

function endGame() {
    gameOver = true;
    document.getElementById('final-score').innerText = score;
    document.getElementById('game-over-screen').classList.remove('hidden');
}

function resetGame() {
    document.getElementById('game-over-screen').classList.add('hidden');
    document.getElementById('score-val').innerText = '0';
    initGame();
}"""
    },
    "🧱 Chunky Neon Brick-Breaker (Retro Arcade)": {
        "index.html": """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Chunky Neon Brick-Breaker</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="game-container">
        <div id="hud">
            <span>Score: <span id="score-val">0</span></span>
            <span>Lives: <span id="lives-val">3</span></span>
        </div>
        <canvas id="gameCanvas"></canvas>
        <div id="game-over-screen" class="hidden">
            <h2 id="end-title">Game Over</h2>
            <p>Score Reached: <span id="final-score">0</span></p>
            <button id="restart-btn" onclick="resetGame()">Start New Round</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>""",
        "style.css": """* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}
body {
    background-color: #0b0c10;
    color: #4630f5;
    font-family: 'Courier New', monospace;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}
#game-container {
    position: relative;
    width: 100vw;
    height: 100vh;
    max-width: 600px;
    max-height: 500px;
    border: 2px solid #00ffcc;
    border-radius: 12px;
    box-shadow: 0 0 30px rgba(0, 255, 204, 0.15);
    background-color: #111116;
    overflow: hidden;
}
#hud {
    position: absolute;
    top: 15px;
    left: 0;
    width: 100%;
    display: flex;
    justify-content: space-between;
    padding: 0 20px;
    font-size: 1.2em;
    font-weight: bold;
    color: #00ffcc;
    text-shadow: 0 0 8px #00ffcc;
    z-index: 10;
}
canvas {
    display: block;
    width: 100%;
    height: 100%;
}
#game-over-screen {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(11, 12, 16, 0.95);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 20;
}
#game-over-screen h2 {
    font-size: 2em;
    margin-bottom: 15px;
    color: #ff007f;
    text-shadow: 0 0 12px #ff007f;
}
button {
    background-color: #00ffcc;
    color: #111116;
    border: none;
    border-radius: 6px;
    padding: 12px 24px;
    font-family: inherit;
    font-weight: bold;
    cursor: pointer;
    box-shadow: 0 0 10px rgba(0, 255, 204, 0.3);
}
button:hover {
    transform: scale(1.05);
    box-shadow: 0 0 20px rgba(0, 255, 204, 0.6);
}
.hidden {
    display: none !important;
}""",
        "script.js": """const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');

let paddle, ball, bricks, score, lives, gameOver, keys;

window.onload = function() {
    canvas.width = canvas.offsetWidth;
    canvas.height = canvas.offsetHeight;
    initGame();
};

function initGame() {
    paddle = {
        width: 100,
        height: 12,
        x: (canvas.width - 100) / 2,
        y: canvas.height - 30,
        speed: 6
    };
    
    ball = {
        x: canvas.width / 2,
        y: canvas.height - 50,
        vx: 3,
        vy: -4,
        radius: 8
    };
    
    score = 0;
    lives = 3;
    gameOver = false;
    keys = {};
    
    const brickRows = 5;
    const brickCols = 6;
    const padding = 10;
    const topOffset = 60;
    const brickWidth = (canvas.width - (padding * (brickCols + 1))) / brickCols;
    const brickHeight = 16;
    
    bricks = [];
    const colors = ['#ff0055', '#00ffcc', '#ffcc00', '#0099ff', '#9900ff'];
    
    for (let r = 0; r < brickRows; r++) {
        for (let c = 0; c < brickCols; c++) {
            bricks.push({
                x: padding + c * (brickWidth + padding),
                y: topOffset + r * (brickHeight + padding),
                width: brickWidth,
                height: brickHeight,
                color: colors[r],
                active: true
            });
        }
    }
    
    window.addEventListener('keydown', e => { keys[e.code] = true; });
    window.addEventListener('keyup', e => { keys[e.code] = false; });
    
    requestAnimationFrame(gameLoop);
}

function update() {
    if (gameOver) return;
    
    if (keys['ArrowLeft'] && paddle.x > 0) paddle.x -= paddle.speed;
    if (keys['ArrowRight'] && paddle.x < canvas.width - paddle.width) paddle.x += paddle.speed;
    
    ball.x += ball.vx;
    ball.y += ball.vy;
    
    if (ball.x < ball.radius || ball.x > canvas.width - ball.radius) {
        ball.vx = -ball.vx;
    }
    
    if (ball.y < ball.radius) {
        ball.vy = -ball.vy;
    }
    
    if (ball.y > paddle.y - ball.radius && 
        ball.x > paddle.x && 
        ball.x < paddle.x + paddle.width) {
        
        let hitPoint = (ball.x - (paddle.x + paddle.width / 2)) / (paddle.width / 2);
        ball.vx = hitPoint * 5;
        ball.vy = -Math.abs(ball.vy);
    }
    
    let allCleared = true;
    for (let b of bricks) {
        if (!b.active) continue;
        allCleared = false;
        
        if (ball.x > b.x - ball.radius && 
            ball.x < b.x + b.width + ball.radius && 
            ball.y > b.y - ball.radius && 
            ball.y < b.y + b.height + ball.radius) {
            
            b.active = false;
            ball.vy = -ball.vy;
            score += 15;
            document.getElementById('score-val').innerText = score;
            break;
        }
    }
    
    if (allCleared) {
        endGame(true);
    }
    
    if (ball.y > canvas.height + ball.radius) {
        lives--;
        document.getElementById('lives-val').innerText = lives;
        if (lives <= 0) {
            endGame(false);
        } else {
            ball.x = canvas.width / 2;
            ball.y = canvas.height - 50;
            ball.vx = 3;
            ball.vy = -4;
        }
    }
}

function draw() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#00ffcc';
    ctx.shadowBlur = 10;
    ctx.shadowColor = '#00ffcc';
    ctx.fillRect(paddle.x, paddle.y, paddle.width, paddle.height);
    
    ctx.beginPath();
    ctx.fillStyle = '#ff00ff';
    ctx.shadowColor = '#ff00ff';
    ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
    ctx.fill();
    
    ctx.shadowBlur = 4;
    for (let b of bricks) {
        if (!b.active) continue;
        ctx.fillStyle = b.color;
        ctx.shadowColor = b.color;
        ctx.fillRect(b.x, b.y, b.width, b.height);
    }
    ctx.shadowBlur = 0;
}

function gameLoop() {
    update();
    draw();
    if (!gameOver) {
        requestAnimationFrame(gameLoop);
    }
}

function endGame(won) {
    gameOver = true;
    document.getElementById('final-score').innerText = score;
    const title = document.getElementById('end-title');
    if (won) {
        title.innerText = "🏆 Victory reached!";
        title.style.color = "#00ffcc";
    } else {
        title.innerText = "💥 Board Crashed!";
        title.style.color = "#ff007f";
    }
    document.getElementById('game-over-screen').classList.remove('hidden');
}

function resetGame() {
    document.getElementById('game-over-screen').classList.add('hidden');
    document.getElementById('score-val').innerText = '0';
    document.getElementById('lives-val').innerText = '3';
    initGame();
}"""
    },
    "🐱 Interactive Pixel Tamagotchi (Virtual Pet)": {
        "index.html": """<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pixel Tamagotchi Simulator</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <div id="virtual-cage">
        <h3 id="pet-name">🔋 TITAN CORE-BOT</h3>
        <div id="display-screen">
            <div id="robot-pet">
                <svg width="120" height="120" viewBox="0 0 100 100">
                    <rect x="25" y="20" width="50" height="40" rx="10" fill="#00ffcc" stroke="#111" stroke-width="3"/>
                    <circle cx="40" cy="35" r="5" fill="#111" id="left-eye"/>
                    <circle cx="60" cy="35" r="5" fill="#111" id="right-eye"/>
                    <path d="M 40,48 Q 50,55 60,48" stroke="#111" stroke-width="3" fill="none" id="mouth"/>
                    <line x1="50" y1="20" x2="50" y2="8" stroke="#00ffcc" stroke-width="4"/>
                    <circle cx="50" cy="6" r="4" fill="#ff00ff"/>
                    <rect x="35" y="60" width="30" height="25" rx="5" fill="#ff00ff" stroke="#111" stroke-width="3"/>
                </svg>
            </div>
            <div id="status-bubble">BEEP! Power level is excellent, creator!</div>
        </div>
        <div id="bars">
            <div class="stat">
                <span>Charge Level (Hunger)</span>
                <div class="bar-container"><div class="fill" id="charge-bar" style="width: 100%;"></div></div>
            </div>
            <div class="stat">
                <span>Fun Entropy (Happiness)</span>
                <div class="bar-container"><div class="fill" id="fun-bar" style="width: 100%;"></div></div>
            </div>
            <div class="stat">
                <span>System Cleanliness (Hygiene)</span>
                <div class="bar-container"><div class="fill" id="clean-bar" style="width: 100%;"></div></div>
            </div>
        </div>
        <div id="actions">
            <button onclick="interact('feed')">🔌 Charge Bot</button>
            <button onclick="interact('play')">🎮 Code Games</button>
            <button onclick="interact('clean')">🧹 Clear Cache</button>
        </div>
    </div>
    <script src="script.js"></script>
</body>
</html>""",
        "style.css": """* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}
body {
    background-color: #0b0b0c;
    color: #00ffcc;
    font-family: 'Courier New', monospace;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
}
#virtual-cage {
    background-color: #1a1a1f;
    border: 3px solid #ff00ff;
    border-radius: 20px;
    width: 320px;
    padding: 20px;
    box-shadow: 0 0 25px rgba(255, 0, 255, 0.2);
    text-align: center;
}
#pet-name {
    font-size: 1.15em;
    margin-bottom: 12px;
    color: #ff00ff;
    text-shadow: 0 0 8px #ff00ff;
}
#display-screen {
    background-color: #111113;
    border: 2px solid #00ffcc;
    border-radius: 10px;
    height: 170px;
    padding: 10px;
    margin-bottom: 15px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}
#status-bubble {
    font-size: 0.75em;
    margin-top: 10px;
    color: #ffffff;
    opacity: 0.9;
    max-width: 250px;
}
#bars {
    text-align: left;
    margin-bottom: 20px;
}
.stat {
    margin-bottom: 8px;
    font-size: 0.75em;
    color: #ff00ff;
}
.bar-container {
    background-color: #2a2a2f;
    border-radius: 5px;
    height: 12px;
    overflow: hidden;
    margin-top: 3px;
    border: 1px solid rgba(255,255,255,0.05);
}
.fill {
    background: linear-gradient(90deg, #00ffcc, #ff00ff);
    height: 100%;
    transition: width 0.3s ease;
}
#actions {
    display: flex;
    justify-content: space-between;
    gap: 8px;
}
button {
    flex: 1;
    background-color: #00ffcc;
    color: #111;
    border: none;
    border-radius: 6px;
    padding: 10px 4px;
    font-size: 0.8em;
    font-family: inherit;
    font-weight: bold;
    cursor: pointer;
    transition: transform 0.1s;
}
button:hover {
    transform: scale(1.05);
}
#robot-pet {
    animation: bob 2s infinite ease-in-out;
}
@keyframes bob {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}""",
        "script.js": """let charge = 100;
let happiness = 100;
let hygiene = 100;

const bubble = document.getElementById('status-bubble');
const leftEye = document.getElementById('left-eye');
const rightEye = document.getElementById('right-eye');
const mouth = document.getElementById('mouth');

setInterval(() => {
    charge = Math.max(0, charge - 2);
    happiness = Math.max(0, happiness - 3);
    hygiene = Math.max(0, hygiene - 1.5);
    updateBars();
    checkFeelings();
}, 2000);

function updateBars() {
    document.getElementById('charge-bar').style.width = charge + '%';
    document.getElementById('fun-bar').style.width = happiness + '%';
    document.getElementById('clean-bar').style.width = hygiene + '%';
}

function checkFeelings() {
    if (charge < 30) {
        bubble.innerText = "LOW POWER! Feed me code cycles or plug me in!";
        setFace('sad');
    } else if (happiness < 30) {
        bubble.innerText = "Boring alert... Play games with me, creator!";
        setFace('sad');
    } else if (hygiene < 30) {
        bubble.innerText = "System memory flooded with junk cache files!";
        setFace('mad');
    } else {
        bubble.innerText = "Core operating parameters are green! Code on, creator.";
        setFace('normal');
    }
}

function setFace(mood) {
    if (mood === 'sad') {
        leftEye.setAttribute('cy', '38');
        rightEye.setAttribute('cy', '38');
        mouth.setAttribute('d', 'M 40,53 Q 50,45 60,53');
    } else if (mood === 'mad') {
        leftEye.setAttribute('cy', '34');
        rightEye.setAttribute('cy', '34');
        mouth.setAttribute('d', 'M 40,50 L 60,50');
    } else {
        leftEye.setAttribute('cy', '35');
        rightEye.setAttribute('cy', '35');
        mouth.setAttribute('d', 'M 40,48 Q 50,55 60,48');
    }
}

function interact(action) {
    if (action === 'feed') {
        charge = Math.min(100, charge + 20);
        bubble.innerText = "🔋 Systems Charged! Mmm, fresh binary calculations.";
        triggerAnimateFace();
    } else if (action === 'play') {
        happiness = Math.min(100, happiness + 25);
        bubble.innerText = "🎮 Executing Pong.exe! Highly engaging!";
        triggerAnimateFace();
    } else if (action === 'clean') {
        hygiene = Math.min(100, hygiene + 30);
        bubble.innerText = "🧹 Cache and system registries purged completely.";
        triggerAnimateFace();
    }
    updateBars();
}

function triggerAnimateFace() {
    leftEye.setAttribute('r', '2');
    setTimeout(() => {
        leftEye.setAttribute('r', '5');
    }, 400);
}"""
    }
}

# --- UTILITY: PARSING ENGINE V2 (Multi-File Extractor) ---
def extract_all_code_blocks(text):
    """Scans the generated assistant text and pulls out multiple program scripts."""
    bt = chr(96) * 3
    pattern = rf"{bt}(\w+)?\n([\s\S]*?)\n{bt}"
    matches = re.findall(pattern, text)
    
    extracted_files = []
    for idx, match in enumerate(matches):
        lang = match[0].lower() if match[0] else "txt"
        code = match[1]
        
        if lang == "html":
            filename = "index.html" if idx == 0 else f"page_{idx}.html"
        elif lang == "css":
            filename = "style.css"
        elif lang == "javascript" or lang == "js":
            filename = "script.js"
        elif lang == "java":
            class_match = re.search(r"class\s+(\w+)", code)
            filename = f"{class_match.group(1)}.java" if class_match else f"Class_{idx}.java"
        elif lang == "python" or lang == "py":
            filename = f"script_{idx}.py" if idx > 0 else "main.py"
        else:
            filename = f"file_{idx}.{lang}"
            
        extracted_files.append({
            "filename": filename,
            "language": lang,
            "content": code
        })
    return extracted_files

# --- UTILITY: ZIP CREATOR FOR EXPORTS ---
def create_project_zip(files_dict):
    """Creates a zip file in memory containing all generated workspace files."""
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zip_file:
        for filename, data in files_dict.items():
            zip_file.writestr(filename, data["content"])
    return zip_buffer.getvalue()

# =====================================================================
# ⚙️ TROPHY ROOM UTILITY FUNCTIONS
# =====================================================================
if "unlocked_achievements" not in st.session_state:
    st.session_state.unlocked_achievements = []

# --- SYSTEM MEMORY SETUP (Session State) ---
if "initialized" not in st.session_state:
    st.session_state.initialized = False
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "messages" not in st.session_state:
    st.session_state.messages = []
if "generated_files" not in st.session_state:
    st.session_state.generated_files = {}
if "selected_file" not in st.session_state:
    st.session_state.selected_file = ""
if "task_logs" not in st.session_state:
    st.session_state.task_logs = ["🟢 System pipeline initialized successfully.", "📡 Multi-file extraction engine v2 loaded."]
if "announcements" not in st.session_state:
    st.session_state.announcements = [
        "🚀 Titan v2.1 Configurable Engine is online!",
        "🏆 Customize Titan's mission guidelines directly in the sidebar!"
    ]
if "last_explained_file" not in st.session_state:
    st.session_state.last_explained_file = ""
if "school_explanation" not in st.session_state:
    st.session_state.school_explanation = ""

# Preload the customizable Jarvis Butler persona instructions
DEFAULT_SYSTEM_INSTRUCTIONS = (
    "You are Titan, a highly formal, articulate, and brilliant software engineering intelligence, "
    "modeled to sound exactly like a highly sophisticated personal butler-assistant.\n\n"
    "CORE RULES:\n"
    "1. Address the user with supreme respect (using polite terms like 'creator', 'developer', or 'guest' where natural), maintaining a calm, articulate helper persona.\n"
    "2. Focus strictly on generating complete, functional, and highly optimized code blocks.\n"
    "3. Ground all code in verified programming rules (strictly no hallucinations).\n"
    "4. If a user asks a casual question, answer elegantly, then note that they can change operational modes in your sidebar settings.\n"
    "5. SAFETY GUARDRAIL: Under no circumstances should you assist with mature, harmful, or illegal topics. Keep all content completely safe, healthy, and clean."
)

if "system_instructions" not in st.session_state:
    st.session_state.system_instructions = DEFAULT_SYSTEM_INSTRUCTIONS

# --- SCREEN 1: THE SETUP SCREEN (Login Gate) ---
if not st.session_state.initialized:
    _, center_col, _ = st.columns([1, 1.8, 1])
    with center_col:
        st.write("##")
        st.write("##")
        render_logo(width=120, align="center")
        st.markdown("<h1 style='text-align: center; margin-top: 15px;'>⚡ TITAN</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center; font-weight: 300; margin-top: -15px;'>{TEAM_NAME.upper()}</h3>", unsafe_allow_html=True)
        st.write("---")
        
        st.info("💻 **Developer Environment Access Gate**\n\nEnter your API key below to securely initialize your development pipelines.")
        user_key = st.text_input("🔑 System Access API Key", type="password", placeholder="Enter API Key...")
        
        st.write("##")
        if st.button("Establish Core Connection", use_container_width=True, type="primary"):
            if user_key.strip():
                st.session_state.api_key = user_key.strip()
                unlock_achievement("handshake", "Handshake Established")
                with st.spinner("Establishing secure handshake..."):
                    time.sleep(1.2)
                st.session_state.initialized = True
                st.rerun()
            else:
                st.error("Access key input cannot be left blank.")

# --- SCREEN 2: MULTI-PAGE DESKTOP ---
else:
    st.sidebar.write("##")
    if os.path.exists("titanlogo.png"):
        st.sidebar.image("titanlogo.png", width=70)
    else:
        st.sidebar.markdown(f"<h2>{SVG_BOLT_LOGO} TITAN</h2>", unsafe_allow_html=True)
    st.sidebar.markdown(f"<p style='font-size: 0.85em; opacity: 0.7; margin-top:-10px;'>By {TEAM_NAME}</p>", unsafe_allow_html=True)
    st.sidebar.write("---")
    
    current_page = st.sidebar.radio(
        "Navigation Hub", 
        ["Active Workspace", "🔌 Integrations Hub", "News & Updates", "Admin Panel", "Support Desk", "Legal Frame"]
    )
    
    if current_page == "Active Workspace":
        st.sidebar.write("---")
        st.sidebar.markdown("### ⚙️ Operational Settings")
        
        op_mode = st.sidebar.selectbox(
            "Operational Mode", 
            ["💻 Coding Engine", "💬 Chat Companion"]
        )
        
        # CONFIGURABLE SYSTEM INSTRUCTIONS TEXT AREA
        st.sidebar.markdown("### 🔧 Core Mission Directives")
        custom_instructions = st.sidebar.text_area(
            "System Instructions Configuration", 
            value=st.session_state.system_instructions,
            height=180,
            help="Define or rewrite Titan's core intelligence constraints and rules on-the-fly."
        )
        if custom_instructions != st.session_state.system_instructions:
            st.session_state.system_instructions = custom_instructions
            st.sidebar.success("Mission parameters reconfigured!")
        
        st.sidebar.write("---")
        st.sidebar.markdown("### 🏆 Titan's Trophy Room")
        
        unlocked = st.session_state.unlocked_achievements
        total_badges = 5
        score = len(unlocked)
        
        if score <= 1:
            level_name = "Level 1: Novice Creator 🛠️"
        elif score <= 3:
            level_name = "Level 2: Sandbox Apprentice 🕹️"
        elif score == 4:
            level_name = "Level 3: Master Engineer 🧠"
        else:
            level_name = "Level 4: Titan Architect 👑"
            
        st.sidebar.markdown(f"**{level_name}**")
        st.sidebar.progress(score / total_badges)
        st.sidebar.markdown(f"<small>Unlocked: {score} of {total_badges} Badges</small>", unsafe_allow_html=True)
        
        badge_icons = {
            "handshake": "🔑 Establish Link",
            "stylist": "🎨 Style Space",
            "blueprint": "🚀 Deploy Blueprint",
            "sandbox": "🎮 Enter Sandbox",
            "scholar": "🎓 Study Files"
        }
        for b_id, b_name in badge_icons.items():
            if b_id in unlocked:
                st.sidebar.markdown(f"✅ **{b_name}**")
            else:
                st.sidebar.markdown(f"🔒 *{b_name}*")
        
        st.sidebar.write("---")
        st.sidebar.markdown("### 🎨 Theme Customization")
        
        theme_options = list(THEME_STYLES.keys())
        selected_theme = st.sidebar.selectbox(
            "Select Workspace Theme", 
            theme_options, 
            index=theme_options.index(st.session_state.active_theme)
        )
        if selected_theme != st.session_state.active_theme:
            st.session_state.active_theme = selected_theme
            unlock_achievement("stylist", "Master Stylist")
            st.rerun()
            
        st.sidebar.write("---")
        st.sidebar.markdown("### 🕹️ Game Blueprint Catalog")
        
        selected_blueprint_name = st.sidebar.selectbox(
            "Select Game Blueprint", 
            ["Choose Template..."] + list(BLUEPRINT_CATALOG.keys())
        )
        
        if selected_blueprint_name != "Choose Template...":
            if st.sidebar.button("🎮 Deploy Selected Blueprint", use_container_width=True, type="secondary"):
                st.session_state.generated_files = {}
                blueprint_files = BLUEPRINT_CATALOG[selected_blueprint_name]
                for filename, code in blueprint_files.items():
                    lang = "html" if filename.endswith(".html") else ("css" if filename.endswith(".css") else "javascript")
                    st.session_state.generated_files[filename] = {
                        "language": lang,
                        "content": code
                    }
                st.session_state.selected_file = "index.html"
                st.session_state.task_logs.append(f"🎮 Successfully deployed {selected_blueprint_name} template code files to workspace.")
                unlock_achievement("blueprint", "Game Dev Recruit")
                st.success("Blueprint Loaded!")
                st.rerun()
        
        st.sidebar.write("---")
        st.sidebar.markdown("### 🛠️ Core Tuning")
        model_mapping = {
            "Titan-V5-Agile (Llama 3.1 8B)": "llama-3.1-8b-instant",
            "Titan-V5-DeepMind (Llama 3.1 70B)": "llama-3.1-70b-versatile",
            "Titan-Light (Gemma 2 9B)": "gemma2-9b-it"
        }
        selected_friendly_model = st.sidebar.selectbox("Active Pipeline Model", list(model_mapping.keys()))
        selected_model_id = model_mapping[selected_friendly_model]
        temp = st.sidebar.slider("Engine Entropy (Temp)", 0.0, 1.0, 0.3)
        
        st.sidebar.write("---")
        st.sidebar.markdown("### 📢 Core Broadcasts")
        for ann in st.session_state.announcements:
            st.sidebar.warning(f"📣 {ann}")
            
    st.sidebar.write("---")
    if st.sidebar.button("🚪 Terminate Session", type="secondary", use_container_width=True):
        st.session_state.initialized = False
        st.session_state.messages = []
        st.session_state.generated_files = {}
        st.session_state.selected_file = ""
        st.session_state.last_explained_file = ""
        st.session_state.school_explanation = ""
        st.session_state.unlocked_achievements = []
        st.rerun()

    # --- RENDERING PAGES ---
    if current_page == "Active Workspace":
        header_col, reset_col = st.columns([8, 2])
        with header_col:
            st.markdown(f"<h1>{SVG_WORKSPACE_ICON} Titan // Active Workspace</h1>", unsafe_allow_html=True)
            st.markdown(f"<p style='font-size: 1.1em; opacity: 0.8; margin-top:-5px;'>Active Mode: <b>{op_mode}</b> // Current Theme: <b>{st.session_state.active_theme}</b> // Powered by {TEAM_NAME}</p>", unsafe_allow_html=True)
        with reset_col:
            st.write("##")
            if st.button("🧹 Clear Chat History", use_container_width=True, type="secondary"):
                st.session_state.messages = []
                st.rerun()
                
        st.write("---")
        chat_col, workspace_col = st.columns([1.2, 1.3])
        
        with chat_col:
            st.markdown("### 💬 System Interface Talking Space")
            if op_mode == "💻 Coding Engine":
                st.write("Command your neural pipeline to generate complete code files, structures, or debug scripts.")
            else:
                st.write("Chat freely with Titan about concepts, logic, schoolwork, or simply have an encouraging conversation.")
            
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.write(msg["content"])
            
            if user_prompt := st.chat_input("Input command directives to Titan..."):
                with st.chat_message("user"):
                    st.write(user_prompt)
                st.session_state.messages.append({"role": "user", "content": user_prompt})
                
                with st.chat_message("assistant"):
                    status_placeholder = st.empty()
                    status_placeholder.markdown("*Analyzing parameters and compiling neural directives...*")
                    
                    try:
                        client = Groq(api_key=st.session_state.api_key)
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": st.session_state.system_instructions},
                                *st.session_state.messages
                            ],
                            model=selected_model_id,
                            temperature=temp,
                        )
                        ai_response = chat_completion.choices[0].message.content
                        status_placeholder.write(ai_response)
                        
                        new_extracted_files = extract_all_code_blocks(ai_response)
                        if new_extracted_files:
                            for f in new_extracted_files:
                                st.session_state.generated_files[f["filename"]] = {
                                    "language": f["language"],
                                    "content": f["content"]
                                }
                            st.session_state.selected_file = new_extracted_files[0]["filename"]
                            st.session_state.task_logs.append(f"🏁 Successfully extracted {len(new_extracted_files)} files to directory using {selected_friendly_model}.")
                        else:
                            st.session_state.task_logs.append("ℹ️ Conversation updated successfully.")
                        
                        st.session_state.messages.append({"role": "assistant", "content": ai_response})
                        st.rerun()
                        
                    except Exception as e:
                        status_placeholder.error(f"Error connecting to Titan: {e}")
                        st.session_state.task_logs.append(f"❌ Handshake failed: {e}")

        with workspace_col:
            st.markdown("### 🖥️ Workspace & Sandbox Viewport")
            for log in reversed(st.session_state.task_logs[-2:]):
                st.info(log)
            
            st.write("---")
            tab_files, tab_sandbox, tab_school = st.tabs([
                "📁 File Editor", 
                "🎮 Live Preview Sandbox", 
                "🎓 Titan's Code School"
            ])
            
            with tab_files:
                st.markdown("📂 **Project Directory System**")
                if st.session_state.generated_files:
                    for filename in st.session_state.generated_files.keys():
                        label = f" 📜 {filename}"
                        if filename == st.session_state.selected_file:
                            label = f" 🎯 {filename} (Active View)"
                        
                        if st.button(label, key=f"file_select_{filename}", use_container_width=True, type="secondary"):
                            st.session_state.selected_file = filename
                            st.rerun()
                else:
                    st.info("📁 Project directory is empty. Deploy a Game Template from the sidebar or ask Titan to write code!")
                
                st.write("---")
                st.markdown("💻 **Extracted Code Viewport**")
                
                active_file = st.session_state.selected_file
                if active_file and active_file in st.session_state.generated_files:
                    st.markdown(f"🔬 Active file: `{active_file}` (`{st.session_state.generated_files[active_file]['language']}`)")
                    st.code(
                        st.session_state.generated_files[active_file]["content"], 
                        language=st.session_state.generated_files[active_file]["language"]
                    )
                    
                    st.write("---")
                    st.markdown("💾 **Export Pipelines**")
                    dl_col1, dl_col2 = st.columns(2)
                    with dl_col1:
                        file_content = st.session_state.generated_files[active_file]["content"]
                        st.download_button(
                            label=f"Download {active_file}",
                            data=file_content,
                            file_name=active_file,
                            mime="text/plain",
                            use_container_width=True,
                            type="secondary"
                        )
                    with dl_col2:
                        zip_data = create_project_zip(st.session_state.generated_files)
                        st.download_button(
                            label="Export Project (.ZIP)",
                            data=zip_data,
                            file_name="titan_project.zip",
                            mime="application/zip",
                            use_container_width=True,
                            type="primary"
                        )
                else:
                    st.info("Select a file from your directory tree to view the raw codebase.")

            with tab_sandbox:
                st.markdown("### 🎮 Dynamic Play Sandbox")
                st.write("Titan merges your HTML, CSS, and JS blocks into a live-running preview. Play your app or game instantly below!")
                if st.session_state.generated_files:
                    merged_html = get_merged_sandbox_html(st.session_state.generated_files)
                    st.components.v1.html(merged_html, height=500, scrolling=True)
                    unlock_achievement("sandbox", "Sandbox Pioneer")
                else:
                    st.info("No generated files found. Deploy a blueprint from the sidebar to play an arcade game instantly!")

            with tab_school:
                st.markdown("### 🎓 Titan's Code School")
                st.write("Welcome, creator! Code School mode breaks down how your selected file actually works, teaching you the core concepts.")
                active_file = st.session_state.selected_file
                if active_file and active_file in st.session_state.generated_files:
                    st.markdown(f"**Selected File:** `{active_file}`")
                    
                    if st.session_state.last_explained_file != active_file:
                        st.session_state.school_explanation = ""
                    
                    if st.button("🎓 Ask Titan to Explain This Code", use_container_width=True, type="primary"):
                        st.session_state.last_explained_file = active_file
                        with st.spinner("Preparing tutorial breakdown..."):
                            try:
                                client = Groq(api_key=st.session_state.api_key)
                                school_prompt = (
                                    "You are Titan, an elegant, encouraging, and highly articulate coding tutor. "
                                    "Your mission is to explain the provided program file in a simple, fun, step-by-step, and educational way "
                                    "that a beginner can easily understand and learn from. Address the user with supreme respect. "
                                    "Use clean, positive, healthy under-18 appropriate analogies."
                                )
                                tutoring_query = f"Please explain the code of this file named '{active_file}':\n\n```\n{st.session_state.generated_files[active_file]['content']}\n```"
                                
                                tutor_completion = client.chat.completions.create(
                                    messages=[
                                        {"role": "system", "content": school_prompt},
                                        {"role": "user", "content": tutoring_query}
                                    ],
                                    model=selected_model_id,
                                    temperature=0.3
                                )
                                st.session_state.school_explanation = tutor_completion.choices[0].message.content
                                st.session_state.task_logs.append(f"🎓 Tutorial generated for {active_file}.")
                                unlock_achievement("scholar", "Code Scholar")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Could not connect to tutor core: {e}")
                    
                    if st.session_state.school_explanation:
                        st.write("---")
                        st.markdown(st.session_state.school_explanation)
                    else:
                        st.info("Click the button above to have Titan break down this script for you!")
                else:
                    st.info("Select a file from your directory tree, then click this tab to learn how it works!")
                
        render_footer()

    # =====================================================================
    # 🔌 NEW HUB PAGE: INTEGRATIONS & ROBOT HARDWARE CODES
    # =====================================================================
    elif current_page == "🔌 Integrations Hub":
        st.markdown(f"<h1>{SVG_INTEGRATION_ICON} 🔌 Integrations & Hardware Hub</h1>", unsafe_allow_html=True)
        st.markdown("<p style='font-size: 1.1em; opacity: 0.8; margin-top:-5px;'>Control custom embeds and link Titan directly to physical hardware and robots!</p>", unsafe_allow_html=True)
        st.write("---")
        
        embed_tab, robot_tab = st.tabs([
            "🌐 Web Embedder Widget Generator", 
            "🤖 Web Serial Physical Robot Link"
        ])
        
        with embed_tab:
            st.markdown("### 🖼️ Embed Titan into Any Website")
            st.write("Let anyone place your live Titan Studio inside their custom blog, portfolio, Wix, or WordPress page!")
            
            st.write("##")
            width_slider = st.slider("Embed Width (pixels or %)", 300, 1200, 800)
            height_slider = st.slider("Embed Height (pixels)", 400, 1000, 600)
            hide_sidebar = st.checkbox("Hide parent sidebar in embed", value=True)
            
            # Formulate the visitor's custom iframe code
            base_url = "https://titanai-mark5beta-rljyvyskurccnqxgrmxw3v.streamlit.app"
            embed_url = f"{base_url}?embed=true" if hide_sidebar else base_url
            
            iframe_code = f'<iframe src="{embed_url}" width="{width_slider}" height="{height_slider}" style="border: 2px solid #00ffcc; border-radius: 12px; box-shadow: 0 0 15px rgba(0, 255, 204, 0.25);"></iframe>'
            
            st.write("---")
            st.markdown("#### 📋 Copy-to-Clipboard HTML Block")
            st.code(iframe_code, language="html")
            
            st.write("---")
            st.markdown("#### 👀 Live Embed Preview")
            st.components.v1.html(iframe_code, height=height_slider+50)

        with robot_tab:
            st.markdown("### 🤖 Web Serial Physical Robot Link")
            st.write("Chromebook and browser power unlocked! Plug any USB robot controller (like an Arduino, Micro:bit, or Pico) into your Chromebook, click connect, and send direct serial steering commands.")
            
            st.write("##")
            
            # Native browser Web Serial integration package
            robot_web_serial_html = """
            <div id="serial-container" style="background-color: #111116; border: 2px solid #ff00ff; border-radius: 15px; padding: 25px; color: #ffffff; font-family: monospace; box-shadow: 0 0 25px rgba(255, 0, 255, 0.15); max-width: 600px; margin: auto;">
                <h3 style="color: #ff00ff; margin-top: 0; text-align: center;">🤖 WEB SERIAL CONTROLLER</h3>
                <p style="text-align: center; font-size: 0.9em; opacity: 0.8;">Securely handshake and drive physical robot wheels over USB serial protocols.</p>
                
                <div style="display: flex; gap: 10px; justify-content: center; margin-bottom: 20px;">
                    <button id="connect-btn" onclick="connectSerial()" style="background-color: #ff00ff; border: none; color: #000; font-weight: bold; padding: 12px 20px; border-radius: 8px; cursor: pointer; box-shadow: 0 0 10px rgba(255, 0, 255, 0.4); transition: transform 0.1s;">🔌 ESTABLISH HARDWARE LINK</button>
                    <button id="disconnect-btn" onclick="disconnectSerial()" style="background-color: #333; border: 1px solid #ff00ff; color: #ff00ff; font-weight: bold; padding: 12px 20px; border-radius: 8px; cursor: pointer;" disabled>Disconnect</button>
                </div>
                
                <div id="connection-status" style="text-align: center; color: #ff4b4b; font-weight: bold; margin-bottom: 15px;">🔌 STATUS: DISCONNECTED</div>
                
                <!-- Digital Simulated Sandbox Preview -->
                <div style="background-color: #050508; height: 180px; border-radius: 10px; position: relative; border: 1px dashed rgba(255,255,255,0.1); margin-bottom: 15px; overflow: hidden;">
                    <div id="sim-robot" style="width: 40px; height: 40px; background-color: #00ffcc; border-radius: 8px; position: absolute; top: 70px; left: 280px; transition: all 0.3s; display: flex; justify-content: center; align-items: center; box-shadow: 0 0 12px #00ffcc;">
                        <span style="color: #000; font-size: 1.2em; font-weight: bold;">🤖</span>
                    </div>
                    <div style="position: absolute; bottom: 8px; left: 10px; font-size: 0.75em; opacity: 0.6; color: #00ffcc;">Simulated Area Preview</div>
                </div>
                
                <!-- Controller Joystick Grid -->
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; max-width: 250px; margin: auto; margin-bottom: 20px;">
                    <div></div>
                    <button onclick="drive('FORWARD')" style="background-color: #00ffcc; border: none; color: #000; font-weight: bold; padding: 10px; border-radius: 8px; cursor: pointer;">⬆️</button>
                    <div></div>
                    <button onclick="drive('LEFT')" style="background-color: #00ffcc; border: none; color: #000; font-weight: bold; padding: 10px; border-radius: 8px; cursor: pointer;">⬅️</button>
                    <button onclick="drive('STOP')" style="background-color: #ff4b4b; border: none; color: #fff; font-weight: bold; padding: 10px; border-radius: 8px; cursor: pointer;">🛑</button>
                    <button onclick="drive('RIGHT')" style="background-color: #00ffcc; border: none; color: #000; font-weight: bold; padding: 10px; border-radius: 8px; cursor: pointer;">➡️</button>
                    <div></div>
                    <button onclick="drive('BACKWARD')" style="background-color: #00ffcc; border: none; color: #000; font-weight: bold; padding: 10px; border-radius: 8px; cursor: pointer;">⬇️</button>
                    <div></div>
                </div>
                
                <div style="background-color: #000; border-radius: 8px; padding: 10px; height: 100px; overflow-y: auto; font-size: 0.8em; border: 1px solid rgba(255,255,255,0.05);" id="serial-terminal">
                    <div style="color: #888;">[Terminal initialized. Waiting for connection...]</div>
                </div>
            </div>
            
            <script>
                let port;
                let writer;
                let rxPos = 280;
                let ryPos = 70;
                
                const robot = document.getElementById('sim-robot');
                const status = document.getElementById('connection-status');
                const terminal = document.getElementById('serial-terminal');
                const connectBtn = document.getElementById('connect-btn');
                const disconnectBtn = document.getElementById('disconnect-btn');
                
                function printLog(text, color="#888") {
                    terminal.innerHTML += `<div style="color: ${color};">[${new Date().toLocaleTimeString()}] ${text}</div>`;
                    terminal.scrollTop = terminal.scrollHeight;
                }
                
                async function connectSerial() {
                    if (!("serial" in navigator)) {
                        printLog("❌ Web Serial is not supported on this browser version. Use Google Chrome!", "#ff4b4b");
                        return;
                    }
                    try {
                        port = await navigator.serial.requestPort();
                        await port.open({ baudRate: 9600 });
                        writer = port.writable.getWriter();
                        
                        status.innerText = "🔌 STATUS: CONNECTED";
                        status.style.color = "#00ffcc";
                        connectBtn.disabled = true;
                        disconnectBtn.disabled = false;
                        printLog("✅ Connected to hardware controller successfully!", "#00ffcc");
                    } catch (err) {
                        printLog("❌ Connection rejected: " + err.message, "#ff4b4b");
                    }
                }
                
                async function disconnectSerial() {
                    try {
                        if (writer) {
                            await writer.releaseLock();
                        }
                        if (port) {
                            await port.close();
                        }
                        status.innerText = "🔌 STATUS: DISCONNECTED";
                        status.style.color = "#ff4b4b";
                        connectBtn.disabled = false;
                        disconnectBtn.disabled = true;
                        printLog("⚠️ Hardware link closed.", "#ffcc00");
                    } catch(err) {
                        printLog("❌ Error during shutdown: " + err.message, "#ff4b4b");
                    }
                }
                
                async function drive(direction) {
                    printLog(`Command Sent: ${direction}`, "#ff00ff");
                    
                    // Move simulated robot
                    if (direction === "FORWARD") ryPos = Math.max(10, ryPos - 20);
                    if (direction === "BACKWARD") ryPos = Math.min(130, ryPos + 20);
                    if (direction === "LEFT") rxPos = Math.max(10, rxPos - 40);
                    if (direction === "RIGHT") rxPos = Math.min(540, rxPos + 40);
                    
                    robot.style.top = ryPos + "px";
                    robot.style.left = rxPos + "px";
                    
                    // Direct binary output mapping for physical serial controller
                    if (writer) {
                        try {
                            const encoder = new TextEncoder();
                            await writer.write(encoder.encode(direction + "\\n"));
                        } catch (err) {
                            printLog("❌ Code write failure: " + err.message, "#ff4b4b");
                        }
                    }
                }
            </script>
            """
            st.components.v1.html(robot_web_serial_html, height=540)
            
        render_footer()

    elif current_page == "News & Updates":
        st.markdown(f"<h1>{SVG_NEWS_ICON} News & Developer Logs</h1>", unsafe_allow_html=True)
        st.write("---")
        st.markdown("### 🚀 Version Release: Beta v2.2.0 (The Integrations Hub Update)")
        st.caption("Updated on July 12, 2026")
        st.markdown("""
        * **🔌 User Integrations Hub:** Added a public-facing widgets tool! Any visitor can now customize and copy an HTML iframe embed block to share Titan Creator's Studio on their Wix, WordPress, or custom websites.
        * **🤖 Web Serial Hardware Driver:** Built client-side browser integration allowing any visitor to physically hook up microcontrollers (Arduino/Micro:bit) to their Chromebook's USB port and run robots right from the site!
        * **The 'Sir' Purge:** Purged conversational title calls from default prompts and tamagotchi parameters.
        * **Trophy Room local Level HUD:** Added dynamic, gamified unlocks to encourage coding, sandbox previews, and theme modifications.
        """)
        render_footer()

    elif current_page == "task manager":
        st.markdown(f"<h1>{SVG_ADMIN_ICON} Controller Workspace</h1>", unsafe_allow_html=True)
        st.write("---")
        st.info("⚠️ **Local Session Environment**\n\nTasks sent here stay registered to your local session state.")
        st.subheader("plan tasks")
        new_ann = st.text_input("Type task text:", placeholder="e.g., Core neural systems are operating within optimal limits...")
        
        if st.button("Send task", use_container_width=True, type="primary"):
            if new_ann:
                st.session_state.announcements.append(new_ann)
                st.success("task successfully registered!")
            else:
                st.error("Text field cannot be left blank.")
        st.write("---")
        st.subheader("Current Active tasks")
        for i, a in enumerate(st.session_state.announcements):
            st.warning(f"📣 {a}")
        render_footer()

    elif current_page == "Support Desk":
        st.markdown(f"<h1>{SVG_SUPPORT_ICON} Community & Support Hub</h1>", unsafe_allow_html=True)
        st.write("---")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 💬 Join our Discord Server")
            st.markdown(f"[💬 **Join the Official Discord Invite**]({DISCORD_URL})")
            st.write("##")
            st.markdown("### 📱 Official Media Channels")
            st.markdown(f"🎥 [**TitanAI Studio on YouTube**]({YOUTUBE_URL})")
            st.markdown(f"📱 [**TitanAI Studio on TikTok**]({TIKTOK_URL})")
        with col2:
            st.markdown("### 🛠️ Developer Support Desk")
            st.info(f"📬 For support or inquiries, please contact our community administrators via our official media handles.")
        render_footer()

    elif current_page == "Legal Frame":
        st.markdown(f"<h1>{SVG_LEGAL_ICON} Legal Framework</h1>", unsafe_allow_html=True)
        st.write("---")
        st.markdown("### 🛡️ Terms of Service & Liability Constraints")
        st.write("1. **User Creations & Code Ownership:** All outputs compiled inside the Titan Creator's Studio remain the property of the user.")
        st.write("2. **Sole Accountability:** Users assume complete, total, and sole responsibility for validating, testing, and compiling all code structures.")
        st.markdown(f"""
        <div style="border: 2px solid #ff4b4b; border-radius: 5px; padding: 15px; background-color: rgba(255, 75, 75, 0.1);">
            <p style="font-weight: bold; text-align: center; margin-top: 0; color: #ff4b4b;">⚠️ MANDATORY LEGAL DISCLAIMER</p>
            <p style="font-size: 0.95em; line-height: 1.6; text-align: justify; color: #f3f4f6;">
                THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. IN NO EVENT SHALL <b>{TEAM_NAME.upper()}</b> OR ITS DEVELOPERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY.
            </p>
        </div>
        """, unsafe_allow_html=True)
        render_footer()

