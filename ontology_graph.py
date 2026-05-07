"""
ontology_graph.py
─────────────────
Drop-in replacement for the plain-text relationship-box in app.py.

Usage in app.py:
    from ontology_graph import render_ontology_graph
    render_ontology_graph(item)          # replaces the old st.markdown relationship-box
    render_full_ontology_graph()         # optional: full map on the landing / index page
"""

from __future__ import annotations
import json
import streamlit.components.v1 as components

# ── colour palette (matches your existing blue/teal/gold theme) ──────────────
CATEGORY_COLORS = {
    "entity":      {"bg": "#1a5f7a", "border": "#2d8bba", "font": "#ffffff"},
    "development": {"bg": "#0d5d49", "border": "#1b8b69", "font": "#ffffff"},
    "process":     {"bg": "#1a4a6b", "border": "#2a6fa8", "font": "#ffffff"},
    "quality":     {"bg": "#4a3060", "border": "#7b52ab", "font": "#ffffff"},
    "stability":   {"bg": "#1a5c3a", "border": "#2d8a5a", "font": "#ffffff"},
    "safety":      {"bg": "#6b3a1a", "border": "#c4622d", "font": "#ffffff"},
    "regulatory":  {"bg": "#2a4a6b", "border": "#4a7fa8", "font": "#ffffff"},
    "lifecycle":   {"bg": "#5a3a1a", "border": "#c4822d", "font": "#ffffff"},
    "modern":      {"bg": "#1a1a5a", "border": "#4a4aaa", "font": "#ffffff"},
    "default":     {"bg": "#2d4a5a", "border": "#4a7a9a", "font": "#ffffff"},
    "guideline":   {"bg": "#b8860b", "border": "#f2c84b", "font": "#1a1a1a"},
    "ctd":         {"bg": "#2f4858", "border": "#5a8fa8", "font": "#e0f0f8"},
}

EDGE_COLORS = {
    "primary":   "#f2c84b",
    "secondary": "#4a9aaa",
    "guideline": "#c4a020",
    "ctd":       "#5a8fa8",
}

# ── full graph data ──────────────────────────────────────────────────────────
# Each entry: (source_node, relation_label, target_node, edge_type)
# This is the complete cross-category ontology graph.
FULL_GRAPH_EDGES: list[tuple[str, str, str, str]] = [
    # Drug Entity
    ("DrugSubstance", "hasImpurity",       "Impurity",          "primary"),
    ("DrugSubstance", "hasCQA",            "CQA",               "primary"),
    ("DrugSubstance", "controlledBy",      "Specification",     "primary"),
    ("DrugSubstance", "documentedIn",      "DMF",               "ctd"),
    ("DrugProduct",   "hasCQA",            "CQA",               "primary"),
    ("DrugProduct",   "containsExcipient", "Excipient",         "primary"),
    ("DrugProduct",   "monitoredBy",       "StabilityStudy",    "primary"),
    ("DrugProduct",   "submittedIn",       "CTDModule3",        "ctd"),
    ("Excipient",     "hasFunctionalRole", "ExcipientRole",     "secondary"),
    ("Excipient",     "mayAffect",         "CQA",               "secondary"),
    ("DMF",           "referencedBy",      "DrugSubstance",     "ctd"),
    # Pharmaceutical Development
    ("QTPP",          "definesTargetFor",  "DrugProduct",       "primary"),
    ("QTPP",          "drivesSelectionOf", "CQA",               "primary"),
    ("CQA",           "testedBy",          "AnalyticalMethod",  "primary"),
    ("CQA",           "controlledBy",      "Specification",     "primary"),
    ("CQA",           "linkedTo",          "QTPP",              "primary"),
    ("CMA",           "mayImpact",         "CQA",               "primary"),
    ("CPP",           "affects",           "CQA",               "primary"),
    ("CMA",           "managedBy",         "ControlStrategy",   "secondary"),
    # Manufacturing
    ("UnitOperation", "hasParameter",      "CPP",               "primary"),
    ("UnitOperation", "generates",         "BatchRecord",       "secondary"),
    ("ProcessValidation", "verifies",      "UnitOperation",     "primary"),
    ("ProcessValidation", "supports",      "ControlStrategy",   "primary"),
    ("ContinuousProcess", "monitoredBy",   "PAT",               "primary"),
    ("ControlStrategy",   "documentedIn",  "CTDModule3",        "ctd"),
    # Quality
    ("Specification", "contains",          "TestItem",          "primary"),
    ("Specification", "definedBy",         "ICH Q6",            "guideline"),
    ("AnalyticalMethod", "validatedBy",    "MethodValidation",  "primary"),
    ("AnalyticalMethod", "developedPer",   "ICH Q14",           "guideline"),
    ("MethodValidation",  "supportedBy",   "ICH Q2(R2)",        "guideline"),
    ("Impurity",      "hasOrigin",         "ProcessStep",       "secondary"),
    ("Impurity",      "controlledBy",      "ControlStrategy",   "secondary"),
    # Stability
    ("StabilityStudy","monitors",          "CQA",               "primary"),
    ("StabilityStudy","supports",          "ShelfLife",         "primary"),
    ("StabilityStudy","conductedPer",      "ICH Q1",            "guideline"),
    ("ShelfLife",     "appearsIn",         "Labeling",          "secondary"),
    ("ShelfLife",     "supportedBy",       "StabilityData",     "primary"),
    # Safety & Efficacy
    ("NonclinicalStudy","supports",        "FirstInHumanDose",  "primary"),
    ("NonclinicalStudy","summarizedIn",    "CTDModule4",        "ctd"),
    ("NAMsModel",     "supportsDecision",  "NonclinicalStudy",  "primary"),
    ("NAMsModel",     "hasContextOfUse",   "RegulatoryQuestion","primary"),
    ("ClinicalStudy", "supports",          "BenefitRisk",       "primary"),
    ("ClinicalStudy", "summarizedIn",      "CTDModule5",        "ctd"),
    # Regulatory
    ("CTDModule3",    "summarizedIn",      "QOS",               "ctd"),
    ("DMF",           "authorizedBy",      "LOA",               "ctd"),
    # Risk & Lifecycle
    ("RiskAssessment","prioritizes",       "ControlAction",     "primary"),
    ("RiskAssessment","conductedPer",      "ICH Q9",            "guideline"),
    ("LifecycleChange","impacts",          "CQA",               "secondary"),
    ("LifecycleChange","managedBy",        "Q12Strategy",       "primary"),
    ("LifecycleChange","managedBy",        "ControlStrategy",   "primary"),
    # FDA Modernization
    ("CMCDataElement","mapsTo",            "CTDModule3",        "ctd"),
    ("AIModel",       "hasContextOfUse",   "QualityDecision",   "primary"),
    ("AIModel",       "assessedPer",       "ICH Q9",            "guideline"),
    ("WeightOfEvidence","integrates",      "NAMsModel",         "primary"),
]

# ── per-item subgraph definitions ────────────────────────────────────────────
ITEM_GRAPHS: dict[str, list[tuple[str, str, str, str]]] = {
    "Drug Substance / API": [
        ("DrugSubstance", "hasImpurity",    "Impurity",         "primary"),
        ("DrugSubstance", "hasCQA",         "CQA",              "primary"),
        ("DrugSubstance", "controlledBy",   "Specification",    "primary"),
        ("Specification", "testedBy",       "AnalyticalMethod", "primary"),
        ("DrugSubstance", "documentedIn",   "DMF",              "ctd"),
        ("DrugSubstance", "conductedPer",   "ICH Q11",          "guideline"),
        ("Impurity",      "controlledBy",   "ControlStrategy",  "secondary"),
    ],
    "Drug Product": [
        ("DrugProduct",  "hasCQA",          "CQA",              "primary"),
        ("CQA",          "controlledBy",    "Specification",    "primary"),
        ("Specification","monitoredBy",     "StabilityStudy",   "primary"),
        ("DrugProduct",  "containsExcipient","Excipient",       "secondary"),
        ("DrugProduct",  "conductedPer",    "ICH Q8",           "guideline"),
        ("DrugProduct",  "submittedIn",     "CTDModule3",       "ctd"),
    ],
    "Excipient": [
        ("Excipient",    "hasFunctionalRole","ExcipientRole",   "primary"),
        ("ExcipientRole","mayAffect",        "CQA",             "primary"),
        ("Excipient",    "riskAssessedBy",   "ICH Q9",          "guideline"),
        ("Excipient",    "documentedIn",     "CTD_3.2.P.4",     "ctd"),
    ],
    "QTPP": [
        ("QTPP",         "definesTargetFor", "DrugProduct",     "primary"),
        ("QTPP",         "drivesSelectionOf","CQA",             "primary"),
        ("CQA",          "linksClinicalTo",  "ControlStrategy", "secondary"),
        ("QTPP",         "conductedPer",     "ICH Q8",          "guideline"),
    ],
    "CQA": [
        ("CQA",          "testedBy",         "AnalyticalMethod","primary"),
        ("AnalyticalMethod","validatedBy",   "MethodValidation","primary"),
        ("CQA",          "controlledBy",     "Specification",   "primary"),
        ("CQA",          "monitoredBy",      "StabilityStudy",  "secondary"),
        ("CQA",          "conductedPer",     "ICH Q8",          "guideline"),
    ],
    "CMA / CPP": [
        ("CMA",          "mayImpact",        "CQA",             "primary"),
        ("CPP",          "affects",          "CQA",             "primary"),
        ("CMA",          "managedBy",        "ControlStrategy", "primary"),
        ("ControlStrategy","conductedPer",   "ICH Q8",          "guideline"),
        ("CPP",          "rankedBy",         "ICH Q9",          "guideline"),
    ],
    "Unit Operations": [
        ("UnitOperation","hasParameter",     "CPP",             "primary"),
        ("CPP",          "affects",          "CQA",             "primary"),
        ("UnitOperation","generates",        "BatchRecord",     "secondary"),
        ("UnitOperation","conductedPer",     "ICH Q10",         "guideline"),
    ],
    "Process Validation": [
        ("ProcessValidation","verifies",     "UnitOperation",   "primary"),
        ("ProcessValidation","supports",     "ControlStrategy", "primary"),
        ("ProcessValidation","documentedIn", "CTDModule3",      "ctd"),
        ("ProcessValidation","conductedPer", "ICH Q10",         "guideline"),
    ],
    "Continuous Manufacturing": [
        ("ContinuousProcess","monitoredBy",  "PAT",             "primary"),
        ("PAT",          "controlledBy",     "RealTimeControl", "primary"),
        ("ContinuousProcess","conductedPer", "ICH Q13",         "guideline"),
        ("ContinuousProcess","enables",      "ContinuousRelease","secondary"),
    ],
    "Specification": [
        ("Specification","contains",         "TestItem",        "primary"),
        ("TestItem",     "hasAcceptanceCriteria","Criterion",   "primary"),
        ("Specification","definedBy",        "ICH Q6",          "guideline"),
        ("Specification","submittedIn",      "CTDModule3",      "ctd"),
    ],
    "Analytical Method": [
        ("AnalyticalMethod","hasPurpose",    "ATP",             "primary"),
        ("AnalyticalMethod","validatedBy",   "MethodValidation","primary"),
        ("MethodValidation","conductedPer",  "ICH Q2(R2)",      "guideline"),
        ("AnalyticalMethod","developedPer",  "ICH Q14",         "guideline"),
    ],
    "Impurity Control": [
        ("Impurity",     "hasOrigin",        "ProcessStep",     "primary"),
        ("Impurity",     "controlledBy",     "ControlStrategy", "primary"),
        ("ControlStrategy","documentedIn",   "Specification",   "secondary"),
        ("Impurity",     "conductedPer",     "ICH Q3",          "guideline"),
    ],
    "Stability Study": [
        ("StabilityStudy","monitors",        "CQA",             "primary"),
        ("StabilityStudy","supports",        "ShelfLife",       "primary"),
        ("StabilityStudy","conductedPer",    "ICH Q1",          "guideline"),
        ("StabilityStudy","documentedIn",    "CTD_3.2.S.7",     "ctd"),
    ],
    "Shelf Life and Storage": [
        ("ShelfLife",    "supportedBy",      "StabilityData",   "primary"),
        ("ShelfLife",    "appearsIn",         "Labeling",        "secondary"),
        ("ShelfLife",    "conductedPer",      "ICH Q1",          "guideline"),
        ("ShelfLife",    "managedBy",         "ICH Q12",         "guideline"),
    ],
    "Nonclinical Evidence": [
        ("NonclinicalStudy","supports",      "FirstInHumanDose","primary"),
        ("NonclinicalStudy","summarizedIn",  "CTDModule4",      "ctd"),
        ("NonclinicalStudy","conductedPer",  "ICH M3",          "guideline"),
        ("NonclinicalStudy","conductedPer",  "ICH S-Series",    "guideline"),
    ],
    "Clinical Evidence": [
        ("ClinicalStudy","supports",         "BenefitRisk",     "primary"),
        ("ClinicalStudy","summarizedIn",     "CTDModule5",      "ctd"),
        ("ClinicalStudy","conductedPer",     "ICH E-Series",    "guideline"),
        ("BenefitRisk",  "supportsApproval", "RegulatoryDecision","secondary"),
    ],
    "CTD Module 3": [
        ("QualityEvidence","submittedIn",    "CTDModule3",      "ctd"),
        ("CTDModule3",   "summarizedIn",     "QOS",             "ctd"),
        ("CTDModule3",   "structuredBy",     "ICH M4",          "guideline"),
        ("CTDModule3",   "enabledBy",        "FDA PQ/CMC",      "guideline"),
    ],
    "DMF / Supplier Evidence": [
        ("SupplierEvidence","documentedIn",  "DMF",             "ctd"),
        ("DMF",          "referencedBy",     "Application",     "ctd"),
        ("DMF",          "authorizedBy",     "LOA",             "ctd"),
        ("DMF",          "conductedPer",     "ICH Q7",          "guideline"),
    ],
    "Quality Risk Management": [
        ("RiskAssessment","prioritizes",     "ControlAction",   "primary"),
        ("RiskAssessment","reviewedBy",      "QualitySystem",   "primary"),
        ("RiskAssessment","conductedPer",    "ICH Q9",          "guideline"),
        ("QualitySystem","conductedPer",     "ICH Q10",         "guideline"),
    ],
    "Lifecycle Change Management": [
        ("LifecycleChange","impacts",        "CQA",             "primary"),
        ("LifecycleChange","impacts",        "CPP",             "secondary"),
        ("LifecycleChange","managedBy",      "Q12Strategy",     "primary"),
        ("Q12Strategy",  "conductedPer",     "ICH Q12",         "guideline"),
    ],
    "PQ/CMC Structured Data": [
        ("CMCDataElement","mapsTo",          "CTDModule3",      "ctd"),
        ("CMCDataElement","supports",        "StructuredReview","primary"),
        ("CMCDataElement","enabledBy",       "FDA PQ/CMC",      "guideline"),
        ("StructuredReview","improves",      "RegulatoryDecision","secondary"),
    ],
    "NAMs Evidence": [
        ("NAMsModel",    "hasContextOfUse",  "RegulatoryQuestion","primary"),
        ("NAMsModel",    "integratedBy",     "WeightOfEvidence","primary"),
        ("WeightOfEvidence","supportsDecision","NonclinicalPackage","secondary"),
        ("NAMsModel",    "conductedPer",     "FDA NAMs",        "guideline"),
    ],
    "AI Credibility": [
        ("AIModel",      "hasContextOfUse",  "QualityDecision", "primary"),
        ("AIModel",      "hasCredibilityEvidence","ValidationPackage","primary"),
        ("ValidationPackage","assessedPer",  "FDA AI",          "guideline"),
        ("AIModel",      "riskAssessedBy",   "ICH Q9",          "guideline"),
    ],
}

# ── node category mapping (for colour) ──────────────────────────────────────
NODE_CATEGORY: dict[str, str] = {
    "DrugSubstance":       "entity",
    "DrugProduct":         "entity",
    "Excipient":           "entity",
    "ExcipientRole":       "entity",
    "DMF":                 "regulatory",
    "LOA":                 "regulatory",
    "QTPP":                "development",
    "CQA":                 "development",
    "CMA":                 "development",
    "CPP":                 "development",
    "ControlStrategy":     "development",
    "UnitOperation":       "process",
    "BatchRecord":         "process",
    "ProcessValidation":   "process",
    "ContinuousProcess":   "process",
    "PAT":                 "process",
    "RealTimeControl":     "process",
    "ContinuousRelease":   "process",
    "ProcessStep":         "process",
    "Specification":       "quality",
    "TestItem":            "quality",
    "Criterion":           "quality",
    "AnalyticalMethod":    "quality",
    "MethodValidation":    "quality",
    "ATP":                 "quality",
    "Impurity":            "quality",
    "StabilityStudy":      "stability",
    "ShelfLife":           "stability",
    "StabilityData":       "stability",
    "Labeling":            "stability",
    "NonclinicalStudy":    "safety",
    "FirstInHumanDose":    "safety",
    "ClinicalStudy":       "safety",
    "BenefitRisk":         "safety",
    "RegulatoryDecision":  "safety",
    "CTDModule3":          "regulatory",
    "CTDModule4":          "regulatory",
    "CTDModule5":          "regulatory",
    "QOS":                 "regulatory",
    "Application":         "regulatory",
    "CTD_3.2.S.7":         "regulatory",
    "CTD_3.2.P.4":         "regulatory",
    "QualityEvidence":     "regulatory",
    "SupplierEvidence":    "regulatory",
    "RiskAssessment":      "lifecycle",
    "ControlAction":       "lifecycle",
    "QualitySystem":       "lifecycle",
    "LifecycleChange":     "lifecycle",
    "Q12Strategy":         "lifecycle",
    "CMCDataElement":      "modern",
    "StructuredReview":    "modern",
    "NAMsModel":           "modern",
    "RegulatoryQuestion":  "modern",
    "WeightOfEvidence":    "modern",
    "NonclinicalPackage":  "modern",
    "AIModel":             "modern",
    "QualityDecision":     "modern",
    "ValidationPackage":   "modern",
    "FirstInHumanExposure":"safety",
}

def _node_style(label: str) -> dict:
    """Return vis.js node options for a label."""
    # Detect guideline nodes
    guideline_prefixes = ("ICH ", "FDA ")
    if any(label.startswith(p) for p in guideline_prefixes):
        c = CATEGORY_COLORS["guideline"]
        shape = "diamond"
        size = 22
    elif label.startswith("CTD") or label in ("QOS", "DMF", "LOA", "Application"):
        c = CATEGORY_COLORS["ctd"]
        shape = "box"
        size = 20
    else:
        cat = NODE_CATEGORY.get(label, "default")
        c = CATEGORY_COLORS[cat]
        shape = "ellipse"
        size = 28

    return {
        "color": {
            "background": c["bg"],
            "border":     c["border"],
            "highlight":  {"background": c["border"], "border": "#f2c84b"},
        },
        "font":  {"color": c["font"], "size": 13, "face": "Segoe UI, sans-serif"},
        "shape": shape,
        "size":  size,
    }


def _edge_style(edge_type: str) -> dict:
    color = EDGE_COLORS.get(edge_type, EDGE_COLORS["secondary"])
    return {
        "color":  {"color": color, "highlight": "#f2c84b"},
        "width":  2 if edge_type == "primary" else 1,
        "dashes": edge_type in ("ctd", "guideline"),
        "smooth": {"type": "curvedCW", "roundness": 0.2},
        "arrows": {"to": {"enabled": True, "scaleFactor": 0.7}},
    }


def _build_graph_data(edges: list[tuple[str, str, str, str]]) -> tuple[list, list]:
    """Convert edge list to vis.js nodes + edges JSON."""
    node_set: dict[str, dict] = {}
    vis_edges = []

    for src, rel, tgt, etype in edges:
        for label in (src, tgt):
            if label not in node_set:
                node_set[label] = {"id": label, "label": label, **_node_style(label)}

        vis_edges.append({
            "from":  src,
            "to":    tgt,
            "label": rel,
            "font":  {"size": 10, "color": "#aaccdd", "align": "middle"},
            **_edge_style(etype),
        })

    return list(node_set.values()), vis_edges


# ── public API ───────────────────────────────────────────────────────────────
def render_ontology_graph(item: str, height: int = 420) -> None:
    """Render an interactive subgraph for the selected ontology item."""
    edges = ITEM_GRAPHS.get(item, [
        ("OntologyItem", "alignedWith", "Guideline", "guideline"),
        ("Guideline",    "supportedBy", "Evidence",  "primary"),
    ])
    nodes, vis_edges = _build_graph_data(edges)
    _render_vis(nodes, vis_edges, height=height, title=f"Ontology graph: {item}")


def render_full_ontology_graph(height: int = 680) -> None:
    """Render the full cross-category ontology graph."""
    nodes, vis_edges = _build_graph_data(FULL_GRAPH_EDGES)
    _render_vis(nodes, vis_edges, height=height, title="Full Pharmaceutical Development Ontology",
                physics_solver="forceAtlas2Based")


def _render_vis(
    nodes: list,
    edges: list,
    height: int = 420,
    title: str = "",
    physics_solver: str = "barnesHut",
) -> None:
    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)

    html = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: transparent; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}

  #graph-wrap {{
    position: relative;
    width: 100%;
    height: {height}px;
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid #2d4a5a;
    background: linear-gradient(135deg, #0a1a26 0%, #0f2233 60%, #0a2040 100%);
  }}

  #graph-canvas {{
    width: 100%;
    height: 100%;
  }}

  #graph-title {{
    position: absolute;
    top: 12px; left: 16px;
    color: #90c0d8;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    pointer-events: none;
    opacity: 0.8;
  }}

  #graph-legend {{
    position: absolute;
    bottom: 12px; right: 14px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    pointer-events: none;
  }}
  .legend-item {{
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 10px;
    color: #90c0d8;
    font-weight: 600;
  }}
  .legend-dot {{
    width: 10px; height: 10px;
    border-radius: 50%;
    flex-shrink: 0;
  }}
  .legend-line {{
    width: 18px; height: 2px;
    flex-shrink: 0;
  }}

  #tooltip {{
    position: absolute;
    display: none;
    padding: 8px 12px;
    background: rgba(10,25,40,0.95);
    border: 1px solid #2d8bba;
    border-radius: 8px;
    color: #e0f0f8;
    font-size: 12px;
    pointer-events: none;
    max-width: 220px;
    z-index: 99;
    box-shadow: 0 4px 16px rgba(0,0,0,0.5);
  }}

  #controls {{
    position: absolute;
    top: 12px; right: 14px;
    display: flex;
    gap: 6px;
  }}
  .ctrl-btn {{
    background: rgba(45,75,100,0.85);
    border: 1px solid #3a6a8a;
    border-radius: 6px;
    color: #90c0d8;
    font-size: 14px;
    width: 28px; height: 28px;
    cursor: pointer;
    display: grid;
    place-items: center;
    transition: background 0.15s;
  }}
  .ctrl-btn:hover {{ background: rgba(45,110,160,0.9); color: #f2c84b; }}
</style>
</head>
<body>
<div id="graph-wrap">
  <div id="graph-title">{title}</div>
  <div id="graph-canvas"></div>
  <div id="controls">
    <button class="ctrl-btn" id="btn-fit" title="Fit view">⊡</button>
    <button class="ctrl-btn" id="btn-physics" title="Toggle physics">⟳</button>
  </div>
  <div id="graph-legend">
    <div class="legend-item"><div class="legend-dot" style="background:#1a5f7a;border:1px solid #2d8bba"></div>Entity</div>
    <div class="legend-item"><div class="legend-dot" style="background:#0d5d49;border:1px solid #1b8b69"></div>Development</div>
    <div class="legend-item"><div class="legend-dot" style="background:#4a3060;border:1px solid #7b52ab"></div>Quality</div>
    <div class="legend-item"><div class="legend-dot" style="background:#1a1a5a;border:1px solid #4a4aaa"></div>Modern</div>
    <div class="legend-item"><div class="legend-line" style="background:#f2c84b"></div>Primary</div>
    <div class="legend-item"><div class="legend-line" style="background:#4a9aaa;border-top:1px dashed #4a9aaa;background:none"></div>Guideline</div>
  </div>
  <div id="tooltip"></div>
</div>

<script>
const nodes = new vis.DataSet({nodes_json});
const edges = new vis.DataSet({edges_json});

const container = document.getElementById('graph-canvas');
const options = {{
  nodes: {{
    borderWidth: 2,
    shadow: {{ enabled: true, color: 'rgba(0,0,0,0.5)', size: 8, x: 2, y: 2 }},
    margin: {{ top: 6, bottom: 6, left: 8, right: 8 }},
  }},
  edges: {{
    font: {{ background: 'rgba(10,25,40,0.7)', strokeWidth: 0 }},
    selectionWidth: 2,
    shadow: {{ enabled: false }},
  }},
  physics: {{
    solver: '{physics_solver}',
    barnesHut: {{
      gravitationalConstant: -5000,
      centralGravity: 0.3,
      springLength: 130,
      springConstant: 0.04,
      damping: 0.12,
    }},
    forceAtlas2Based: {{
      gravitationalConstant: -60,
      centralGravity: 0.01,
      springLength: 120,
      springConstant: 0.08,
      damping: 0.4,
    }},
    stabilization: {{ iterations: 200, updateInterval: 25 }},
  }},
  interaction: {{
    hover: true,
    tooltipDelay: 150,
    zoomView: true,
    dragView: true,
    navigationButtons: false,
    keyboard: false,
  }},
  layout: {{ improvedLayout: true }},
}};

const network = new vis.Network(container, {{ nodes, edges }}, options);

// Fit after stabilization
network.on('stabilizationIterationsDone', () => {{
  network.fit({{ animation: {{ duration: 600, easingFunction: 'easeInOutQuad' }} }});
}});

// Tooltip on hover
const tooltip = document.getElementById('tooltip');
network.on('hoverNode', (params) => {{
  const node = nodes.get(params.node);
  tooltip.style.display = 'block';
  tooltip.style.left = (params.event.offsetX + 14) + 'px';
  tooltip.style.top  = (params.event.offsetY - 10) + 'px';
  tooltip.innerHTML  = '<b>' + node.label + '</b>';
}});
network.on('blurNode', () => {{ tooltip.style.display = 'none'; }});

network.on('hoverEdge', (params) => {{
  const edge = edges.get(params.edge);
  tooltip.style.display = 'block';
  tooltip.style.left = (params.event.offsetX + 14) + 'px';
  tooltip.style.top  = (params.event.offsetY - 10) + 'px';
  tooltip.innerHTML  = '→ <i>' + (edge.label || '') + '</i>';
}});
network.on('blurEdge', () => {{ tooltip.style.display = 'none'; }});

// Controls
document.getElementById('btn-fit').addEventListener('click', () => {{
  network.fit({{ animation: {{ duration: 500, easingFunction: 'easeInOutQuad' }} }});
}});

let physicsOn = true;
document.getElementById('btn-physics').addEventListener('click', () => {{
  physicsOn = !physicsOn;
  network.setOptions({{ physics: {{ enabled: physicsOn }} }});
  document.getElementById('btn-physics').style.color = physicsOn ? '#90c0d8' : '#f2c84b';
}});
</script>
</body>
</html>
"""
    components.html(html, height=height + 10, scrolling=False)
