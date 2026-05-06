import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="Pharma Tool Strategy",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="expanded",
)


NEEDS = [
    {
        "need": "CMC evidence structuring",
        "pressure": 95,
        "market_readiness": 90,
        "domain_fit": 95,
        "regulatory_basis": "FDA PQ/CMC, ICH M4Q, CTD Module 2.3 and Module 3",
        "buyer": "Regulatory CMC, Quality, RA, CMC writing teams",
        "pain": "CMC evidence is still trapped in documents, tables, PDFs, and reviewer narratives.",
        "tool": "CMC Evidence Graph",
        "why_now": "FDA is moving toward structured PQ/CMC submissions and computable CMC data.",
    },
    {
        "need": "Analytical method and specification intelligence",
        "pressure": 92,
        "market_readiness": 88,
        "domain_fit": 100,
        "regulatory_basis": "ICH Q2(R2), ICH Q14, ICH Q6A/Q6B, ICH Q1",
        "buyer": "QC, Analytical Development, QA, Regulatory CMC",
        "pain": "Specifications, test methods, validation evidence, and stability claims are hard to trace.",
        "tool": "Analytical Method Intelligence Tool",
        "why_now": "Q14 and Q2(R2) raise the bar for explaining why a method is fit for purpose.",
    },
    {
        "need": "Lifecycle change impact analysis",
        "pressure": 86,
        "market_readiness": 82,
        "domain_fit": 88,
        "regulatory_basis": "ICH Q9(R1), ICH Q10, ICH Q12",
        "buyer": "QA, Manufacturing Science, Regulatory CMC, Site Quality",
        "pain": "Post-approval changes are slow because impact across CQA, CPP, method, and stability is unclear.",
        "tool": "Quality Lifecycle Impact Analyzer",
        "why_now": "Regulators expect risk-based lifecycle control and stronger quality knowledge management.",
    },
    {
        "need": "NAMs regulatory evidence readiness",
        "pressure": 78,
        "market_readiness": 68,
        "domain_fit": 72,
        "regulatory_basis": "FDA NAMs draft guidance, FDA animal testing roadmap, ICH M3 and S-series",
        "buyer": "Nonclinical, Translational Science, Regulatory Strategy",
        "pain": "Sponsors need to justify when NAMs can support or replace animal evidence.",
        "tool": "NAMs Evidence Builder",
        "why_now": "FDA is actively encouraging human-relevant evidence and weight-of-evidence approaches.",
    },
    {
        "need": "AI model credibility documentation",
        "pressure": 75,
        "market_readiness": 70,
        "domain_fit": 76,
        "regulatory_basis": "FDA AI draft guidance, context of use, model risk, credibility assessment",
        "buyer": "Digital R&D, Regulatory Science, Data Science, Quality",
        "pain": "AI outputs cannot support decisions unless the model context, risk, and validation are documented.",
        "tool": "AI Credibility Documentation Module",
        "why_now": "AI is moving into regulatory decision support, but credibility evidence is still immature.",
    },
]


ROADMAP = [
    {
        "phase": "Phase 1",
        "title": "Analytical Method & Specification Intelligence",
        "timeline": "0-3 months",
        "output": "Upload method/specification documents, extract tests and criteria, map them to ICH Q2/Q14/Q6.",
    },
    {
        "phase": "Phase 2",
        "title": "CMC Evidence Graph",
        "timeline": "3-6 months",
        "output": "Connect drug substance, drug product, specifications, batch analysis, stability, and CTD sections.",
    },
    {
        "phase": "Phase 3",
        "title": "Lifecycle Change Impact",
        "timeline": "6-9 months",
        "output": "Identify impacted CQAs, methods, stability commitments, and regulatory documents after a change.",
    },
    {
        "phase": "Phase 4",
        "title": "Modernization Modules",
        "timeline": "9-12 months",
        "output": "Add NAMs evidence readiness and AI credibility documentation as advanced modules.",
    },
]


def score_row(row: dict) -> int:
    return round(
        row["pressure"] * 0.4
        + row["market_readiness"] * 0.3
        + row["domain_fit"] * 0.3
    )


def badge(label: str, tone: str = "green") -> str:
    colors = {
        "green": ("#e7f2ec", "#1f6f55"),
        "blue": ("#e8f1f8", "#236b9a"),
        "gold": ("#f4ecd9", "#9a6a1f"),
        "red": ("#f5e6e1", "#ad4f3f"),
        "dark": ("#182328", "#ffffff"),
    }
    bg, fg = colors[tone]
    return (
        f"<span style='background:{bg};color:{fg};padding:0.25rem 0.55rem;"
        f"border-radius:0.35rem;font-size:0.82rem;font-weight:700'>{label}</span>"
    )


def card(title: str, body: str, tag: str | None = None, tone: str = "green") -> None:
    tag_html = badge(tag, tone) if tag else ""
    st.markdown(
        f"""
        <div class="card">
            <div class="card-tag">{tag_html}</div>
            <h3>{title}</h3>
            <p>{body}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 2.2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }
    h1, h2, h3 {
        letter-spacing: 0;
    }
    .hero {
        border-left: 8px solid #2e715e;
        padding: 1.2rem 0 1.3rem 1.4rem;
        margin-bottom: 1.3rem;
    }
    .hero h1 {
        font-size: 3rem;
        line-height: 1.05;
        margin-bottom: 0.7rem;
    }
    .hero p {
        color: #5c6668;
        font-size: 1.2rem;
        max-width: 900px;
    }
    .card {
        border: 1px solid #ded7ca;
        background: #fffdf8;
        padding: 1.1rem 1.15rem;
        min-height: 205px;
        margin-bottom: 1rem;
    }
    .card h3 {
        font-size: 1.28rem;
        margin: 0.55rem 0 0.5rem 0;
    }
    .card p {
        color: #526063;
        font-size: 0.98rem;
        line-height: 1.45;
    }
    .metric-box {
        border: 1px solid #ded7ca;
        padding: 1rem;
        background: #fffdf8;
    }
    .small-muted {
        color: #687477;
        font-size: 0.94rem;
    }
    .decision {
        background: #172126;
        color: white;
        padding: 1.2rem 1.4rem;
        margin: 1rem 0;
    }
    .decision h3 {
        color: white;
        margin-top: 0;
    }
    .source {
        color: #667174;
        font-size: 0.85rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero">
        <h1>Pharma Tool Strategy</h1>
        <p>
        A decision dashboard for identifying where pharmaceutical companies need
        practical tools across CMC, quality, analytical methods, lifecycle control,
        NAMs, and AI credibility.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


with st.sidebar:
    st.header("Strategy Lens")
    selected_need = st.selectbox("Select a need area", [item["need"] for item in NEEDS])
    st.divider()
    st.caption("Scoring weights")
    pressure_weight = st.slider("Industry pressure", 0.0, 1.0, 0.40, 0.05)
    readiness_weight = st.slider("Market readiness", 0.0, 1.0, 0.30, 0.05)
    fit_weight = st.slider("Your domain fit", 0.0, 1.0, 0.30, 0.05)
    total = pressure_weight + readiness_weight + fit_weight
    st.caption("Weights are normalized automatically.")


df = pd.DataFrame(NEEDS)
df["strategy_score"] = df.apply(
    lambda r: round(
        r["pressure"] * pressure_weight / total
        + r["market_readiness"] * readiness_weight / total
        + r["domain_fit"] * fit_weight / total
    ),
    axis=1,
)
df = df.sort_values("strategy_score", ascending=False)


top = df.iloc[0]
col1, col2, col3 = st.columns(3)
col1.metric("Top opportunity", top["tool"])
col2.metric("Strategy score", f"{top['strategy_score']}/100")
col3.metric("Best first wedge", "Analytical + CMC")


st.markdown(
    """
    <div class="decision">
        <h3>Recommendation</h3>
        <p>
        Start with <b>Analytical Method & Specification Intelligence</b>,
        then expand into a <b>CMC Evidence Graph</b>. This is the best fit because
        the pain is concrete, the regulatory basis is clear, and the workflow is
        close to your analytical method and quality experience.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


st.subheader("Opportunity Ranking")
st.dataframe(
    df[
        [
            "need",
            "tool",
            "strategy_score",
            "pressure",
            "market_readiness",
            "domain_fit",
            "regulatory_basis",
        ]
    ],
    hide_index=True,
    use_container_width=True,
)


st.bar_chart(
    df.set_index("tool")[["pressure", "market_readiness", "domain_fit"]],
    height=360,
)


st.subheader("Need Areas")
cols = st.columns(2)
for idx, item in enumerate(NEEDS):
    with cols[idx % 2]:
        tone = ["green", "blue", "gold", "red", "dark"][idx]
        card(item["tool"], item["pain"], item["regulatory_basis"], tone)


selected = next(item for item in NEEDS if item["need"] == selected_need)
st.subheader("Selected Need Deep Dive")
left, right = st.columns([1, 1])

with left:
    st.markdown(f"### {selected['tool']}")
    st.write(selected["pain"])
    st.markdown("**Likely buyers**")
    st.write(selected["buyer"])
    st.markdown("**Why now**")
    st.write(selected["why_now"])

with right:
    st.markdown("### Regulatory rationale")
    st.info(selected["regulatory_basis"])
    st.markdown("### Initial product promise")
    st.write(
        "Convert fragmented regulatory and quality evidence into a traceable, "
        "queryable structure that helps teams explain why a method, specification, "
        "or control strategy is scientifically and regulatorily justified."
    )


st.subheader("Product Roadmap")
for item in ROADMAP:
    with st.expander(f"{item['phase']} · {item['title']} · {item['timeline']}", expanded=item["phase"] == "Phase 1"):
        st.write(item["output"])


st.subheader("MVP Feature Set")
mvp1, mvp2, mvp3 = st.columns(3)
with mvp1:
    card(
        "Document-to-Structure",
        "Extract tests, analytical procedures, acceptance criteria, validation items, and CTD locations from uploaded documents.",
        "MVP",
        "green",
    )
with mvp2:
    card(
        "Guideline Rationale Engine",
        "Map each extracted item to ICH Q2(R2), Q14, Q6, Q1, Q9, Q10, Q12, or FDA PQ/CMC rationale.",
        "Core",
        "blue",
    )
with mvp3:
    card(
        "Gap Report",
        "Generate a reviewer-style report showing missing validation evidence, weak specification linkage, and lifecycle risks.",
        "Output",
        "gold",
    )


st.subheader("Why this market is attractive")
st.markdown(
    """
    - The workflow is document-heavy, evidence-heavy, and difficult to manage manually.
    - FDA PQ/CMC is pushing CMC data toward structured, computable formats.
    - ICH Q14 and Q2(R2) make analytical method rationale more important.
    - QMM, Q9, Q10, and Q12 increase pressure for lifecycle quality knowledge management.
    - NAMs and AI credibility are emerging modules, but the first wedge should be CMC and analytical methods.
    """
)


st.subheader("Reference Basis")
st.markdown(
    """
    <p class="source">
    Basis: FDA PQ/CMC structured data initiative, FDA Quality Management Maturity,
    FDA AI draft guidance, FDA NAMs draft guidance and animal testing reduction roadmap,
    ICH Q1/Q2/Q6/Q8/Q9/Q10/Q12/Q14, and IQVIA R&D productivity trends.
    </p>
    """,
    unsafe_allow_html=True,
)
