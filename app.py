Ah, I see exactly what happened!

The error popped up because the introductory text from my previous message ("Here is the complete, mobile-optimized code...") was accidentally copied into your `app.py` file along with the code itself. Python tried to read my conversational greeting as a command and got confused.

To fix this, completely clear your `app.py` file and paste **only** the code block below.

```python
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
         border-left: 4px solid #7ab8d4; padding-left: 8px; margin-top: 1.5rem !important; }
    h3 { font-size: 0.9rem !important; font-weight: 600 !important; color: #0a2a42 !important; margin: 1rem 0 0.4rem !important; }
    
    /* Input styling */
    .stNumberInput label, .stSelectbox label { font-size: 0.85rem !important; color: #03223a !important; font-weight: 500 !important; }
    div[data-baseweb="input"] > div, div[data-baseweb="select"] > div {
        background: #ffffff !important; 
        border: 1px solid #7ab8d4 !important;
        border-radius: 6px !important; 
    }
    input, .stSelectbox div { font-size: 0.95rem !important; color: #03223a !important; }

    /* Result cards */
    .result-card {
        background: #ffffff; border: 1px solid #7ab8d4;
        border-radius: 8px; padding: 0.7rem 1rem; margin: 0.4rem 0;
        display: flex; justify-content: space-between; align-items: center;
    }
    .result-label { font-size: 0.82rem; color: #0a2a42; font-weight: 500; }
    .result-value { font-size: 1.1rem; font-weight: 700; color: #03223a; }
    .result-unit  { font-size: 0.75rem; color: #7ab8d4; margin-left: 4px; }
    
    /* Scrollable Reference Tables for narrow screens */
    .ref-section { 
        background: #f0f8fc; border-radius: 8px; padding: 0.6rem 0.8rem; margin-top: 0.5rem; 
        overflow-x: auto; -webkit-overflow-scrolling: touch;
    }
    table { width: 100%; border-collapse: collapse; font-size: 0.8rem; }
    th { background: #e8f4fa; color: #03223a; font-weight: 600; padding: 6px 8px; text-align: left; border-bottom: 1px solid #7ab8d4; white-space: nowrap; }
    td { padding: 5px 8px; color: #0a2a42; border-bottom: 0.5px solid #d0e8f2; white-space: nowrap; }
    tr:last-child td { border-bottom: none; }
    
    /* Misc */
    .stExpander { border: 1px solid #7ab8d4 !important; border-radius: 8px !important; background-color: #ffffff; }
    .divider { border: none; border-top: 1px solid #d0e8f2; margin: 1.2rem 0 0.8rem; }
    .sub-note { font-size: 0.75rem; color: #5a8fa8; margin: 0.2rem 0 1rem; }
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

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── INPUTS ──────────────────────────────────────────────────────────
st.markdown("## System Inputs")

col1, col2 = st.columns(2)
with col1:
    hv_kv      = st.selectbox("HV source voltage (kV)", options=[33.0, 66.0, 110.0, 132.0, 220.0, 400.0], index=2)
    lv_kv      = st.selectbox("LV system voltage (kV)", options=[11.0, 22.0, 33.0, 66.0], index=2)
    load_mva   = st.number_input("Total load demand (MVA)", value=40.0, step=1.0, min_value=0.1)
with col2:
    source_mva = st.number_input("Source short-circuit (MVA)", value=1000.0, step=100.0, min_value=10.0)
    n_working  = st.number_input("Working transformers", value=1, step=1, min_value=1)

# ── CALCULATIONS ────────────────────────────────────────────────────
SQRT3 = math.sqrt(3)

tr_mva_required = load_mva / n_working

hv_fl_current = (tr_mva_required * 1000) / (SQRT3 * hv_kv)
lv_fl_current = (tr_mva_required * 1000) / (SQRT3 * lv_kv)

fault_ka_hv   = (source_mva * 1000) / (SQRT3 * hv_kv)
fault_ka_lv   = (source_mva * 1000) / (SQRT3 * lv_kv)

CB_CURRENTS  = [630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000]
CB_BREAKING  = [16, 20, 25, 31.5, 40, 50, 63]
CT_RATIOS    = [200, 300, 400, 600, 800, 1000, 1200, 1500, 2000, 2500, 3000, 4000]

def next_standard(val, std_list):
    for s in std_list:
        if s >= val:
            return s
    return std_list[-1]

hv_cb_current  = next_standard(hv_fl_current, CB_CURRENTS)
lv_cb_current  = next_standard(lv_fl_current, CB_CURRENTS)
hv_cb_breaking = next_standard(fault_ka_hv,   CB_BREAKING)
lv_cb_breaking = next_standard(fault_ka_lv,   CB_BREAKING)
hv_ct_ratio    = next_standard(hv_fl_current, CT_RATIOS)
lv_ct_ratio    = next_standard(lv_fl_current, CT_RATIOS)

def result_row(label, value, unit):
    st.markdown(f"""
    <div class="result-card">
        <span class="result-label">{label}</span>
        <span>
            <span class="result-value">{value}</span>
            <span class="result-unit">{unit}</span>
        </span>
    </div>""", unsafe_allow_html=True)

# ── RESULTS ─────────────────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown("## Results")

st.markdown("### Transformer")
result_row("Required rating (each)", f"{tr_mva_required:.1f}", "MVA")

st.markdown("### HV Side")
result_row("Full-load current", f"{hv_fl_current:.1f}", "A")
result_row("Fault current (3φ)", f"{fault_ka_hv:.2f}", "kA")
result_row("Recommended CB current", f"{hv_cb_current}", "A")
result_row("Recommended CB breaking", f"{hv_cb_breaking}", "kA")
result_row("Recommended CT ratio", f"{hv_ct_ratio} / 1", "A")

st.markdown("### LV Side")
result_row("Full-load current", f"{lv_fl_current:.1f}", "A")
result_row("Fault current (3φ)", f"{fault_ka_lv:.2f}", "kA")
result_row("Recommended CB current", f"{lv_cb_current}", "A")
result_row("Recommended CB breaking", f"{lv_cb_breaking}", "kA")
result_row("Recommended CT ratio", f"{lv_ct_ratio} / 1", "A")

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── QUICK SUMMARY FOR MEETING NOTES ─────────────────────────────────
st.markdown("### 📝 Quick Summary")
st.info(
    f"**Load:** {load_mva} MVA | **Transformers:** {n_working} × {tr_mva_required:.1f} MVA\n\n"
    f"**HV ({hv_kv} kV):** {hv_cb_current} A CB, {hv_cb_breaking} kA Breaking\n\n"
    f"**LV ({lv_kv} kV):** {lv_cb_current} A CB, {lv_cb_breaking} kA Breaking"
)

st.markdown('<p class="sub-note" style="text-align: center; margin-top: 1rem;">Fault MVA and CB requirements are based directly on the Source MVA input.<br>For preliminary review use only.</p>', unsafe_allow_html=True)

```
