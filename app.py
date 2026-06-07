import streamlit as st
import math

st.set_page_config(page_title="Substation Calculator", page_icon="⚡", layout="centered")

st.markdown("""
<style>
    /* Lock background to off-white to protect styling from system Dark Mode */
    .stApp { background-color: #f4f8fb; }
    
    /* Mobile-rigid container with shadow */
    .block-container { 
        padding: 1.5rem 1rem 2.5rem; 
        max-width: 480px; 
        margin: auto; 
        background-color: #ffffff; 
        box-shadow: 0px 4px 12px rgba(0,0,0,0.05);
        border-radius: 0 0 12px 12px;
    }
    
    h1 { font-size: 1.3rem !important; font-weight: 700 !important; color: #03223a !important; margin-bottom: 0 !important; }
    h2 { font-size: 1.05rem !important; font-weight: 600 !important; color: #0a2a42 !important;
         border-left: 4px solid #7ab8d4; padding-left: 8px; margin-top: 1.2rem !important; }
    h3 { font-size: 0.9rem !important; font-weight: 600 !important; color: #0a2a42 !important; margin: 1rem 0 0.4rem !important; }
    
    /* Input styling */
    .stNumberInput label { font-size: 0.85rem !important; color: #03223a !important; font-weight: 500 !important; }
    div[data-baseweb="input"] > div {
        background: #ffffff !important; 
        border: 1px solid #7ab8d4 !important;
        border-radius: 6px !important; 
    }
    input { font-size: 0.95rem !important; color: #03223a !important; }

    /* Result cards - compact */
    .result-card {
        background: #ffffff; border: 1px solid #7ab8d4;
        border-radius: 6px; padding: 0.6rem 0.8rem; margin: 0.4rem 0;
        display: flex; justify-content: space-between; align-items: center;
    }
    .result-label { font-size: 0.82rem; color: #0a2a42; font-weight: 500; }
    .result-value { font-size: 1.1rem; font-weight: 700; color: #03223a; }
    .result-unit  { font-size: 0.75rem; color: #7ab8d4; margin-left: 3px; }
    
    /* Scrollable Reference Tables */
    .ref-section { 
        background: #f0f8fc; border-radius: 8px; padding: 0.6rem 0.8rem; margin-top: 0.5rem; 
        overflow-x: auto; -webkit-overflow-scrolling: touch;
    }
    table { width: 100%; border-collapse: collapse; font-size: 0.75rem; }
    th { background: #e8f4fa; color: #03223a; font-weight: 600; padding: 5px 6px; text-align: left; border-bottom: 1px solid #7ab8d4; white-space: nowrap; }
    td { padding: 4px 6px; color: #0a2a42; border-bottom: 0.5px solid #d0e8f2; white-space: nowrap; }
    tr:last-child td { border-bottom: none; }
    
    /* Misc */
    .stExpander { border: 1px solid #7ab8d4 !important; border-radius: 8px !important; background-color: #ffffff; }
    .divider { border: none; border-top: 1px solid #d0e8f2; margin: 1.5rem 0 1rem; }
    .sub-note { font-size: 0.75rem; color: #5a8fa8; margin: 0.2rem 0 1rem; }
    .prompt-msg { font-size: 0.85rem; color: #f57f17; background: #fff8e1; padding: 0.8rem; border-radius: 8px; border: 1px solid #f9a825; text-align: center; margin-top: 1rem; font-weight: 500; }
    
    /* Formula boxes */
    .formula-box { background: #f9fbfe; border: 1px dashed #7ab8d4; padding: 0.8rem; border-radius: 6px; font-size: 0.85rem; color: #0a2a42; margin-bottom: 0.8rem; }
    .formula-title { font-weight: 700; color: #03223a; margin-bottom: 0.4rem; font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

st.markdown("# ⚡ Substation Design Calculator")
st.markdown('<p class="sub-note">Primary system — EHV/HV · Preliminary sizing</p>', unsafe_allow_html=True)

# ── REFERENCE TABLES ────────────────────────────────────────────────
with st.expander("📋 Conductor & Equipment Reference"):
    st.markdown('<div class="ref-section">', unsafe_allow_html=True)

    st.markdown("### Overhead line conductors (ACSR)")
    st.markdown("""
<table>
<tr><th>Conductor</th><th>Rating (A)</th><th>Voltage level</th></tr>
<tr><td>Weasel</td><td>175</td><td>11 / 33 kV</td></tr>
<tr><td>Rabbit</td><td>245</td><td>33 kV</td></tr>
<tr><td>Dog</td><td>261</td><td>33 / 66 kV</td></tr>
<tr><td>Lynx</td><td>340</td><td>66 / 110 kV</td></tr>
<tr><td>Panther</td><td>385</td><td>110 kV</td></tr>
<tr><td>Wolf</td><td>415</td><td>110 / 132 kV</td></tr>
<tr><td>Zebra</td><td>550</td><td>110 / 132 / 220 kV</td></tr>
<tr><td>Moose</td><td>655</td><td>220 / 400 kV</td></tr>
<tr><td>Bersfort</td><td>800</td><td>400 kV</td></tr>
<tr><td>Twin Moose</td><td>1300</td><td>400 kV</td></tr>
</table>
""", unsafe_allow_html=True)

    st.markdown("### Copper busbar (indoor / GIS)")
    st.markdown("""
<table>
<tr><th>Size (mm)</th><th>Rating (A)</th><th>Voltage level</th></tr>
<tr><td>50 × 6</td><td>630</td><td>11 kV</td></tr>
<tr><td>63 × 6</td><td>800</td><td>11 kV</td></tr>
<tr><td>80 × 8</td><td>1250</td><td>11 / 33 kV</td></tr>
<tr><td>100 × 10</td><td>1600</td><td>33 kV</td></tr>
<tr><td>120 × 10</td><td>2000</td><td>33 kV</td></tr>
<tr><td>160 × 10</td><td>2500</td><td>33 kV</td></tr>
<tr><td>200 × 12</td><td>3150</td><td>33 / 110 kV GIS</td></tr>
</table>
""", unsafe_allow_html=True)

    st.markdown("### Circuit breaker — standard ratings (IEC 62271)")
    st.markdown("""
<table>
<tr><th>Voltage</th><th>Current (A)</th><th>Breaking (kA)</th></tr>
<tr><td>11 kV</td><td>630 / 1250</td><td>25 / 31.5</td></tr>
<tr><td>33 kV</td><td>1250 / 2000</td><td>25 / 31.5 / 40</td></tr>
<tr><td>110 kV</td><td>1250 / 2000 / 3150</td><td>31.5 / 40</td></tr>
<tr><td>230 kV</td><td>1250 / 2000 / 3150</td><td>40 / 50</td></tr>
</table>
""", unsafe_allow_html=True)

    st.markdown("### CT primary ratios — standard (IEC 61869-2)")
    st.markdown("""
<table>
<tr><th>Voltage</th><th>Standard primary current (A)</th></tr>
<tr><td>11 / 33 kV</td><td>200, 300, 400, 600, 800, 1000, 1200, 1500, 2000</td></tr>
<tr><td>110 / 230 kV</td><td>200, 400, 600, 800, 1000, 1200, 1500, 2000, 2500</td></tr>
</table>
""", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider" style="margin-top: 0.5rem;">', unsafe_allow_html=True)

# ── INPUTS ──────────────────────────────────────────────────────────
st.markdown("## System Inputs")

with st.form("input_form", border=False):
    col1, col2 = st.columns(2)
    with col1:
        hv_kv    = st.number_input("HV system voltage (kV)", value=None, min_value=1.0, placeholder="e.g., 110.0")
        lv_kv    = st.number_input("LV system voltage (kV)", value=None, min_value=1.0, placeholder="e.g., 33.0")
        tr_mva   = st.number_input("Transformer rating (MVA)", value=None, min_value=0.1, placeholder="e.g., 40.0")
    with col2:
        hv_fault_ka = st.number_input("HV Max Fault (kA)", value=None, min_value=1.0, placeholder="e.g., 40.0")
        lv_fault_ka = st.number_input("LV Max Fault (kA)", value=None, min_value=1.0, placeholder="e.g., 25.0")
        
    st.markdown('<br>', unsafe_allow_html=True)
    submitted = st.form_submit_button("⚡ Calculate Results", type="primary", use_container_width=True)

# ── CONDITIONAL EXECUTION ───────────────────────────────────────────
if submitted:
    if hv_kv and lv_kv and tr_mva and hv_fault_ka and lv_fault_ka:

        # ── CALCULATIONS ────────────────────────────────────────────────
        SQRT3 = math.sqrt(3)

        hv_fl_current = (tr_mva * 1000) / (SQRT3 * hv_kv)
        lv_fl_current = (tr_mva * 1000) / (SQRT3 * lv_kv)
        
        hv_source_mva = SQRT3 * hv_kv * hv_fault_ka
        lv_source_mva = SQRT3 * lv_kv * lv_fault_ka

        def result_row(label, value, unit, subtext=None):
            sub_html = f'<div style="font-size: 0.65rem; color: #5a8fa8; margin-top: -2px;">{subtext}</div>' if subtext else ''
            html_str = f'<div class="result-card"><div><div class="result-label">{label}</div>{sub_html}</div><span><span class="result-value">{value}</span><span class="result-unit">{unit}</span></span></div>'
            st.markdown(html_str, unsafe_allow_html=True)

        # ── RESULTS ─────────────────────────────────────────────────────
        st.markdown('<hr class="divider">', unsafe_allow_html=True)
        st.markdown("## Results")
        
        result_row("Transformer base rating", f"{tr_mva:.1f}", "MVA")

        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.markdown("### HV Side")
            result_row("Full-load current", f"{hv_fl_current:.0f}", "A", "ONAN Base")

        with res_col2:
            st.markdown("### LV Side")
            result_row("Full-load current", f"{lv_fl_current:.0f}", "A", "ONAN Base")

        st.markdown('<hr class="divider">', unsafe_allow_html=True)

        # ── KEY FORMULAS ────────────────────────────────────────────────
        st.markdown("## 🧮 Key Formulas & Math")
        
        st.markdown("""
        <div class="formula-box">
            <div class="formula-title">1. Source Short-Circuit MVA</div>
            $$MVA_{SC} = \sqrt{3} \times V_{sys} \times I_{SC}$$
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"**HV:** $\\sqrt{{3}} \\times {hv_kv} \\times {hv_fault_ka} = $ **{hv_source_mva:.1f} MVA**")
        st.markdown(f"**LV:** $\\sqrt{{3}} \\times {lv_kv} \\times {lv_fault_ka} = $ **{lv_source_mva:.1f} MVA**")
        
        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("""
        <div class="formula-box">
            <div class="formula-title">2. Transformer Full-Load Current</div>
            $$I_{FL} = \frac{S_{TRF} \times 1000}{\sqrt{3} \times V_{sys}}$$
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**HV:** $({tr_mva} \\times 1000) / (\\sqrt{{3}} \\times {hv_kv}) = $ **{hv_fl_current:.0f} A**")
        st.markdown(f"**LV:** $({tr_mva} \\times 1000) / (\\sqrt{{3}} \\times {lv_kv}) = $ **{lv_fl_current:.0f} A**")

    else:
        st.markdown('<div class="prompt-msg">Please fill in all 5 system inputs above to generate sizing results.</div>', unsafe_allow_html=True)
