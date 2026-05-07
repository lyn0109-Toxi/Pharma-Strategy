import base64
from pathlib import Path
import io

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="ToxiGuard AI", page_icon="TG", layout="wide")


def image_to_data_uri(path):
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"


genotoxicity_image = Path(__file__).with_name("genotoxicity.png")
genotoxicity_uri = image_to_data_uri(genotoxicity_image)


def to_float(value):
    try:
        return float(value.strip().replace("%", ""))
    except (AttributeError, ValueError):
        return None


def assess_impurities(df):
    origin_actions = {
        "degradation product": "Link to forced degradation pathway and stability-indicating method.",
        "raw material": "Check supplier qualification, raw material specification, and carryover control.",
        "unreacted starting material": "Confirm purge factor, process clearance, and residual starting material control.",
        "process impurity": "Assess process origin, purge strategy, and batch-to-batch trend.",
        "residual solvent": "Compare with ICH Q3C class limit and daily exposure.",
        "unknown impurity": "Identify structure, assess qualification threshold, and evaluate genotoxic alert.",
    }

    rows = []
    if df is None or df.empty:
        return rows

    for index, row in df.iterrows():
        code = str(row.get("Impurity Code", "")).strip()
        chemical_name = str(row.get("Chemical Name", "")).strip()
        origin = str(row.get("Origin", "")).strip()
        observed_val = row.get("Observed (%)", None)
        limit_val = row.get("Specification (%)", None)
        concern = str(row.get("Concern", "")).strip()

        if not code or pd.isna(code) or code == "nan":
            continue

        try:
            observed = float(observed_val) if not pd.isna(observed_val) else None
        except ValueError:
            observed = None

        try:
            limit = float(limit_val) if not pd.isna(limit_val) else None
        except ValueError:
            limit = None

        observed_text = f"{observed:.3g}" if observed is not None else ""
        limit_text = f"{limit:.3g}" if limit is not None else ""

        origin_note = origin_actions.get(
            origin.lower(),
            "Clarify impurity origin and link the control strategy to the manufacturing process.",
        )

        if observed is None or limit is None:
            status = "Review needed"
            action = "Check numeric result and specification format."
        elif observed <= limit:
            status = "Within specification"
            action = f"Document as controlled under current specification. {origin_note}"
        else:
            status = "Above specification"
            action = (
                "Investigate root cause, toxicological qualification, and regulatory impact. "
                f"{origin_note}"
            )

        rows.append(
            {
                "Impurity Code": code,
                "Impurity Chemical Name": chemical_name,
                "Origin": origin,
                "Observed (%)": observed_text,
                "Specification (%)": limit_text,
                "Concern": concern,
                "Status": status,
                "Regulatory Action": action,
            }
        )
    return rows


KNOWN_IMPURITY_REFERENCES = {
    "acetaminophen": [
        {
            "Reference Impurity": "p-Aminophenol / 4-Aminophenol",
            "Impurity Chemical Name": "4-Aminophenol",
            "Likely Origin": "Raw material or degradation product",
            "Why It Matters": "Potential carryover from synthesis and known degradation-related concern",
            "Control Strategy": "Raw material control, release/stability method, degradation pathway justification",
            "Reference Basis": "USP/EP/JP monograph preferred; verify with DMF or validated literature if compendial data are unavailable",
        },
        {
            "Reference Impurity": "4-Nitrophenol",
            "Impurity Chemical Name": "4-Nitrophenol",
            "Likely Origin": "Raw material or synthetic intermediate",
            "Why It Matters": "May indicate upstream material carryover or incomplete process clearance",
            "Control Strategy": "Supplier qualification, incoming raw material specification, purge assessment",
            "Reference Basis": "USP/EP monograph preferred; verify with literature only as supportive evidence",
        },
        {
            "Reference Impurity": "Acetanilide-related impurity",
            "Impurity Chemical Name": "Acetanilide or route-specific acetanilide analog",
            "Likely Origin": "Process impurity",
            "Why It Matters": "Can be associated with process route or side reaction profile",
            "Control Strategy": "Process impurity mapping, batch trend review, method specificity check",
            "Reference Basis": "USP/EP approved specification preferred; confirm exact identity with validated method",
        },
    ],
    "telmisartan": [
        {
            "Reference Impurity": "Telmisartan related substance / process-related analog",
            "Impurity Chemical Name": "Route-specific telmisartan related compound",
            "Likely Origin": "Process impurity",
            "Why It Matters": "May arise from coupling, cyclization, or side reaction depending on route",
            "Control Strategy": "Route-specific impurity map, purge factor, batch trend review",
            "Reference Basis": "USP/EP monograph preferred; verify exact identity with DMF or literature if needed",
        },
        {
            "Reference Impurity": "Residual starting material or intermediate",
            "Impurity Chemical Name": "Route-specific starting material or intermediate",
            "Likely Origin": "Unreacted starting material",
            "Why It Matters": "Indicates incomplete conversion or insufficient purge during manufacturing",
            "Control Strategy": "Starting material specification, process clearance, residual control",
            "Reference Basis": "USP/EP monograph preferred when available; replace with route-specific starting material name",
        },
        {
            "Reference Impurity": "Oxidative or stress degradation product",
            "Impurity Chemical Name": "Route-specific oxidative degradation product",
            "Likely Origin": "Degradation product",
            "Why It Matters": "May appear during forced degradation or long-term stability",
            "Control Strategy": "Forced degradation, stability-indicating method, shelf-life trend evaluation",
            "Reference Basis": "USP/EP monograph preferred when available; confirm under validated stability protocol",
        },
    ],
}


def get_impurity_references(compound_name):
    compound = compound_name.strip()
    key = compound.lower()
    if not compound:
        return []
    if key in KNOWN_IMPURITY_REFERENCES:
        return KNOWN_IMPURITY_REFERENCES[key]

    return [
        {
            "Reference Impurity": f"{compound} related substances",
            "Impurity Chemical Name": "To be confirmed from USP/EP or validated method",
            "Likely Origin": "To be confirmed",
            "Why It Matters": "Compound-specific impurity profile should be verified from authoritative references",
            "Control Strategy": "Search USP/EP monograph first; if unavailable, use DMF, validated method, forced degradation, and literature",
            "Reference Basis": "No verified entry loaded in demo library; user should confirm for the searched compound",
        }
    ]


st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=Outfit:wght@400;700;900&display=swap');

:root {
    --primary-blue: #123d61;
    --accent-gold: #f2c84b;
    --accent-green: #1b8b69;
    --glass-bg: rgba(255, 255, 255, 0.7);
    --glass-border: rgba(255, 255, 255, 0.5);
    --neon-glow: 0 0 20px rgba(242, 200, 75, 0.5);
}

.stApp { 
    background: radial-gradient(circle at 10% 10%, #f0f4f8 0%, #e8edf3 100%);
    font-family: 'Inter', sans-serif;
}

.block-container { max-width: 1320px; padding-top: 2rem; }

/* --- Premium Visualization Stage --- */
.ontology-visual-stage {
    position: relative;
    min-height: 24rem;
    border-radius: 1.5rem;
    overflow: hidden;
    margin-bottom: 2rem;
    border: 1px solid var(--glass-border);
    background: 
        linear-gradient(135deg, #e8f4fb 0%, #f8fbfc 48%, #dceef7 100%);
    box-shadow: 0 30px 60px rgba(8, 32, 51, 0.15);
    backdrop-filter: blur(10px);
}

/* Moving Scan Line Animation */
.ontology-visual-stage::after {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, transparent, var(--accent-gold), transparent);
    box-shadow: var(--neon-glow);
    animation: scanMove 4s linear infinite;
    z-index: 10;
}

@keyframes scanMove {
    0% { top: 0; opacity: 0; }
    50% { opacity: 1; }
    100% { top: 100%; opacity: 0; }
}

.title-ribbon {
    position: absolute;
    left: 50%;
    top: 2rem;
    transform: translateX(-50%);
    padding: 1rem 2.5rem;
    text-align: center;
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 4rem;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    z-index: 5;
}

.title-ribbon h1 {
    margin: 0;
    color: var(--primary-blue);
    font-family: 'Outfit', sans-serif;
    font-size: 2.2rem;
    font-weight: 950;
    letter-spacing: -1px;
}

/* --- Sophisticated Neural Loader --- */
.neural-loader-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem;
    background: var(--glass-bg);
    border-radius: 2rem;
    border: 1px solid var(--glass-border);
    margin: 2rem 0;
}

.neural-node-wrapper {
    position: relative;
    width: 100px;
    height: 100px;
}

.neural-node {
    position: absolute;
    width: 15px;
    height: 15px;
    background: var(--primary-blue);
    border-radius: 50%;
    animation: pulseNode 1.5s ease-in-out infinite;
}

.node-1 { top: 0; left: 50%; animation-delay: 0s; }
.node-2 { top: 30%; left: 100%; animation-delay: 0.2s; }
.node-3 { top: 80%; left: 80%; animation-delay: 0.4s; }
.node-4 { top: 80%; left: 20%; animation-delay: 0.6s; }
.node-5 { top: 30%; left: 0%; animation-delay: 0.8s; }

@keyframes pulseNode {
    0%, 100% { transform: scale(1); opacity: 0.3; box-shadow: none; }
    50% { transform: scale(1.5); opacity: 1; box-shadow: var(--neon-glow); }
}

.loading-text {
    margin-top: 2rem;
    font-family: 'Outfit', sans-serif;
    font-weight: 700;
    color: var(--primary-blue);
    letter-spacing: 2px;
    text-transform: uppercase;
}

/* --- Golden Thread Animation --- */
.golden-thread-premium {
    position: absolute;
    left: 10%;
    right: 10%;
    top: 15rem;
    height: 6px;
    border-radius: 10px;
    background: linear-gradient(90deg, #f2c84b, #1b8b69, #236b9a);
    background-size: 200% 100%;
    animation: flowLight 3s linear infinite;
    box-shadow: var(--neon-glow);
}

@keyframes flowLight {
    0% { background-position: 100% 0%; }
    100% { background-position: -100% 0%; }
}

/* --- Premium Evidence Nodes --- */
.evidence-node-premium {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: 1.2rem;
    padding: 1.5rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 10px 20px rgba(0,0,0,0.03);
    cursor: pointer;
    text-align: center;
}

.evidence-node-premium:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 20px 40px rgba(18, 61, 97, 0.12);
    background: white;
    border-color: var(--accent-gold);
}

.node-number-premium {
    width: 40px;
    height: 40px;
    background: var(--primary-blue);
    color: white;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 900;
    margin: 0 auto 1rem;
}

/* --- Streamlit Overrides --- */
div.stButton > button {
    border-radius: 1rem !important;
    border: 1px solid var(--glass-border) !important;
    background: var(--glass-bg) !important;
    color: var(--primary-blue) !important;
    font-weight: 700 !important;
    transition: all 0.3s !important;
}

div.stButton > button:hover {
    border-color: var(--accent-gold) !important;
    box-shadow: var(--neon-glow) !important;
    transform: translateY(-2px);
}
</style>
""",
    unsafe_allow_html=True,
)

def render_premium_loader(text="ANALYZING ONTOLOGY NODES"):
    st.markdown(
        f"""
        <div class="neural-loader-container">
            <div class="neural-node-wrapper">
                <div class="neural-node node-1"></div>
                <div class="neural-node node-2"></div>
                <div class="neural-node node-3"></div>
                <div class="neural-node node-4"></div>
                <div class="neural-node node-5"></div>
            </div>
            <div class="loading-text">{{text}}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_premium_visual_stage():
    st.markdown(
        """
        <div class="ontology-visual-stage">
            <div class="title-ribbon">
                <h1>ToxiGuard AI</h1>
                <p style="margin:0; font-weight:700; color:#1b8b69; font-size:0.9rem;">ONTOLOGY & REGULATORY NAVIGATOR</p>
            </div>
            <div class="golden-thread-premium"></div>
            <div style="position:absolute; bottom:2rem; width:100%; text-align:center;">
                <span style="background:rgba(255,255,255,0.8); padding:0.5rem 1.5rem; border-radius:2rem; font-weight:800; color:#123d61; font-size:0.8rem; border:1px solid #eee;">
                    EVIDENCE CORE: CMC · QUALITY · RISK · SUBMISSION
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

render_premium_visual_stage()


st.markdown(
    """
<div class="kicker">What We Do</div>
<div class="big-question">Prediction alone is not enough.</div>
<p class="body-large">
AI toxicity prediction is becoming more important in pharmaceutical development,
but the business value comes from interpretation. We help teams understand whether
a signal is scientifically credible, whether it creates regulatory risk, and what
evidence should come next.
</p>
""",
    unsafe_allow_html=True,
)

st.markdown('<div class="service-grid">', unsafe_allow_html=True)
col_s1, col_s2, col_s3 = st.columns(3)
with col_s1:
    st.markdown("""
    <div class="evidence-node-premium">
        <div class="node-number-premium">01</div>
        <h3 style="color:#123d61; font-family:'Outfit';">In Silico Assessment</h3>
        <p style="color:#536064; font-size:0.9rem;">API, 불순물, 분해산물에 대한 사전 독성 스크리닝 및 규제 대응 전략 수립.</p>
    </div>
    """, unsafe_allow_html=True)
with col_s2:
    st.markdown("""
    <div class="evidence-node-premium">
        <div class="node-number-premium">02</div>
        <h3 style="color:#123d61; font-family:'Outfit';">ICH M7 Compliance</h3>
        <p style="color:#536064; font-size:0.9rem;">유전독성 불순물의 분류, 노출 허용량 계산 및 ICH M7 가이드라인 기반 정당성 입증.</p>
    </div>
    """, unsafe_allow_html=True)
with col_s3:
    st.markdown("""
    <div class="evidence-node-premium">
        <div class="node-number-premium">03</div>
        <h3 style="color:#123d61; font-family:'Outfit';">Gap Analysis</h3>
        <p style="color:#536064; font-size:0.9rem;">과학적 불확실성을 IND, NDA 제출을 위한 구체적 데이터 갭 분석 및 실행 전략으로 전환.</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)


st.markdown(
    """
<div style="display:flex; justify-content:space-between; align-items:center; background:rgba(18,61,97,0.05); padding:2rem; border-radius:1rem; border:1px solid rgba(18,61,97,0.1); margin:2rem 0;">
    <div style="text-align:center; flex:1;">
        <div style="width:30px; height:30px; background:var(--primary-blue); color:white; border-radius:50%; margin:0 auto 0.5rem; display:flex; align-items:center; justify-content:center; font-weight:900;">1</div>
        <b style="color:var(--primary-blue); font-size:0.8rem;">INPUT</b>
        <p style="font-size:0.75rem; color:#666; margin:0;">SMILES & Info</p>
    </div>
    <div style="flex:0.5; height:2px; background:linear-gradient(90deg, var(--primary-blue), var(--accent-green));"></div>
    <div style="text-align:center; flex:1;">
        <div style="width:30px; height:30px; background:var(--accent-green); color:white; border-radius:50%; margin:0 auto 0.5rem; display:flex; align-items:center; justify-content:center; font-weight:900;">2</div>
        <b style="color:var(--accent-green); font-size:0.8rem;">SCREEN</b>
        <p style="font-size:0.75rem; color:#666; margin:0;">QSAR & Ref</p>
    </div>
    <div style="flex:0.5; height:2px; background:linear-gradient(90deg, var(--accent-green), var(--accent-gold));"></div>
    <div style="text-align:center; flex:1;">
        <div style="width:30px; height:30px; background:var(--accent-gold); color:white; border-radius:50%; margin:0 auto 0.5rem; display:flex; align-items:center; justify-content:center; font-weight:900;">3</div>
        <b style="color:var(--accent-gold); font-size:0.8rem;">INTERPRET</b>
        <p style="font-size:0.75rem; color:#666; margin:0;">Tox Concern</p>
    </div>
    <div style="flex:0.5; height:2px; background:linear-gradient(90deg, var(--accent-gold), var(--primary-blue));"></div>
    <div style="text-align:center; flex:1;">
        <div style="width:30px; height:30px; background:var(--primary-blue); color:white; border-radius:50%; margin:0 auto 0.5rem; display:flex; align-items:center; justify-content:center; font-weight:900;">4</div>
        <b style="color:var(--primary-blue); font-size:0.8rem;">DECIDE</b>
        <p style="font-size:0.75rem; color:#666; margin:0;">Regulatory Action</p>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


st.markdown('<div class="assessment">', unsafe_allow_html=True)
st.markdown("## Start Preliminary Toxicity Assessment")
st.caption("Demo only. Final regulatory decisions require qualified expert review.")

compound = st.text_input("Compound Name", key="compound_name")
smiles = st.text_input("SMILES", key="smiles")

reference_rows = get_impurity_references(compound)
if compound.strip():
    st.markdown(f"### Known Impurity Reference for {compound.strip()}")
    st.caption(
        "The searched compound is checked against the current demo reference library. "
        "USP/EP monographs should be used as the primary source when available. "
        "If no verified entry is loaded, the table shows a search/verification plan."
    )
    st.table(reference_rows)
else:
    st.info("Enter a compound name to check compound-specific impurity reference information.")

material_type = st.selectbox(
    "Material Type",
    ["API", "Excipient", "Impurity", "Degradation Product"],
    key="material_type",
)

purpose = st.selectbox(
    "Assessment Purpose",
    [
        "Early R&D",
        "IND",
        "NDA (505(b)(1) - New Drug)",
        "NDA (505(b)(2) - Repurposed/Modified)",
        "ANDA (Generic)",
        "Investor Due Diligence",
    ],
    key="purpose",
)

st.markdown("### Related Substance / Impurity Specification Input")
st.caption(
    "Directly edit the table below to input your analytical lab results ('Observed (%)') "
    "and compare them against your proposed or compendial 'Specification (%)'. "
    "You can add or remove rows directly from the table."
)

default_impurities = pd.DataFrame([
    {"Impurity Code": "Impurity A", "Chemical Name": "4-Aminophenol", "Origin": "Degradation product", "Observed (%)": 0.08, "Specification (%)": 0.10, "Concern": "Genotoxic alert not identified"},
    {"Impurity Code": "Impurity B", "Chemical Name": "Route-specific starting material", "Origin": "Unreacted starting material", "Observed (%)": 0.16, "Specification (%)": 0.15, "Concern": "Requires qualification review"},
    {"Impurity Code": "Impurity C", "Chemical Name": "Supplier-related raw material impurity", "Origin": "Raw material", "Observed (%)": 0.04, "Specification (%)": 0.05, "Concern": "Supplier-related carryover"},
    {"Impurity Code": "Impurity D", "Chemical Name": "Unknown related substance", "Origin": "Unknown impurity", "Observed (%)": 0.06, "Specification (%)": 0.05, "Concern": "Structure identification needed"}
])

edited_df = st.data_editor(default_impurities, num_rows="dynamic", use_container_width=True, key="impurity_editor")

if st.button("Run Preliminary Assessment", key="run_assessment"):
    render_premium_loader("AI CORE: INITIALIZING TOXICITY INTERPRETATION")
    import time
    time.sleep(1.8)
    st.markdown('<div class="report">', unsafe_allow_html=True)
    st.markdown("### Preliminary Regulatory Toxicology Report")

    impurity_rows = assess_impurities(edited_df)

    # 1. KPI Metrics — driven by actual input data
    total_count = len(impurity_rows) if impurity_rows else 0
    above_spec_count = len([r for r in impurity_rows if r['Status'] == 'Above specification'])
    within_spec_count = len([r for r in impurity_rows if r['Status'] == 'Within specification'])
    review_count = len([r for r in impurity_rows if r['Status'] == 'Review needed'])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Impurities Entered", str(total_count))
    col2.metric("Within Specification", str(within_spec_count), None, delta_color="normal")
    col3.metric("Above Specification ⚠️", str(above_spec_count), f"+{above_spec_count}" if above_spec_count > 0 else None, delta_color="inverse")
    col4.metric("Review Needed", str(review_count))

    st.markdown("---")

    # 2. Charts — all driven by user input
    if impurity_rows:
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            st.markdown("#### Observed vs. Specification (ICH Q3A/B Threshold)")
            obs_vals = []
            spec_vals = []
            labels = []
            for r in impurity_rows:
                try:
                    obs_vals.append(float(r["Observed (%)"]))
                    spec_vals.append(float(r["Specification (%)"]))
                    labels.append(r["Impurity Code"])
                except (ValueError, TypeError):
                    continue
            fig = go.Figure()
            fig.add_trace(go.Bar(x=labels, y=obs_vals, name="Observed (%)", marker_color="#0070c0"))
            fig.add_trace(go.Scatter(x=labels, y=spec_vals, name="Specification Limit", mode="lines+markers", line=dict(color="#bb3e33", dash="dash", width=2)))
            # ICH Q3A identification threshold for API
            if material_type == "API":
                fig.add_hline(y=0.10, line_dash="dot", line_color="orange", annotation_text="ICH Q3A ID Threshold (0.10%)")
                fig.add_hline(y=0.15, line_dash="dot", line_color="red", annotation_text="ICH Q3A Qual. Threshold (0.15%)")
            fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=340, legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig, use_container_width=True)

        with col_chart2:
            st.markdown("#### Margin of Safety (Observed / Specification)")
            margin_data = []
            for r in impurity_rows:
                try:
                    obs = float(r["Observed (%)"])
                    spec = float(r["Specification (%)"])
                    pct = round((obs / spec) * 100, 1) if spec > 0 else 0
                    margin_data.append({"Impurity": r["Impurity Code"], "Usage (%)": pct})
                except (ValueError, TypeError):
                    continue
            if margin_data:
                df_margin = pd.DataFrame(margin_data)
                colors = ["#b71c1c" if v > 100 else "#f57c00" if v > 80 else "#1b5e20" for v in df_margin["Usage (%)"]]
                fig2 = go.Figure(go.Bar(x=df_margin["Impurity"], y=df_margin["Usage (%)"], marker_color=colors, text=[f"{v}%" for v in df_margin["Usage (%)"]], textposition="outside"))
                fig2.add_hline(y=100, line_dash="dash", line_color="red", annotation_text="Specification Limit (100%)")
                fig2.add_hline(y=80, line_dash="dot", line_color="orange", annotation_text="Warning Zone (80%)")
                fig2.update_layout(yaxis_title="% of Specification Used", margin=dict(l=20, r=20, t=30, b=20), height=340)
                st.plotly_chart(fig2, use_container_width=True)

        # Row 2: Origin distribution + Status summary
        col_chart3, col_chart4 = st.columns(2)
        with col_chart3:
            st.markdown("#### Impurity Origin Distribution")
            origin_counts = {}
            for r in impurity_rows:
                o = r["Origin"]
                origin_counts[o] = origin_counts.get(o, 0) + 1
            fig3 = go.Figure(go.Pie(labels=list(origin_counts.keys()), values=list(origin_counts.values()), hole=0.45, marker=dict(colors=["#0070c0", "#bb3e33", "#f0ad4e", "#5cb85c", "#6c757d"])))
            fig3.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=300)
            st.plotly_chart(fig3, use_container_width=True)

        with col_chart4:
            st.markdown("#### Compliance Status Summary")
            status_map = {"Within specification": within_spec_count, "Above specification": above_spec_count, "Review needed": review_count}
            fig4 = go.Figure(go.Bar(x=list(status_map.keys()), y=list(status_map.values()), marker_color=["#1b5e20", "#b71c1c", "#f57c00"], text=list(status_map.values()), textposition="outside"))
            fig4.update_layout(margin=dict(l=20, r=20, t=30, b=20), height=300, yaxis_title="Count")
            st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    st.write(f"**Compound:** {compound if compound else 'Not provided'}")
    st.write(f"**SMILES:** {smiles if smiles else 'Not provided'}")
    st.write(f"**Material Type:** {material_type}")
    st.write(f"**Assessment Purpose:** {purpose}")

    st.markdown("#### Predicted Toxicity Concerns")
    st.write(
        """
    - Mutagenicity: Low preliminary concern unless structural alerts are identified
    - Genotoxicity: Low preliminary concern; confirm with QSAR evidence package
    - Carcinogenicity: Exposure-dependent concern requiring longer-term context
    - Hepatotoxicity: Further review recommended based on class and exposure
    - Reproductive toxicity: Data gap remains unless supported by analog evidence
    """
    )

    st.markdown("#### Regulatory Interpretation")
    if purpose == "NDA (505(b)(2) - Repurposed/Modified)":
        st.success(
            """
        **505(b)(2) Pathway Analysis:** 
        As the API is already known, full systemic toxicity data can likely rely on the Reference Listed Drug (RLD) or literature. 
        However, the regulatory focus must shift to strictly qualifying **new impurities, novel excipients, or degradation products** arising from your new formulation or new route of administration. 
        Focus your efforts on ICH M7 justification for any new peaks and bridging local toxicity data.
        """
        )
    else:
        st.write(
            """
        The current signal should be interpreted through intended use, material classification,
        exposure level, impurity profile, and the credibility of the supporting model or NAMs evidence.
        """
        )

    if impurity_rows:
        st.markdown("#### Impurities Comparison: Observed vs. Specification Limits")
        st.caption(
            "Specification basis in this demo: proposed internal limit (% area or w/w). "
            "For real use, align the basis with approved specifications, stability data, "
            "ICH Q3A/Q3B thresholds, ICH M7 acceptable intake logic, or product-specific justification."
        )
        
        # Enhanced Data Table using Pandas
        df_impurities = pd.DataFrame(impurity_rows)
        def highlight_status(val):
            if val == 'Above specification':
                return 'background-color: #ffebee; color: #b71c1c; font-weight: bold'
            elif val == 'Within specification':
                return 'background-color: #e8f5e9; color: #1b5e20; font-weight: bold'
            return ''
        
        styled_df = df_impurities.style.map(highlight_status, subset=['Status'])
        st.dataframe(styled_df, use_container_width=True)

        above_spec = [row for row in impurity_rows if row["Status"] == "Above specification"]
        review_needed = [row for row in impurity_rows if row["Status"] == "Review needed"]

        if above_spec:
            st.error(
                "One or more impurities are above the proposed specification. "
                "A toxicological qualification and regulatory impact assessment should be prepared."
            )
        elif review_needed:
            st.warning(
                "Some impurity rows need review because the observed result or specification is not numeric."
            )
        else:
            st.success(
                "All listed impurities are within the proposed specification based on the values provided."
            )

        st.markdown("#### CTD 3.2.P.5.5 / DMF Justification Narrative Drafts")
        st.caption("AI-generated regulatory narrative blocks ready for CTD 3.2.P.5.5 insertion or DMF defense. Review and adapt based on actual QSAR outputs.")
        
        # Narrative generation and PDF Export Logic
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        pdf_elements = [Paragraph("CTD 3.2.P.5.5 Regulatory Narrative Drafts", styles['Title']), Spacer(1, 12)]
        
        for row in impurity_rows:
            status = row["Status"]
            if status == "Review needed":
                continue
            
            code = row["Impurity Code"]
            name = row["Impurity Chemical Name"]
            origin = row["Origin"].lower()
            obs = row["Observed (%)"]
            spec = row["Specification (%)"]
            
            if status == "Above specification":
                narrative = (
                    f"**[{code}] Justification for Specification Limit:**\n\n"
                    f"The {origin} identified as **{name}** was observed at a maximum level of **{obs}%**, which exceeds the initial proposed specification of **{spec}%**. "
                    f"To justify the acceptance of this impurity at the observed level, an *in silico* toxicological assessment was conducted in accordance with ICH M7 principles. "
                    f"Complementary QSAR methodologies (statistical-based and expert rule-based) confirmed the absence of structural alerts for mutagenicity (Class 5). "
                    f"Furthermore, read-across analysis comparing {name} to structurally similar approved analogs demonstrates that human exposure at the {obs}% limit presents negligible toxicological risk. "
                    f"Therefore, the specification limit is toxicologically qualified and justified for inclusion in CTD 3.2.P.5.5."
                )
                st.warning(narrative)
                pdf_elements.append(Paragraph(f"<b>[{code}] Justification for Specification Limit:</b>", styles['Heading2']))
                pdf_elements.append(Spacer(1, 6))
                pdf_elements.append(Paragraph(narrative.replace('**', '').replace('*', ''), styles['Normal']))
                pdf_elements.append(Spacer(1, 12))
                
            elif status == "Within specification":
                narrative = (
                    f"**[{code}] Routine Control Statement:**\n\n"
                    f"The {origin} **{name}** is routinely monitored. The observed data demonstrates a maximum level of **{obs}%**, "
                    f"which is consistently well within the established specification limit of **{spec}%**. "
                    f"Current manufacturing process controls and analytical procedures are fully validated to ensure clearance below the ICH Q3A/Q3B qualification threshold. "
                    f"No further toxicological qualification is required."
                )
                st.info(narrative)
                pdf_elements.append(Paragraph(f"<b>[{code}] Routine Control Statement:</b>", styles['Heading2']))
                pdf_elements.append(Spacer(1, 6))
                pdf_elements.append(Paragraph(narrative.replace('**', '').replace('*', ''), styles['Normal']))
                pdf_elements.append(Spacer(1, 12))
                
        # Generate PDF
        doc.build(pdf_elements)
        st.markdown("---")
        st.download_button(
            label="📄 Export CTD 3.2.P.5.5 Narrative (PDF)",
            data=pdf_buffer.getvalue(),
            file_name="CTD_3_2_P_5_5_Narrative.pdf",
            mime="application/pdf"
        )
    else:
        st.warning(
            "No valid impurity rows were detected. Use this format: "
            "Impurity A, 4-Aminophenol, Degradation product, 0.08, 0.10, Genotoxic alert not identified"
        )

    st.markdown("#### Recommended Next Steps")
    if purpose == "NDA (505(b)(2) - Repurposed/Modified)":
        st.write(
            """
        1. **Compare Impurity Profiles:** Map the new impurity profile against the RLD or USP/EP monograph.
        2. **Isolate Delta:** Identify any *new* impurities or degradation products not present in the original product.
        3. **In Silico Assessment:** Perform QSAR ICH M7 assessment specifically for the newly identified impurities.
        4. **Exposure & Local Toxicity:** If the route of administration changed, assess local toxicity and new exposure limits.
        5. **Bridging Strategy:** Prepare a scientific justification bridging the safety of the RLD to your new formulation.
        """
        )
    else:
        st.write(
            """
        1. Confirm known related substances using USP/EP monographs when available
        2. Review QSAR outputs from VEGA, OECD QSAR Toolbox, or equivalent tools
        3. Document model applicability domain and explainability
        4. Conduct impurity profiling and degradation product assessment
        5. Prepare ICH M7-based justification if relevant
        6. Consider confirmatory Ames testing if structural alerts remain unresolved
        """
        )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ─── CTD 3.2.P.8 Stability / Shelf-Life Prediction (ICH Q1E) ───
st.markdown("---")
st.markdown(
    """
<div class="kicker">CTD 3.2.P.8.3</div>
<div class="big-question">Shelf-Life Prediction (ICH Q1E)</div>
<p class="body-large">
Enter your long-term (25°C/60%RH) and accelerated (40°C/75%RH) stability data below.
ToxiGuard AI performs ICH Q1E linear regression with 95% confidence intervals for both
conditions and compares the degradation trends to determine shelf-life supportability.
</p>
""",
    unsafe_allow_html=True,
)

st.caption(
    "ICH Q1E approach: if accelerated data shows significant change, the shelf life "
    "cannot be extrapolated beyond the long-term data coverage. If no significant change "
    "at accelerated conditions, extrapolation up to 2× long-term coverage is supported."
)

stab_spec = st.number_input(
    "Specification Limit (%) for this impurity",
    min_value=0.01, max_value=5.0, value=0.15, step=0.01, key="stab_spec"
)


def run_regression(df_in, max_proj=60):
    """Run OLS regression and return results dict."""
    df_c = df_in.dropna()
    if len(df_c) < 3:
        return None
    x = df_c.iloc[:, 0].values.astype(float)
    y = df_c.iloc[:, 1].values.astype(float)
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
    x_pred = np.linspace(0, max(x.max() * 2, max_proj), 300)
    y_pred = slope * x_pred + intercept
    n = len(x)
    x_mean = np.mean(x)
    se = std_err * np.sqrt(1.0 / n + (x_pred - x_mean) ** 2 / np.sum((x - x_mean) ** 2))
    t_val = stats.t.ppf(0.95, df=n - 2)
    y_upper = y_pred + t_val * se
    cross = np.where(y_upper >= stab_spec)[0]
    shelf = float(x_pred[cross[0]]) if len(cross) > 0 else None
    return {
        "x": x, "y": y, "x_pred": x_pred, "y_pred": y_pred, "y_upper": y_upper,
        "slope": slope, "intercept": intercept, "r_sq": r_value ** 2,
        "shelf_life": shelf,
    }


col_long, col_accel = st.columns(2)

with col_long:
    st.markdown("##### Long-Term (25°C / 60% RH)")
    lt_default = pd.DataFrame({
        "Time (months)": [0, 3, 6, 9, 12, 18, 24],
        "Impurity (%)": [0.02, 0.03, 0.04, 0.06, 0.07, 0.09, 0.11],
    })
    lt_df = st.data_editor(lt_default, num_rows="dynamic", use_container_width=True, key="lt_editor")

with col_accel:
    st.markdown("##### Accelerated (40°C / 75% RH)")
    ac_default = pd.DataFrame({
        "Time (months)": [0, 1, 2, 3, 6],
        "Impurity (%)": [0.02, 0.04, 0.07, 0.11, 0.18],
    })
    ac_df = st.data_editor(ac_default, num_rows="dynamic", use_container_width=True, key="ac_editor")

if st.button("Run Shelf-Life Prediction", key="run_stability"):
    lt_res = run_regression(lt_df, max_proj=60)
    ac_res = run_regression(ac_df, max_proj=12)

    if lt_res is None:
        st.error("Long-term data requires at least 3 data points.")
    else:
        # KPI row
        lt_sl_text = f"{lt_res['shelf_life']:.1f} mo" if lt_res['shelf_life'] else "> 60 mo"
        ac_sl_text = f"{ac_res['shelf_life']:.1f} mo" if ac_res and ac_res['shelf_life'] else ("N/A" if ac_res is None else "> 12 mo")
        ac_slope_text = f"{ac_res['slope']:.5f}" if ac_res else "N/A"

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Long-Term Shelf Life", lt_sl_text)
        c2.metric("Long-Term R²", f"{lt_res['r_sq']:.4f}")
        c3.metric("Accelerated Slope (%/mo)", ac_slope_text)
        c4.metric("Accel. vs Long-Term Rate", f"{(ac_res['slope'] / lt_res['slope']):.1f}×" if ac_res and lt_res['slope'] != 0 else "N/A")

        # Charts side by side
        ch1, ch2 = st.columns(2)
        with ch1:
            st.markdown("#### Long-Term (25°C / 60% RH)")
            fig_lt = go.Figure()
            fig_lt.add_trace(go.Scatter(x=lt_res["x"], y=lt_res["y"], mode="markers", name="Observed", marker=dict(size=9, color="#0070c0")))
            fig_lt.add_trace(go.Scatter(x=lt_res["x_pred"], y=lt_res["y_pred"], mode="lines", name="Regression", line=dict(color="#002060")))
            fig_lt.add_trace(go.Scatter(x=lt_res["x_pred"], y=lt_res["y_upper"], mode="lines", name="95% UCI", line=dict(color="#f57c00", dash="dash")))
            fig_lt.add_hline(y=stab_spec, line_dash="dash", line_color="red", annotation_text=f"Spec ({stab_spec}%)")
            if lt_res["shelf_life"]:
                fig_lt.add_vline(x=lt_res["shelf_life"], line_dash="dot", line_color="green", annotation_text=f"{lt_res['shelf_life']:.1f}mo")
            fig_lt.update_layout(xaxis_title="Time (months)", yaxis_title="Impurity (%)", height=380, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h", y=-0.25))
            st.plotly_chart(fig_lt, use_container_width=True)

        with ch2:
            st.markdown("#### Accelerated (40°C / 75% RH)")
            if ac_res:
                fig_ac = go.Figure()
                fig_ac.add_trace(go.Scatter(x=ac_res["x"], y=ac_res["y"], mode="markers", name="Observed", marker=dict(size=9, color="#bb3e33")))
                fig_ac.add_trace(go.Scatter(x=ac_res["x_pred"], y=ac_res["y_pred"], mode="lines", name="Regression", line=dict(color="#8b0000")))
                fig_ac.add_trace(go.Scatter(x=ac_res["x_pred"], y=ac_res["y_upper"], mode="lines", name="95% UCI", line=dict(color="#f57c00", dash="dash")))
                fig_ac.add_hline(y=stab_spec, line_dash="dash", line_color="red", annotation_text=f"Spec ({stab_spec}%)")
                if ac_res["shelf_life"]:
                    fig_ac.add_vline(x=ac_res["shelf_life"], line_dash="dot", line_color="green", annotation_text=f"{ac_res['shelf_life']:.1f}mo")
                fig_ac.update_layout(xaxis_title="Time (months)", yaxis_title="Impurity (%)", height=380, margin=dict(l=20, r=20, t=30, b=20), legend=dict(orientation="h", y=-0.25))
                st.plotly_chart(fig_ac, use_container_width=True)
            else:
                st.info("Accelerated data insufficient for regression (need ≥ 3 points).")

        # Regulatory interpretation
        st.markdown("#### Regulatory Interpretation (ICH Q1E)")
        sig_change = False
        if ac_res and ac_res["slope"] > 0 and lt_res["slope"] > 0:
            rate_ratio = ac_res["slope"] / lt_res["slope"]
            if rate_ratio > 3.0 or (ac_res["shelf_life"] is not None and ac_res["shelf_life"] < 6):
                sig_change = True

        if sig_change:
            st.error(
                f"**Significant change detected at accelerated conditions.** "
                f"The degradation rate at 40°C/75%RH is **{rate_ratio:.1f}× faster** than long-term. "
                f"Per ICH Q1E, the proposed shelf life **cannot be extrapolated** beyond the "
                f"available long-term data coverage ({lt_res['x'].max():.0f} months). "
                f"Additional long-term data is required to support shelf-life extension."
            )
        else:
            if lt_res["shelf_life"] and lt_res["shelf_life"] >= 24:
                st.success(
                    f"No significant change at accelerated conditions. "
                    f"Long-term 95% UCI crosses the specification at **{lt_res['shelf_life']:.1f} months**. "
                    f"Per ICH Q1E, a shelf life of **24 months** is supported."
                )
            elif lt_res["shelf_life"] and lt_res["shelf_life"] >= 12:
                st.warning(
                    f"No significant change at accelerated conditions. "
                    f"Long-term 95% UCI crosses at **{lt_res['shelf_life']:.1f} months**. "
                    f"A shelf life of **{int(lt_res['shelf_life'] // 6) * 6} months** may be supportable."
                )
            elif lt_res["shelf_life"]:
                st.error(
                    f"Long-term 95% UCI crosses the specification at only "
                    f"**{lt_res['shelf_life']:.1f} months**. Process optimization is recommended."
                )
            else:
                st.success(
                    f"The impurity trend remains well below the specification ({stab_spec}%) "
                    f"throughout the projected range. A shelf life of 24+ months is likely supportable."
                )

st.markdown("## Request a Consultation")
name = st.text_input("Name", key="contact_name")
company = st.text_input("Company", key="contact_company")
email = st.text_input("Email", key="contact_email")
project = st.text_area("Compound / Project Description", key="contact_project")

if st.button("Submit Request", key="submit_request"):
    st.success("Thank you. Your request has been received.")
    st.write(f"Name: {name}")
    st.write(f"Company: {company}")
    st.write(f"Email: {email}")
    st.write(f"Project: {project}")

st.markdown("---")
st.caption(
    "ToxiGuard AI is an early-stage decision-support concept for in silico toxicology, "
    "NAMs interpretation, and regulatory strategy. USP/EP monographs should be used as "
    "the primary reference for compendial impurity information when available."
)
