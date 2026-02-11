import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import base64

# Note: For full Google OAuth, install: pip install google-auth-oauthlib streamlit-oauth
# This is a simplified version. For production, use proper OAuth flow.

# Page configuration
st.set_page_config(
    page_title="Crypto Volatility Visualizer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Enhanced with improved welcome page and dropdown styling
st.markdown("""
    <style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    * {
        font-family: 'Outfit', sans-serif;
    }
    
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
    }
    
    /* Hide Streamlit Branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Welcome Page Styles */
    .welcome-container {
        background: linear-gradient(145deg, rgba(20,25,35,0.9), rgba(30,35,50,0.8));
        border-radius: 24px;
        padding: 60px 40px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        border: 1px solid rgba(45,212,191,0.1);
        backdrop-filter: blur(10px);
        margin-top: 40px;
    }
    
    .welcome-title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #2dd4bf 0%, #8b5cf6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 10px;
        letter-spacing: -1px;
    }
    
    .welcome-subtitle {
        color: #94a3b8;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 40px;
        font-weight: 300;
    }
    
    .welcome-badges {
        display: flex;
        justify-content: center;
        gap: 20px;
        margin-bottom: 40px;
        flex-wrap: wrap;
    }
    
    .badge {
        background: rgba(45,212,191,0.1);
        border: 1px solid rgba(45,212,191,0.3);
        padding: 10px 24px;
        border-radius: 50px;
        color: #2dd4bf;
        font-size: 0.9rem;
        font-weight: 500;
    }
    
    .form-section-title {
        color: #2dd4bf;
        font-size: 1.8rem;
        font-weight: 600;
        text-align: center;
        margin: 30px 0 30px 0;
    }
    
    .form-label {
        color: #e2e8f0;
        font-size: 0.95rem;
        font-weight: 500;
        margin-bottom: 8px;
        display: block;
    }
    
    /* Input Field Styling */
    .stTextInput > div > div > input {
        background-color: #1a1f2e !important;
        border: 1px solid rgba(45,212,191,0.2) !important;
        border-radius: 12px !important;
        color: #ecf0f1 !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2dd4bf !important;
        box-shadow: 0 0 0 2px rgba(45,212,191,0.1) !important;
    }
    
    .stTextInput > div > div > input::placeholder {
        color: #64748b !important;
    }
    
    /* Number Input Styling */
    .stNumberInput > div > div > input {
        background-color: #1a1f2e !important;
        border: 1px solid rgba(45,212,191,0.2) !important;
        border-radius: 12px !important;
        color: #ecf0f1 !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #2dd4bf !important;
        box-shadow: 0 0 0 2px rgba(45,212,191,0.1) !important;
    }
    
    /* Selectbox Styling - FIXED */
    .stSelectbox > div > div {
        background-color: #1a1f2e !important;
        border: 1px solid rgba(45,212,191,0.2) !important;
        border-radius: 12px !important;
    }
    
    .stSelectbox > div > div > div {
        background-color: #1a1f2e !important;
        color: #ecf0f1 !important;
        padding: 12px 16px !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    
    /* Remove red border on focus */
    .stSelectbox > div > div:focus-within {
        border-color: #2dd4bf !important;
        box-shadow: 0 0 0 2px rgba(45,212,191,0.1) !important;
    }
    
    /* Dropdown Menu Styling */
    [data-baseweb="popover"] {
        background-color: #1a1f2e !important;
    }
    
    [data-baseweb="select"] > div {
        background-color: #1a1f2e !important;
        border-color: rgba(45,212,191,0.2) !important;
    }
    
    [data-baseweb="select"] > div:focus {
        border-color: #2dd4bf !important;
        box-shadow: 0 0 0 2px rgba(45,212,191,0.1) !important;
    }
    
    /* Dropdown Options */
    [role="option"] {
        background-color: #1a1f2e !important;
        color: #ecf0f1 !important;
        padding: 12px 16px !important;
        white-space: normal !important;
        overflow: visible !important;
        min-height: 48px !important;
        display: flex !important;
        align-items: center !important;
    }
    
    [role="option"]:hover {
        background-color: rgba(45,212,191,0.2) !important;
    }
    
    ul[role="listbox"] {
        background-color: #1a1f2e !important;
        border: 1px solid rgba(45,212,191,0.3) !important;
        border-radius: 12px !important;
        max-height: 300px !important;
    }
    
    /* Fix for sidebar selectbox text wrapping */
    [data-testid="stSidebar"] .stSelectbox > div > div > div {
        white-space: normal !important;
        line-height: 1.3 !important;
        min-height: 40px !important;
    }
    
    /* Submit Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #2dd4bf 0%, #10b981 100%) !important;
        color: #0f1419 !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 14px 32px !important;
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 20px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(45,212,191,0.3) !important;
    }
    
    /* Google Login Button */
    .google-login-btn {
        background: white !important;
        color: #1f2937 !important;
        border: 1px solid rgba(45,212,191,0.2) !important;
        border-radius: 12px !important;
        padding: 14px 32px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        margin-top: 10px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 12px !important;
        cursor: pointer !important;
    }
    
    .google-login-btn:hover {
        background: #f9fafb !important;
        border-color: #2dd4bf !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 10px 30px rgba(45,212,191,0.2) !important;
    }
    
    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        margin: 20px 0;
        color: #64748b;
        font-size: 0.9rem;
    }
    
    .divider::before,
    .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid rgba(45,212,191,0.2);
    }
    
    .divider::before {
        margin-right: 15px;
    }
    
    .divider::after {
        margin-left: 15px;
    }
    
    /* Welcome Footer */
    .welcome-footer {
        text-align: center;
        margin-top: 50px;
        color: #64748b;
        font-size: 0.9rem;
    }
    
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 20px;
        margin-top: 30px;
    }
    
    .feature-card {
        background: rgba(30,35,50,0.5);
        border: 1px solid rgba(45,212,191,0.1);
        border-radius: 16px;
        padding: 20px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-color: rgba(45,212,191,0.4);
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 10px;
    }
    
    .feature-title {
        color: #e2e8f0;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 8px;
    }
    
    .feature-desc {
        color: #94a3b8;
        font-size: 0.9rem;
        line-height: 1.4;
    }
    
    /* Metric Cards */
    .metric-card {
        background: linear-gradient(145deg, rgba(20,25,35,0.8), rgba(30,35,50,0.6));
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(45,212,191,0.1);
        text-align: center;
    }
    
    .metric-title {
        color: #94a3b8;
        font-size: 0.85rem;
        font-weight: 500;
        margin-bottom: 8px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        color: #2dd4bf;
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 4px;
    }
    
    .metric-label {
        color: #64748b;
        font-size: 0.8rem;
    }
    
    /* Header Styles */
    .app-header {
        background: linear-gradient(145deg, rgba(20,25,35,0.95), rgba(30,35,50,0.85));
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        border: 1px solid rgba(45,212,191,0.1);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .app-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2dd4bf;
    }
    
    .app-subtitle {
        color: #94a3b8;
        font-size: 0.9rem;
    }
    
    .live-indicator {
        background: rgba(16,185,129,0.2);
        border: 1px solid #10b981;
        padding: 6px 16px;
        border-radius: 50px;
        color: #10b981;
        font-size: 0.85rem;
        font-weight: 600;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(20,25,35,0.6);
        border-radius: 12px;
        padding: 6px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #94a3b8;
        font-weight: 500;
        padding: 10px 20px;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(45,212,191,0.2), rgba(139,92,246,0.2));
        color: #2dd4bf !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #141925 0%, #1e2330 100%);
        border-right: 1px solid rgba(45,212,191,0.1);
    }
    
    .sidebar-title {
        color: #2dd4bf;
        font-size: 1.2rem;
        font-weight: 700;
        margin-bottom: 10px;
        text-align: center;
    }
    
    .sidebar-subtitle {
        color: #94a3b8;
        font-size: 0.85rem;
        text-align: center;
        margin-bottom: 24px;
    }
    
    /* Slider Styling */
    .stSlider > div > div > div > div {
        background-color: #2dd4bf !important;
    }
    
    .stSlider > div > div > div {
        background-color: rgba(45,212,191,0.2) !important;
    }
    
    /* Radio Button Styling */
    .stRadio > div {
        background-color: rgba(20,25,35,0.6);
        padding: 10px;
        border-radius: 12px;
    }
    
    .stRadio > div > label > div[data-testid="stMarkdownContainer"] > p {
        color: #ecf0f1;
    }
    
    /* Chart Container */
    .chart-container {
        background: rgba(15,20,25,0.4);
        border-radius: 16px;
        padding: 20px;
        border: 1px solid rgba(45,212,191,0.05);
        margin-bottom: 20px;
    }
    
    .chart-title {
        color: #e2e8f0;
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 16px;
    }
    
    /* Volatility Badge */
    .volatility-high {
        background: rgba(248,113,113,0.2);
        border: 1px solid #f87171;
        color: #f87171;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    .volatility-low {
        background: rgba(16,185,129,0.2);
        border: 1px solid #10b981;
        color: #10b981;
        padding: 4px 12px;
        border-radius: 50px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Data Table Styling */
    .stDataFrame {
        background-color: rgba(20,25,35,0.6) !important;
        border-radius: 12px;
    }
    
    /* Download Button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #8b5cf6 0%, #6366f1 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-weight: 600 !important;
    }
    
    /* Footer */
    .app-footer {
        text-align: center;
        padding: 30px;
        color: #64748b;
        font-size: 0.9rem;
        margin-top: 40px;
        border-top: 1px solid rgba(45,212,191,0.1);
    }
    
    /* Spacing */
    .spacer {
        height: 20px;
    }
    
    .spacer-lg {
        height: 40px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'initialized' not in st.session_state:
    st.session_state.initialized = False
    st.session_state.user_name = ""
    st.session_state.user_email = ""
    st.session_state.generated_data = None

# Helper functions
def gauss_random():
    """Generate Gaussian random number"""
    u = 0
    v = 0
    while u == 0:
        u = np.random.random()
    while v == 0:
        v = np.random.random()
    return np.sqrt(-2.0 * np.log(u)) * np.cos(2.0 * np.pi * v)

def simulate_price(days, base, amplitude, frequency, drift, noise, pattern):
    """Simulate cryptocurrency price movements"""
    prices = []
    dates = []
    start_date = datetime.now() - timedelta(days=days)
    
    for i in range(days):
        t = (i / days) * 2 * np.pi * frequency
        wave = 0
        
        if pattern == 'Sine Wave (Smooth Cycles)':
            wave = amplitude * np.sin(t)
        elif pattern == 'Cosine Wave (Phase Shift)':
            wave = amplitude * np.cos(t)
        elif pattern == 'Combined Waves':
            wave = amplitude * (0.6 * np.sin(t) + 0.4 * np.cos(2 * t))
        elif pattern == 'Realistic Behavior':
            wave = amplitude * (0.5 * np.sin(t) + 0.3 * np.cos(1.7 * t) + 0.2 * np.sin(3.1 * t))
        
        trend_val = drift * i
        noise_val = noise * gauss_random()
        price = max(100, base + wave + trend_val + noise_val)
        d = start_date + timedelta(days=i)
        
        dates.append(d)
        prices.append(price)
    
    return dates, prices

def generate_ohlcv(dates, close_prices):
    """Generate OHLCV data from close prices"""
    data = []
    for i, (d, close) in enumerate(zip(dates, close_prices)):
        spread = close * (0.01 + np.random.random() * 0.03)
        open_price = close + (np.random.random() - 0.5) * spread
        high = max(open_price, close) + np.random.random() * spread
        low = min(open_price, close) - np.random.random() * spread
        volume = int(500 + np.random.random() * 9500)
        
        data.append({
            'date': d,
            'open': open_price,
            'high': high,
            'low': low,
            'close': close,
            'volume': volume
        })
    
    return pd.DataFrame(data)

def get_plotly_layout():
    """Get consistent Plotly layout"""
    return {
        'paper_bgcolor': 'rgba(0,0,0,0)',
        'plot_bgcolor': 'rgba(15,20,25,0.4)',
        'font': {'color': '#ecf0f1', 'family': 'Outfit, sans-serif', 'size': 11},
        'margin': {'l': 50, 'r': 20, 't': 10, 'b': 40},
        'xaxis': {'gridcolor': 'rgba(255,255,255,0.05)', 'linecolor': 'rgba(255,255,255,0.1)'},
        'yaxis': {'gridcolor': 'rgba(255,255,255,0.05)', 'linecolor': 'rgba(255,255,255,0.1)', 'tickprefix': '$'},
        'showlegend': False,
        'hovermode': 'x unified'
    }

# Welcome Page
if not st.session_state.initialized:
    # Add spacing at top
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    
    # Center the welcome content
    col1, col2, col3 = st.columns([0.5, 3, 0.5])
    
    with col2:
        # Opening container div
        st.markdown('<div class="welcome-container">', unsafe_allow_html=True)
        
        # Title and subtitle
        st.markdown("""
            <div class="welcome-title">📊 Crypto Volatility Visualizer</div>
            <div class="welcome-subtitle">🚀 Real-time Data Analysis & Market Insights</div>
        """, unsafe_allow_html=True)
        
        # Badges
        st.markdown("""
            <div class="welcome-badges">
                <span class="badge">📊 INTERACTIVE</span>
                <span class="badge">📈 REAL-TIME</span>
                <span class="badge">🔥 ADVANCED</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Feature cards
        st.markdown("""
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon">📈</div>
                    <div class="feature-title">Live Charts</div>
                    <div class="feature-desc">Interactive candlestick & line charts</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🎲</div>
                    <div class="feature-title">Simulations</div>
                    <div class="feature-desc">Advanced mathematical modeling</div>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">⚡</div>
                    <div class="feature-title">Real-time</div>
                    <div class="feature-desc">Instant parameter adjustments</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        # Form section title
        st.markdown('<div class="form-section-title">⚡ Get Started in Seconds</div>', unsafe_allow_html=True)
        
        # Closing container div (form will be inside)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Simple form with just name
        with st.form("welcome_form"):
            st.markdown('<div class="form-label">👤 Enter Your Name</div>', unsafe_allow_html=True)
            name = st.text_input("Name", label_visibility="collapsed", placeholder="Enter your name", key="name_input")
            
            st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
            submitted = st.form_submit_button("🚀 Start Exploring", width="stretch")
            
            if submitted and name:
                st.session_state.initialized = True
                st.session_state.user_name = name
                st.session_state.user_email = ""
                st.rerun()
        
        # Footer
        st.markdown("""
            <div class="welcome-footer">
                <p>💡 Analyze cryptocurrency price patterns with interactive mathematical simulations</p>
                <p style="margin-top: 10px; font-size: 0.85rem;">Powered by Advanced Analytics & Real-time Processing</p>
            </div>
        """, unsafe_allow_html=True)

# Main Application
else:
    # Header
    st.markdown(f"""
        <div class="app-header">
            <div>
                <div class="app-title">📊 Crypto Volatility Visualizer</div>
                <div class="app-subtitle">Real-time Data Analysis & Market Insights</div>
            </div>
            <div class="live-indicator">● LIVE</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Navigation Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Dashboard", "📈 Analysis", "⚖️ Compare", "📋 Data Explorer"])
    
    # Sidebar Controls
    with st.sidebar:
        st.markdown("""
            <div class="sidebar-title">⚙️ MARKET SIMULATION</div>
            <div class="sidebar-subtitle">Configure your analysis</div>
            <div class="spacer"></div>
        """, unsafe_allow_html=True)
        
        # Price Pattern
        st.markdown('<div class="form-label">📊 Price Pattern</div>', unsafe_allow_html=True)
        pattern = st.selectbox(
            "Price Pattern",
            ["Sine Wave (Smooth Cycles)", "Cosine Wave (Phase Shift)", "Combined Waves", "Realistic Behavior"],
            label_visibility="collapsed"
        )
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        
        # Amplitude
        st.markdown('<div class="form-label">💰 Amplitude ($)</div>', unsafe_allow_html=True)
        amplitude = st.slider(
            "Amplitude ($)",
            min_value=500,
            max_value=15000,
            value=5000,
            step=100,
            help="Low Swing ← → High Swing",
            label_visibility="collapsed"
        )
        st.markdown(f'<div style="text-align: center; color: #2dd4bf; font-weight: 600; margin-top: 5px;">${amplitude:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        
        # Frequency
        st.markdown('<div class="form-label">⚡ Frequency (Speed)</div>', unsafe_allow_html=True)
        frequency = st.slider(
            "Frequency (Speed)",
            min_value=1,
            max_value=20,
            value=3,
            step=1,
            help="Slow ← → Fast",
            label_visibility="collapsed"
        )
        st.markdown(f'<div style="text-align: center; color: #2dd4bf; font-weight: 600; margin-top: 5px;">{frequency}</div>', unsafe_allow_html=True)
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        
        # Drift
        st.markdown('<div class="form-label">📈 Drift (Trend)</div>', unsafe_allow_html=True)
        drift = st.slider(
            "Drift (Trend)",
            min_value=-200,
            max_value=200,
            value=50,
            step=10,
            help="Downtrend ← → Uptrend",
            label_visibility="collapsed"
        )
        st.markdown(f'<div style="text-align: center; color: #2dd4bf; font-weight: 600; margin-top: 5px;">{drift}</div>', unsafe_allow_html=True)
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        
        # Noise
        st.markdown('<div class="form-label">🎲 Noise (Randomness)</div>', unsafe_allow_html=True)
        noise = st.slider(
            "Noise (Randomness)",
            min_value=0,
            max_value=8000,
            value=1500,
            step=100,
            help="None ← → Max",
            label_visibility="collapsed"
        )
        st.markdown(f'<div style="text-align: center; color: #2dd4bf; font-weight: 600; margin-top: 5px;">${noise:,}</div>', unsafe_allow_html=True)
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        
        # Base Price
        st.markdown('<div class="form-label">💵 Base Price ($)</div>', unsafe_allow_html=True)
        base_price = st.slider(
            "Base Price ($)",
            min_value=10000,
            max_value=100000,
            value=45000,
            step=1000,
            help="10k ← → 100k",
            label_visibility="collapsed"
        )
        st.markdown(f'<div style="text-align: center; color: #2dd4bf; font-weight: 600; margin-top: 5px;">${base_price:,}</div>', unsafe_allow_html=True)
    
    # Generate Data
    days = 90
    dates, prices = simulate_price(days, base_price, amplitude, frequency, drift, noise, pattern)
    df = generate_ohlcv(dates, prices)
    st.session_state.generated_data = df
    
    # Calculate Metrics
    last_price = prices[-1]
    mean_price = np.mean(prices)
    std_dev = np.std(prices)
    avg_range = df['high'].sub(df['low']).mean()
    avg_volume = df['volume'].mean()
    
    # Dashboard Tab
    with tab1:
        # Metrics Row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Current Price</div>
                    <div class="metric-value">${int(last_price):,}</div>
                    <div class="metric-label">Close</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Volatility (σ)</div>
                    <div class="metric-value">${int(std_dev):,}</div>
                    <div class="metric-label">Std Dev</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Daily Range</div>
                    <div class="metric-value">${int(avg_range):,}</div>
                    <div class="metric-label">Avg H-L</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Trading Volume</div>
                    <div class="metric-value">{avg_volume/1000:.1f}K</div>
                    <div class="metric-label">Avg Daily</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        
        # Chart Type Selection
        chart_type = st.radio(
            "Chart Type",
            ["Candle", "Line", "Area"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Main OHLC Chart
        st.markdown('<div class="chart-title">📈 OHLC Candlestick Chart</div>', unsafe_allow_html=True)
        
        fig = go.Figure()
        
        if chart_type == "Candle":
            fig.add_trace(go.Candlestick(
                x=df['date'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'],
                increasing_line_color='#10b981',
                decreasing_line_color='#f87171'
            ))
        elif chart_type == "Area":
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['close'],
                mode='lines',
                fill='tozeroy',
                fillcolor='rgba(45,212,191,0.15)',
                line=dict(color='#2dd4bf', width=2.5)
            ))
        else:  # Line
            fig.add_trace(go.Scatter(
                x=df['date'],
                y=df['close'],
                mode='lines',
                line=dict(color='#2dd4bf', width=2.5, shape='spline')
            ))
        
        fig.update_layout(**get_plotly_layout(), height=360)
        st.plotly_chart(fig, width="stretch", config={'displayModeBar': False})
        
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        
        # Bottom Row: Volume + Returns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="chart-title">📊 Trading Volume Analysis</div>', unsafe_allow_html=True)
            
            volume_colors = ['rgba(16,185,129,0.7)' if i > 0 and df.iloc[i]['close'] > df.iloc[i-1]['close'] 
                           else 'rgba(248,113,113,0.7)' for i in range(len(df))]
            
            fig_vol = go.Figure()
            fig_vol.add_trace(go.Bar(
                x=df['date'],
                y=df['volume'],
                marker_color=volume_colors
            ))
            
            layout = get_plotly_layout()
            layout['yaxis'] = {'gridcolor': 'rgba(255,255,255,0.05)', 'linecolor': 'rgba(255,255,255,0.1)', 'title': {'text': 'Volume'}}
            fig_vol.update_layout(**layout, height=280)
            st.plotly_chart(fig_vol, width="stretch", config={'displayModeBar': False})
        
        with col2:
            st.markdown('<div class="chart-title">📉 Daily Returns Volatility</div>', unsafe_allow_html=True)
            
            returns = df['close'].pct_change() * 100
            returns = returns.dropna()
            ret_colors = ['rgba(16,185,129,0.7)' if r >= 0 else 'rgba(248,113,113,0.7)' for r in returns]
            
            fig_ret = go.Figure()
            fig_ret.add_trace(go.Bar(
                x=df['date'][1:],
                y=returns,
                marker_color=ret_colors
            ))
            
            layout = get_plotly_layout()
            layout['yaxis'] = {'gridcolor': 'rgba(255,255,255,0.05)', 'linecolor': 'rgba(255,255,255,0.1)', 
                              'ticksuffix': '%', 'title': {'text': 'Daily Return %'}}
            fig_ret.update_layout(**layout, height=280)
            st.plotly_chart(fig_ret, width="stretch", config={'displayModeBar': False})
    
    # Analysis Tab
    with tab2:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown('<div class="chart-title">📊 High vs Low Price Comparison</div>', unsafe_allow_html=True)
            
            fig_hl = go.Figure()
            fig_hl.add_trace(go.Scatter(
                x=df['date'],
                y=df['high'],
                mode='lines',
                name='High',
                line=dict(color='#10b981', width=2)
            ))
            fig_hl.add_trace(go.Scatter(
                x=df['date'],
                y=df['low'],
                mode='lines',
                name='Low',
                line=dict(color='#f87171', width=2),
                fill='tonexty',
                fillcolor='rgba(45,212,191,0.1)'
            ))
            
            layout = get_plotly_layout()
            layout['showlegend'] = True
            layout['legend'] = {'x': 0, 'y': 1.1, 'orientation': 'h'}
            fig_hl.update_layout(**layout, height=380)
            st.plotly_chart(fig_hl, width="stretch", config={'displayModeBar': False})
        
        with col2:
            st.markdown('<div class="chart-title">📈 Volatility Metrics</div>', unsafe_allow_html=True)
            
            max_price = df['close'].max()
            min_price = df['close'].min()
            avg_daily_change = returns.mean()
            sharpe = (avg_daily_change / (std_dev / np.sqrt(len(df['close'])))) if std_dev != 0 else 0
            
            vol_level = "HIGH" if std_dev > 2000 else "LOW"
            vol_class = "volatility-high" if vol_level == "HIGH" else "volatility-low"
            
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Max Price</div>
                    <div class="metric-value" style="font-size: 1.4rem;">${int(max_price):,}</div>
                </div>
                <div class="spacer"></div>
                <div class="metric-card">
                    <div class="metric-title">Min Price</div>
                    <div class="metric-value" style="font-size: 1.4rem;">${int(min_price):,}</div>
                </div>
                <div class="spacer"></div>
                <div class="metric-card">
                    <div class="metric-title">Volatility Level</div>
                    <div style="margin-top: 10px;"><span class="{vol_class}">{vol_level}</span></div>
                </div>
                <div class="spacer"></div>
                <div class="metric-card">
                    <div class="metric-title">Avg Daily Change</div>
                    <div class="metric-value" style="font-size: 1.4rem; color: {'#10b981' if avg_daily_change >= 0 else '#f87171'}">
                        {'+' if avg_daily_change >= 0 else ''}{avg_daily_change:.2f}%
                    </div>
                </div>
                <div class="spacer"></div>
                <div class="metric-card">
                    <div class="metric-title">Sharpe Ratio</div>
                    <div class="metric-value" style="font-size: 1.4rem;">{sharpe:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="spacer-lg"></div>', unsafe_allow_html=True)
        
        # Histogram
        st.markdown('<div class="chart-title">📊 Price Distribution & Density</div>', unsafe_allow_html=True)
        
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(
            x=df['close'],
            nbinsx=25,
            marker=dict(
                color='rgba(139,92,246,0.6)',
                line=dict(color='rgba(139,92,246,0.9)', width=1)
            )
        ))
        
        layout = get_plotly_layout()
        layout['xaxis']['tickprefix'] = '$'
        layout['yaxis'] = {'gridcolor': 'rgba(255,255,255,0.05)', 'linecolor': 'rgba(255,255,255,0.1)', 'title': {'text': 'Frequency'}}
        fig_hist.update_layout(**layout, height=300)
        st.plotly_chart(fig_hist, width="stretch", config={'displayModeBar': False})
    
    # Comparison Tab
    with tab3:
        st.markdown('<div class="chart-title">⚖️ Stable vs Volatile Asset Comparison</div>', unsafe_allow_html=True)
        st.markdown('<div style="text-align: center; color: #94a3b8; margin-bottom: 20px;">Side-by-side analysis of low-volatility vs high-volatility market behavior</div>', unsafe_allow_html=True)
        
        # Generate comparison data
        days_comp = 180
        stable_dates, stable_prices = simulate_price(days_comp, base_price, 500, 2, 20, 200, 'Sine Wave (Smooth Cycles)')
        volatile_dates, volatile_prices = simulate_price(days_comp, base_price, 8000, 5, 30, 5000, 'Realistic Behavior')
        
        fig_comp = go.Figure()
        
        fig_comp.add_trace(go.Scatter(
            x=stable_dates,
            y=stable_prices,
            mode='lines',
            name='Stable Asset',
            line=dict(color='#10b981', width=2.5)
        ))
        
        fig_comp.add_trace(go.Scatter(
            x=volatile_dates,
            y=volatile_prices,
            mode='lines',
            name='Volatile Asset',
            line=dict(color='#f87171', width=2.5)
        ))
        
        layout = get_plotly_layout()
        layout['showlegend'] = True
        layout['legend'] = {'x': 0, 'y': 1.1, 'orientation': 'h', 'bgcolor': 'rgba(0,0,0,0.3)'}
        fig_comp.update_layout(**layout, height=400)
        st.plotly_chart(fig_comp, width="stretch", config={'displayModeBar': False})
        
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        
        # Metrics
        col1, col2 = st.columns(2)
        
        stable_std = np.std(stable_prices)
        stable_swing = max(stable_prices) - min(stable_prices)
        stable_return = ((stable_prices[-1] - stable_prices[0]) / stable_prices[0]) * 100
        
        volatile_std = np.std(volatile_prices)
        volatile_swing = max(volatile_prices) - min(volatile_prices)
        volatile_return = ((volatile_prices[-1] - volatile_prices[0]) / volatile_prices[0]) * 100
        
        with col1:
            st.markdown(f"""
                <div class="metric-card" style="border-color: rgba(16,185,129,0.3);">
                    <div style="font-size: 1.3rem; font-weight: 700; color: #10b981; margin-bottom: 20px;">
                        🟢 Stable Asset (Low Volatility)
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div class="metric-title">Amplitude</div>
                        <div class="metric-value" style="font-size: 1.3rem;">$500</div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div class="metric-title">Std Dev</div>
                        <div class="metric-value" style="font-size: 1.3rem;">${int(stable_std):,}</div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div class="metric-title">Max Swing</div>
                        <div class="metric-value" style="font-size: 1.3rem;">${int(stable_swing):,}</div>
                    </div>
                    <div>
                        <div class="metric-title">Total Return</div>
                        <div class="metric-value" style="font-size: 1.3rem; color: {'#10b981' if stable_return >= 0 else '#f87171'}">
                            {'+' if stable_return >= 0 else ''}{stable_return:.2f}%
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-card" style="border-color: rgba(248,113,113,0.3);">
                    <div style="font-size: 1.3rem; font-weight: 700; color: #f87171; margin-bottom: 20px;">
                        🔴 Volatile Asset (High Volatility)
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div class="metric-title">Amplitude</div>
                        <div class="metric-value" style="font-size: 1.3rem;">$8,000</div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div class="metric-title">Std Dev</div>
                        <div class="metric-value" style="font-size: 1.3rem;">${int(volatile_std):,}</div>
                    </div>
                    <div style="margin-bottom: 12px;">
                        <div class="metric-title">Max Swing</div>
                        <div class="metric-value" style="font-size: 1.3rem;">${int(volatile_swing):,}</div>
                    </div>
                    <div>
                        <div class="metric-title">Total Return</div>
                        <div class="metric-value" style="font-size: 1.3rem; color: {'#10b981' if volatile_return >= 0 else '#f87171'}">
                            {'+' if volatile_return >= 0 else ''}{volatile_return:.2f}%
                        </div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
    
    # Data Explorer Tab
    with tab4:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown('<div class="chart-title">📋 OHLCV Dataset Explorer</div>', unsafe_allow_html=True)
            st.markdown('<div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px;">Real-time OHLCV data inspection with preprocessing applied</div>', unsafe_allow_html=True)
        
        with col2:
            # CSV Download
            csv = df.copy()
            csv['date'] = csv['date'].dt.strftime('%Y-%m-%d')
            csv_string = csv.to_csv(index=False)
            st.download_button(
                label="⬇ Download CSV",
                data=csv_string,
                file_name="crypto_ohlcv_data.csv",
                mime="text/csv"
            )
        
        # Data Summary
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        with col1:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Total Rows</div>
                    <div class="metric-value" style="font-size: 1.4rem;">{len(df)}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-title">Columns</div>
                    <div class="metric-value" style="font-size: 1.4rem;">6</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="metric-card">
                    <div class="metric-title">Missing Data</div>
                    <div class="metric-value" style="font-size: 1.4rem;">0</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Start Date</div>
                    <div class="metric-value" style="font-size: 1rem;">{df['date'].min().strftime('%Y-%m-%d')}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col5:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">End Date</div>
                    <div class="metric-value" style="font-size: 1rem;">{df['date'].max().strftime('%Y-%m-%d')}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col6:
            st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Avg Close</div>
                    <div class="metric-value" style="font-size: 1rem;">${int(df['close'].mean()):,}</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
        
        # Data Table
        display_df = df.copy()
        display_df['date'] = display_df['date'].dt.strftime('%Y-%m-%d')
        display_df['open'] = display_df['open'].apply(lambda x: f"${x:.2f}")
        display_df['high'] = display_df['high'].apply(lambda x: f"${x:.2f}")
        display_df['low'] = display_df['low'].apply(lambda x: f"${x:.2f}")
        display_df['close'] = display_df['close'].apply(lambda x: f"${x:.2f}")
        display_df.columns = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
        
        st.dataframe(
            display_df,
            width="stretch",
            height=500,
            hide_index=True
        )
    
    # Footer
    st.markdown("""
        <div class="app-footer">
            <div style="font-size: 1.1rem; font-weight: 600; color: #2dd4bf; margin-bottom: 10px;">
                📊 Crypto Volatility Visualizer
            </div>
            <div>Real-time Data Analysis & Market Insights | Powered by Advanced Analytics</div>
        </div>
    """, unsafe_allow_html=True)
