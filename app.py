import streamlit.components.v1 as components
import streamlit as st
from urllib.parse import quote


st.set_page_config(
    page_title="Pharmaceutical Development Ontology",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="expanded",
)


GUIDELINES = {
    "ICH Q1": {
        "title": "Stability Testing",
        "scope": "Stability study design, storage conditions, shelf-life estimation, photostability, and data evaluation.",
        "rationale": "Use when the ontology item must prove that product quality remains acceptable over time.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH Q2(R2)": {
        "title": "Validation of Analytical Procedures",
        "scope": "Specificity, accuracy, precision, linearity, range, detection limit, quantitation limit, and robustness.",
        "rationale": "Use when the ontology item depends on a test method being reliable for its intended purpose.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH Q3": {
        "title": "Impurities",
        "scope": "Organic impurities, degradation products, residual solvents, and elemental impurities.",
        "rationale": "Use when the ontology item must identify, qualify, limit, or monitor impurity risk.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH Q6": {
        "title": "Specifications",
        "scope": "Test procedures and acceptance criteria for drug substances and drug products.",
        "rationale": "Use when the ontology item defines what must be tested and what acceptance criteria apply.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH Q7": {
        "title": "GMP for Active Pharmaceutical Ingredients",
        "scope": "GMP expectations for API manufacture, control, documentation, materials, and quality management.",
        "rationale": "Use when the ontology item concerns API manufacturing practice and GMP control.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH Q8": {
        "title": "Pharmaceutical Development",
        "scope": "QTPP, CQA, formulation development, process understanding, and control strategy.",
        "rationale": "Use when the ontology item explains how product design creates the intended quality profile.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH Q9": {
        "title": "Quality Risk Management",
        "scope": "Risk identification, risk analysis, risk control, risk communication, and risk review.",
        "rationale": "Use when the ontology item requires risk-based prioritization or justification.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH Q10": {
        "title": "Pharmaceutical Quality System",
        "scope": "Quality system operation across development, technology transfer, commercial manufacturing, and discontinuation.",
        "rationale": "Use when the ontology item must be controlled through deviation, CAPA, change control, or continual improvement.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH Q11": {
        "title": "Development and Manufacture of Drug Substances",
        "scope": "API manufacturing process development, starting materials, control strategy, and impurity control.",
        "rationale": "Use when the ontology item concerns drug substance origin, route, control, or manufacturing knowledge.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH Q12": {
        "title": "Lifecycle Management",
        "scope": "Post-approval change management, established conditions, PACMP, and product lifecycle strategy.",
        "rationale": "Use when the ontology item must support predictable regulatory change management after approval.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH Q13": {
        "title": "Continuous Manufacturing",
        "scope": "Development, implementation, operation, and control of continuous manufacturing.",
        "rationale": "Use when the ontology item addresses continuous process design or real-time process control.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH Q14": {
        "title": "Analytical Procedure Development",
        "scope": "Analytical target profile, method development knowledge, method risk, and lifecycle management.",
        "rationale": "Use when the ontology item must explain why an analytical method was designed in a particular way.",
        "url": "https://www.ich.org/page/quality-guidelines",
    },
    "ICH M4": {
        "title": "Common Technical Document",
        "scope": "Standardized submission structure for quality, nonclinical, and clinical documentation.",
        "rationale": "Use when the ontology item must be placed into a regulatory submission structure.",
        "url": "https://www.ich.org/page/ctd",
    },
    "ICH M7": {
        "title": "Mutagenic Impurities",
        "scope": "Assessment and control of DNA-reactive mutagenic impurities.",
        "rationale": "Use when impurity risk involves potential mutagenicity and patient safety limits.",
        "url": "https://www.ich.org/page/multidisciplinary-guidelines",
    },
    "ICH M3": {
        "title": "Nonclinical Safety Studies",
        "scope": "Timing and scope of nonclinical safety studies to support clinical trials and marketing authorization.",
        "rationale": "Use when the ontology item defines the nonclinical evidence package for human exposure.",
        "url": "https://www.ich.org/page/multidisciplinary-guidelines",
    },
    "ICH S-Series": {
        "title": "Safety Guidelines",
        "scope": "Genotoxicity, safety pharmacology, reproductive toxicity, carcinogenicity, biotechnology products, and oncology products.",
        "rationale": "Use when the ontology item concerns toxicology or nonclinical safety evidence.",
        "url": "https://www.ich.org/page/safety-guidelines",
    },
    "ICH E-Series": {
        "title": "Efficacy Guidelines",
        "scope": "Clinical trial design, conduct, statistical principles, safety reporting, and clinical study reports.",
        "rationale": "Use when the ontology item concerns clinical evidence and efficacy evaluation.",
        "url": "https://www.ich.org/page/efficacy-guidelines",
    },
    "FDA PQ/CMC": {
        "title": "Pharmaceutical Quality / CMC Structured Data",
        "scope": "Structured CMC data elements for drug substance, drug product, specifications, batch analysis, and stability.",
        "rationale": "Use when CMC information must become structured, reusable, and reviewable as data.",
        "url": "https://www.fda.gov/industry/fda-data-standards-advisory-board/pharmaceutical-quality-chemistry-manufacturing-controls-pqcmc",
    },
    "FDA NAMs": {
        "title": "New Approach Methodologies",
        "scope": "Context of use, human biological relevance, technical characterization, and fit-for-purpose assessment.",
        "rationale": "Use when nonclinical evidence includes human-relevant alternatives to conventional animal testing.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/general-considerations-use-new-approach-methodologies-drug-development",
    },
    "FDA AI": {
        "title": "AI for Regulatory Decision-Making",
        "scope": "Context of use, model risk, credibility assessment, validation, and lifecycle maintenance.",
        "rationale": "Use when AI model outputs are used to support regulatory or quality decisions.",
        "url": "https://www.fda.gov/regulatory-information/search-fda-guidance-documents/considerations-use-artificial-intelligence-support-regulatory-decision-making-drug-and-biological",
    },
}


ONTOLOGY = {
    "1. Drug Entity": {
        "description": "Core product entities that define what the medicine is made of and how it is presented to patients.",
        "items": {
            "Drug Substance / API": {
                "definition": "The active substance responsible for the intended pharmacological effect.",
                "details": [
                    "Origin and source of the active substance",
                    "Manufacturing route and starting material strategy",
                    "Physicochemical properties such as solubility, particle size, polymorphism, hygroscopicity, and water content",
                    "Impurity profile, residual solvent risk, elemental impurity risk, and stability profile",
                    "DMF or equivalent supplier-controlled evidence",
                ],
                "data": ["DMF Type II", "API CoA", "manufacturing flow", "impurity profile", "stability data", "batch analysis"],
                "ctd": ["3.2.S.1 General Information", "3.2.S.2 Manufacture", "3.2.S.3 Characterisation", "3.2.S.4 Control of Drug Substance", "3.2.S.7 Stability"],
                "guidelines": ["ICH Q11", "ICH Q7", "ICH Q3", "ICH Q1", "ICH M4"],
                "rationale": "API evidence must prove identity, origin, manufacturing consistency, impurity control, GMP suitability, and stability. That is why Q11, Q7, Q3, Q1, and CTD Module 3.2.S are the core references.",
            },
            "Drug Product": {
                "definition": "The finished dosage form containing the drug substance and excipients in the final presentation.",
                "details": [
                    "Dosage form, route of administration, strength, and packaging configuration",
                    "Finished product specification and acceptance criteria",
                    "Batch formula, manufacturing process, and process controls",
                    "Dissolution, content uniformity, assay, impurities, microbial quality, or sterility depending on dosage form",
                    "Shelf-life and storage condition justification",
                ],
                "data": ["QTPP", "CQA list", "finished product specification", "batch records", "batch analysis", "stability protocol and report"],
                "ctd": ["3.2.P.1 Description and Composition", "3.2.P.2 Pharmaceutical Development", "3.2.P.3 Manufacture", "3.2.P.5 Control of Drug Product", "3.2.P.8 Stability"],
                "guidelines": ["ICH Q8", "ICH Q6", "ICH Q1", "ICH Q2(R2)", "ICH Q14", "ICH M4"],
                "rationale": "Drug product evidence must prove that formulation and process design produce a finished medicine with reproducible quality. Q8 supports development logic, Q6 supports specifications, Q1 supports stability, and Q2/Q14 support analytical control.",
            },
            "Excipient": {
                "definition": "A non-active ingredient that supports manufacturability, stability, delivery, appearance, or patient use.",
                "details": [
                    "Excipient grade, compendial status, supplier qualification, and CoA review",
                    "Functional role such as diluent, binder, disintegrant, lubricant, stabilizer, preservative, or solvent",
                    "Compatibility with API and influence on dissolution, stability, and manufacturability",
                    "Residual solvent, elemental impurity, microbial, or animal-origin risk when relevant",
                ],
                "data": ["excipient CoA", "pharmacopeial monograph", "supplier qualification", "compatibility study", "risk assessment"],
                "ctd": ["3.2.P.1 Composition", "3.2.P.2 Pharmaceutical Development", "3.2.P.4 Control of Excipients"],
                "guidelines": ["ICH Q8", "ICH Q9", "ICH Q3"],
                "rationale": "Excipients are not pharmacologically active, but they can change CQAs. Q8 supports formulation rationale, Q9 supports risk-based evaluation, and Q3 applies when impurity risks are relevant.",
            },
        },
    },
    "2. Pharmaceutical Development": {
        "description": "Design logic that connects target product performance to formulation, material attributes, process variables, and control strategy.",
        "items": {
            "QTPP": {
                "definition": "Quality Target Product Profile: the prospective summary of product quality characteristics required for safety and efficacy.",
                "details": [
                    "Target dosage form, route, strength, release profile, patient use, packaging, and stability goal",
                    "Defines what the product must become before formulation and process details are fixed",
                    "Provides the anchor for CQA identification and control strategy design",
                ],
                "data": ["target product profile", "clinical/regulatory target", "dosage form target", "stability target"],
                "ctd": ["3.2.P.2 Pharmaceutical Development", "Module 2.3 Quality Overall Summary"],
                "guidelines": ["ICH Q8", "ICH Q9"],
                "rationale": "QTPP is a Q8 development concept. Q9 is linked because QTPP drives risk-based selection of CQAs and controls.",
            },
            "CQA": {
                "definition": "Critical Quality Attribute: a physical, chemical, biological, or microbiological property that should be controlled to ensure product quality.",
                "details": [
                    "Examples include assay, content uniformity, dissolution, impurities, pH, water content, sterility, and microbial limits",
                    "CQAs connect patient-facing product performance to tests, acceptance criteria, process controls, and stability monitoring",
                    "CQA criticality should be justified by patient risk and product performance impact",
                ],
                "data": ["CQA assessment", "risk ranking", "specification linkage", "method linkage", "stability linkage"],
                "ctd": ["3.2.P.2 Pharmaceutical Development", "3.2.P.5 Control of Drug Product", "3.2.P.8 Stability"],
                "guidelines": ["ICH Q8", "ICH Q9", "ICH Q6", "ICH Q1"],
                "rationale": "CQAs originate from Q8 development logic. Q9 explains risk ranking, Q6 turns CQAs into specifications, and Q1 verifies whether CQAs remain controlled over time.",
            },
            "CMA / CPP": {
                "definition": "Critical Material Attributes and Critical Process Parameters that can affect CQAs.",
                "details": [
                    "CMA examples: API particle size, polymorph, water content, excipient grade, and impurity burden",
                    "CPP examples: blending time, granulation endpoint, drying temperature, compression force, coating parameters, and sterilization conditions",
                    "CMA and CPP understanding supports design space, process control, validation, and lifecycle change management",
                ],
                "data": ["DoE results", "process development report", "material characterization", "risk assessment", "control strategy"],
                "ctd": ["3.2.P.2 Pharmaceutical Development", "3.2.P.3 Manufacture", "3.2.P.3.5 Process Validation"],
                "guidelines": ["ICH Q8", "ICH Q9", "ICH Q10", "ICH Q11"],
                "rationale": "Q8 explains the link between formulation/process understanding and CQAs. Q9 ranks risk. Q10 governs lifecycle control. Q11 applies when the material attribute belongs to drug substance development.",
            },
        },
    },
    "3. Manufacturing Process": {
        "description": "Manufacturing knowledge that shows how designed quality is reproduced batch after batch.",
        "items": {
            "Unit Operations": {
                "definition": "Discrete manufacturing steps such as weighing, mixing, granulation, drying, milling, compression, coating, sterilization, filling, and packaging.",
                "details": [
                    "Each unit operation should be linked to the CQAs it can affect",
                    "In-process controls should be justified by process risk and product performance",
                    "Manufacturing description should be traceable to batch record and process validation evidence",
                ],
                "data": ["manufacturing flow diagram", "batch record", "IPC list", "equipment parameters", "process development report"],
                "ctd": ["3.2.P.3 Manufacture", "3.2.P.3.3 Description of Manufacturing Process", "3.2.P.3.4 Controls of Critical Steps"],
                "guidelines": ["ICH Q8", "ICH Q9", "ICH Q10"],
                "rationale": "Manufacturing steps are selected and justified through Q8 process understanding, prioritized through Q9 risk management, and maintained through the Q10 quality system.",
            },
            "Process Validation": {
                "definition": "Evidence that the manufacturing process can consistently deliver product meeting predetermined quality attributes.",
                "details": [
                    "Includes process design, process qualification, and continued process verification",
                    "Should connect CPPs, IPCs, CQAs, batch analysis, and deviation/CAPA history",
                    "Supports commercial manufacturing confidence and lifecycle control",
                ],
                "data": ["PV protocol", "PV report", "PPQ batches", "continued process verification", "deviation trend"],
                "ctd": ["3.2.P.3.5 Process Validation and/or Evaluation"],
                "guidelines": ["ICH Q8", "ICH Q9", "ICH Q10"],
                "rationale": "Process validation must show that process knowledge and control strategy are effective. Q8 supports design understanding, Q9 supports risk-based controls, and Q10 supports ongoing verification.",
            },
            "Continuous Manufacturing": {
                "definition": "A manufacturing approach where material is continuously input, processed, and output under an integrated control strategy.",
                "details": [
                    "Requires process dynamics, residence time distribution, diversion strategy, and real-time monitoring concepts",
                    "Can connect strongly with PAT, model-based control, and continuous verification",
                    "Requires clear linkage among process parameters, material traceability, and quality decisions",
                ],
                "data": ["control strategy", "residence time model", "diversion strategy", "PAT data", "process monitoring"],
                "ctd": ["3.2.P.3 Manufacture", "3.2.P.5 Control of Drug Product"],
                "guidelines": ["ICH Q13", "ICH Q8", "ICH Q9", "ICH Q10"],
                "rationale": "Q13 is the direct reference for continuous manufacturing. Q8, Q9, and Q10 remain necessary because development logic, risk control, and quality system operation still apply.",
            },
        },
    },
    "4. Quality System": {
        "description": "Specifications, test methods, validation evidence, and quality operations used to prove and maintain product quality.",
        "items": {
            "Specification": {
                "definition": "A list of tests, analytical procedures, and acceptance criteria that define product or material quality.",
                "details": [
                    "Drug substance and drug product specifications should be separately defined",
                    "Tests should be justified by CQAs, impurity risks, dosage form characteristics, and stability needs",
                    "Acceptance criteria should be supported by development data, batch analysis, safety considerations, and stability data",
                ],
                "data": ["specification table", "acceptance criteria", "justification", "batch analysis", "stability trend"],
                "ctd": ["3.2.S.4 Control of Drug Substance", "3.2.P.5 Control of Drug Product"],
                "guidelines": ["ICH Q6", "ICH Q3", "ICH Q1", "ICH Q2(R2)", "ICH Q14"],
                "rationale": "Q6 defines the specification framework. Q3 supports impurity limits. Q1 supports stability-related criteria. Q2 and Q14 support the methods used to measure each attribute.",
            },
            "Analytical Method": {
                "definition": "A procedure used to measure a quality attribute such as assay, impurities, dissolution, water content, pH, or microbial quality.",
                "details": [
                    "Method purpose should be defined by an analytical target profile or equivalent intended use",
                    "Method parameters and conditions should be justified through development knowledge",
                    "Method performance should be validated against the intended use and product matrix",
                    "Stability-indicating methods should demonstrate separation of degradation products when relevant",
                ],
                "data": ["method procedure", "ATP", "development report", "validation protocol", "validation report", "robustness data"],
                "ctd": ["3.2.S.4.2 Analytical Procedures", "3.2.S.4.3 Validation", "3.2.P.5.2 Analytical Procedures", "3.2.P.5.3 Validation"],
                "guidelines": ["ICH Q14", "ICH Q2(R2)", "ICH Q6", "ICH Q1"],
                "rationale": "Q14 explains how and why the analytical procedure was developed. Q2(R2) proves that the method is valid for its intended use. Q6 connects the method to a specification, and Q1 is relevant when the method supports stability.",
            },
            "Impurity Control": {
                "definition": "A control framework for process impurities, degradation products, residual solvents, elemental impurities, and mutagenic impurities.",
                "details": [
                    "Impurities should be classified by origin, toxicity concern, formation pathway, and control point",
                    "Drug substance impurities and drug product degradation products should be distinguished",
                    "Control strategy can include process controls, raw material controls, specifications, and stability monitoring",
                ],
                "data": ["impurity profile", "qualification threshold", "toxicological assessment", "forced degradation", "control strategy"],
                "ctd": ["3.2.S.3.2 Impurities", "3.2.S.4 Control of Drug Substance", "3.2.P.5 Control of Drug Product", "3.2.P.8 Stability"],
                "guidelines": ["ICH Q3", "ICH M7", "ICH Q11", "ICH Q1"],
                "rationale": "Q3 is the core impurity guideline family. M7 applies to mutagenic impurities. Q11 connects impurity control to API manufacture. Q1 applies when impurity increase is a stability concern.",
            },
        },
    },
    "5. Stability": {
        "description": "Evidence that quality remains acceptable across shelf life, storage, transport, and use conditions.",
        "items": {
            "Stability Study": {
                "definition": "A planned study to monitor whether drug substance or drug product quality changes over time under defined conditions.",
                "details": [
                    "Includes long-term, accelerated, intermediate, photostability, and in-use studies where relevant",
                    "Monitors attributes such as assay, impurities, dissolution, pH, water content, microbial quality, and appearance",
                    "Supports shelf life, retest period, storage condition, and packaging suitability",
                ],
                "data": ["stability protocol", "timepoint results", "trend analysis", "storage condition", "shelf-life proposal"],
                "ctd": ["3.2.S.7 Stability", "3.2.P.8 Stability"],
                "guidelines": ["ICH Q1", "ICH Q2(R2)", "ICH Q14"],
                "rationale": "Q1 is the direct stability guideline family. Q2/Q14 are linked when stability-indicating analytical methods are required to produce reliable stability data.",
            },
            "Shelf Life and Storage": {
                "definition": "The approved period and conditions under which product quality is expected to remain within specification.",
                "details": [
                    "Derived from stability data, statistical evaluation, packaging suitability, and degradation behavior",
                    "Must be consistent with product labeling and distribution conditions",
                    "Can be affected by post-approval changes in formulation, process, site, or packaging",
                ],
                "data": ["stability model", "expiry dating", "storage statement", "labeling text", "packaging data"],
                "ctd": ["3.2.P.8 Stability", "Module 1 Labeling when region-specific"],
                "guidelines": ["ICH Q1", "ICH Q12"],
                "rationale": "Q1 supports the scientific basis for shelf life and storage conditions. Q12 becomes relevant when lifecycle changes could affect approved stability commitments.",
            },
        },
    },
    "6. Safety and Efficacy": {
        "description": "Nonclinical and clinical evidence that supports patient exposure, benefit, risk, and intended use.",
        "items": {
            "Nonclinical Evidence": {
                "definition": "Pharmacology, toxicology, safety pharmacology, genotoxicity, and related evidence supporting human use.",
                "details": [
                    "Defines whether a candidate can proceed into clinical testing",
                    "Links toxicology findings, exposure margins, safety pharmacology, and risk management",
                    "For oncology or biotechnology products, product-specific ICH safety guidance may apply",
                ],
                "data": ["pharmacology report", "toxicology report", "TK/PK data", "safety pharmacology", "genotoxicity"],
                "ctd": ["Module 4 Nonclinical Study Reports", "Module 2.4 Nonclinical Overview", "Module 2.6 Nonclinical Summaries"],
                "guidelines": ["ICH M3", "ICH S-Series", "ICH M4"],
                "rationale": "M3 defines timing and scope of nonclinical safety studies. The S-series provides safety-specific expectations. M4 defines how nonclinical evidence is submitted.",
            },
            "Clinical Evidence": {
                "definition": "Human study evidence used to evaluate efficacy, safety, dose, population, and benefit-risk.",
                "details": [
                    "Includes Phase 1, Phase 2, Phase 3, and post-marketing evidence where relevant",
                    "Connects protocol, endpoints, statistical analysis, clinical study report, and labeling claims",
                    "May connect to biomarkers, companion diagnostics, and real-world evidence depending on product strategy",
                ],
                "data": ["protocol", "CSR", "statistical analysis plan", "efficacy endpoints", "safety database"],
                "ctd": ["Module 5 Clinical Study Reports", "Module 2.5 Clinical Overview", "Module 2.7 Clinical Summary"],
                "guidelines": ["ICH E-Series", "ICH M4"],
                "rationale": "The E-series governs clinical trial design, conduct, analysis, and reporting. M4 defines how clinical evidence is structured in the submission.",
            },
        },
    },
    "7. Regulatory Documentation": {
        "description": "Submission structures and referenced documents that make product knowledge reviewable by regulators.",
        "items": {
            "CTD Module 3": {
                "definition": "The quality module of the Common Technical Document, covering drug substance and drug product CMC evidence.",
                "details": [
                    "3.2.S covers drug substance information",
                    "3.2.P covers drug product information",
                    "Module 2.3 summarizes quality evidence in the Quality Overall Summary",
                    "A strong ontology should map every quality node to a CTD location",
                ],
                "data": ["Module 2.3 QOS", "3.2.S", "3.2.P", "specification tables", "stability summaries"],
                "ctd": ["Module 2.3 Quality Overall Summary", "Module 3 Quality"],
                "guidelines": ["ICH M4", "FDA PQ/CMC"],
                "rationale": "M4 defines the CTD structure. FDA PQ/CMC is relevant because CMC information is moving toward more structured, data-oriented formats.",
            },
            "DMF / Supplier Evidence": {
                "definition": "Confidential supplier-controlled information referenced to support API, excipient, packaging, or other material quality.",
                "details": [
                    "Type II DMF commonly supports API information",
                    "Type III DMF supports packaging material",
                    "Type IV DMF supports excipients, colorants, flavors, or related materials",
                    "Letter of Authorization enables the applicant to reference confidential supplier information",
                ],
                "data": ["DMF number", "LOA", "supplier CoA", "quality agreement", "change notification"],
                "ctd": ["3.2.S drug substance references", "3.2.P.4 excipient references", "3.2.P.7 container closure references"],
                "guidelines": ["ICH Q7", "ICH Q11", "ICH M4"],
                "rationale": "DMF evidence supports confidential material knowledge. Q7 and Q11 apply when the referenced information concerns API GMP, manufacture, and control. M4 defines how references are placed in the submission.",
            },
        },
    },
    "8. Risk and Lifecycle": {
        "description": "Risk-based and lifecycle-based control of product knowledge after development and approval.",
        "items": {
            "Quality Risk Management": {
                "definition": "A systematic process for assessing, controlling, communicating, and reviewing quality risk.",
                "details": [
                    "Can be applied to CQA selection, CPP ranking, specification justification, method robustness, supplier risk, and change impact",
                    "Typical tools include FMEA, HACCP, risk ranking, and decision trees",
                    "Risk outputs should be traceable to control strategy and lifecycle monitoring",
                ],
                "data": ["risk assessment", "FMEA", "risk ranking", "risk review", "control action"],
                "ctd": ["3.2.P.2 Pharmaceutical Development", "3.2.P.3 Manufacture", "3.2.P.5 Control of Drug Product"],
                "guidelines": ["ICH Q9", "ICH Q10"],
                "rationale": "Q9 is the direct guideline for quality risk management. Q10 is linked because risk outputs must be managed inside the pharmaceutical quality system.",
            },
            "Lifecycle Change Management": {
                "definition": "Management of post-approval changes in a way that preserves product quality and regulatory commitments.",
                "details": [
                    "Changes may affect materials, process, site, equipment, specification, analytical method, packaging, or stability commitments",
                    "A useful ontology should show which CQA, CPP, method, CTD section, and guideline are impacted",
                    "Established conditions and post-approval change management plans can make change strategy more predictable",
                ],
                "data": ["change request", "impact assessment", "established conditions", "PACMP", "CAPA", "PQR/APR"],
                "ctd": ["Module 3 Quality", "regional post-approval change submissions"],
                "guidelines": ["ICH Q9", "ICH Q10", "ICH Q12"],
                "rationale": "Q9 supports change risk assessment, Q10 governs quality system execution, and Q12 provides the lifecycle regulatory framework for post-approval changes.",
            },
        },
    },
    "9. FDA Modernization": {
        "description": "Modern evidence layers that extend conventional development evidence toward structured data, NAMs, and AI credibility.",
        "items": {
            "PQ/CMC Structured Data": {
                "definition": "A structured data approach to CMC information including drug substance, drug product, specification, batch analysis, and stability.",
                "details": [
                    "Transforms CMC content from narrative documents into reusable, reviewable data elements",
                    "Fits naturally with an ontology because each CMC element can be mapped to a node, relation, and evidence source",
                    "Supports future readiness for more structured regulatory submissions",
                ],
                "data": ["drug substance data", "drug product data", "specifications", "batch analysis", "stability data"],
                "ctd": ["Module 2.3 Quality Overall Summary", "Module 3 Quality"],
                "guidelines": ["FDA PQ/CMC", "ICH M4", "ICH Q6", "ICH Q1"],
                "rationale": "FDA PQ/CMC is relevant when CMC evidence must become structured data. M4 anchors the CTD structure, while Q6 and Q1 define key specification and stability data elements.",
            },
            "NAMs Evidence": {
                "definition": "New Approach Methodologies that can support nonclinical evidence through human-relevant models, in vitro systems, organoids, MPS, or computational approaches.",
                "details": [
                    "Requires clear context of use",
                    "Requires human biological relevance",
                    "Requires technical characterization and limitations",
                    "Requires fit-for-purpose justification and weight-of-evidence integration",
                ],
                "data": ["context of use", "model characterization", "validation evidence", "weight-of-evidence matrix"],
                "ctd": ["Module 4 Nonclinical", "Module 2.4 Nonclinical Overview", "Module 2.6 Nonclinical Summaries"],
                "guidelines": ["FDA NAMs", "ICH M3", "ICH S-Series"],
                "rationale": "FDA NAMs guidance supports the evaluation of alternative evidence. M3 and the S-series remain necessary because NAMs evidence still supports nonclinical safety decisions.",
            },
            "AI Credibility": {
                "definition": "Evidence that an AI model used for regulatory or quality decision support is credible for its stated context of use.",
                "details": [
                    "Defines context of use and model role in decision-making",
                    "Evaluates model risk and potential decision impact",
                    "Documents validation, verification, limitations, monitoring, and lifecycle maintenance",
                    "Should be linked to the quality or regulatory decision the model supports",
                ],
                "data": ["context of use", "model risk assessment", "validation data", "monitoring plan", "model change log"],
                "ctd": ["Relevant CTD section depending on AI use case", "quality system records when used in GMP context"],
                "guidelines": ["FDA AI", "ICH Q9", "ICH Q10"],
                "rationale": "FDA AI guidance is relevant when AI supports regulatory decision-making. Q9 supports model risk assessment, and Q10 applies when AI use is embedded in the pharmaceutical quality system.",
            },
        },
    },
}


def flatten_items():
    rows = []
    for category, category_data in ONTOLOGY.items():
        for item, item_data in category_data["items"].items():
            rows.append(
                {
                    "Category": category,
                    "Ontology Item": item,
                    "Primary Guidelines": ", ".join(item_data["guidelines"]),
                    "CTD / Evidence Location": "; ".join(item_data["ctd"][:2]),
                }
            )
    return rows


def guideline_chip(name):
    return f"<span class='chip'>{name}</span>"


PROCESS_FLOW = [
    ("1. Drug Entity", "API, product, excipient", "Q11 / Q8", "Material identity"),
    ("2. Pharmaceutical Development", "QTPP, CQA, CMA, CPP", "Q8 / Q9", "Product design"),
    ("3. Manufacturing Process", "Unit operations, validation", "Q8 / Q10", "Process control"),
    ("4. Quality System", "Specs, methods, impurities", "Q6 / Q2 / Q14", "Quality evidence"),
    ("5. Stability", "Shelf life and storage", "Q1", "Time-based proof"),
    ("6. Safety and Efficacy", "Nonclinical and clinical", "M3 / S / E", "Benefit and risk"),
    ("7. Regulatory Documentation", "CTD, DMF, evidence", "M4 / PQ-CMC", "Submission structure"),
    ("8. Risk and Lifecycle", "Risk and change control", "Q9 / Q10 / Q12", "Lifecycle control"),
    ("9. FDA Modernization", "PQ-CMC, NAMs, AI", "FDA / ICH", "Modern evidence"),
]


def render_card(title, body, footer=None, accent="green"):
    accent_map = {
        "green": "#2e715e",
        "blue": "#236b9a",
        "gold": "#9a6a1f",
        "red": "#ad4f3f",
        "dark": "#172126",
    }
    color = accent_map.get(accent, accent_map["green"])
    footer_html = f"<div class='card-footer'>{footer}</div>" if footer else ""
    st.markdown(
        f"""
        <div class="info-card" style="border-top:4px solid {color};">
            <h3>{title}</h3>
            <p>{body}</p>
            {footer_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_list_card(title, values, css_class="list-card"):
    items = "".join([f"<li>{value}</li>" for value in values])
    st.markdown(
        f"""
        <div class="{css_class}">
            <h3>{title}</h3>
            <ul>{items}</ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_process_image(selected_category):
    nodes = [
        ("1. Drug Entity", "DRUG ENTITY", "API · PRODUCT · EXCIPIENT", "ICH Q11 · Q7 · Q8", "blue"),
        ("2. Pharmaceutical Development", "DEVELOPMENT", "QTPP · CQA · CMA/CPP", "ICH Q8 · Q9", "green"),
        ("3. Manufacturing Process", "MANUFACTURING", "UNIT OPS · VALIDATION", "ICH Q10 · Q13", "orange"),
        ("4. Quality System", "QUALITY SYSTEM", "SPEC · METHOD · IMPURITY", "ICH Q6 · Q2 · Q14", "green"),
        ("5. Stability", "STABILITY", "SHELF LIFE · STORAGE", "ICH Q1", "green"),
        ("6. Safety and Efficacy", "SAFETY & EFFICACY", "NONCLINICAL · CLINICAL", "ICH M3 · S · E", "blue"),
        ("7. Regulatory Documentation", "REGULATORY DOCS", "CTD · DMF · QOS", "ICH M4 · PQ/CMC", "orange"),
        ("8. Risk and Lifecycle", "RISK & LIFECYCLE", "QRM · CHANGE", "ICH Q9 · Q10 · Q12", "rose"),
        ("9. FDA Modernization", "FDA MODERNIZATION", "STRUCTURED DATA · AI · NAMs", "FDA · ICH", "purple"),
    ]
    node_html = []
    for category, title, content, guide, color in nodes:
        active = "active" if category == selected_category else ""
        node_html.append(
            f"""
            <a class="map-node {color} {active}" href="?category={quote(category)}" target="_parent">
                <span class="node-number">{category.split(".", 1)[0]}</span>
                <span class="node-copy">
                    <strong>{title}</strong>
                    <em>{content}</em>
                    <b>{guide}</b>
                </span>
            </a>
            """
        )

    html = f"""
    <style>
        body {{
            margin: 0;
            background: transparent;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        }}
        .click-map {{
            min-height: 760px;
            border-radius: 30px;
            overflow: hidden;
            background:
                linear-gradient(135deg, #e8f2f7 0%, #fbfdfe 46%, #eef7f1 100%);
            border: 1px solid #c6d9e2;
            box-shadow: 0 22px 48px rgba(8, 32, 51, 0.16);
        }}
        .map-title {{
            background: linear-gradient(90deg, #123d61 0%, #1a775f 100%);
            color: white;
            padding: 28px 36px 12px 36px;
            font-size: 42px;
            font-weight: 900;
            letter-spacing: 1px;
            text-align: center;
            line-height: 1.08;
        }}
        .map-subtitle {{
            margin: 0;
            padding: 0 36px 24px 36px;
            background: linear-gradient(90deg, #123d61 0%, #1a775f 100%);
            color: #d8edf6;
            font-size: 18px;
            font-weight: 800;
            text-align: center;
        }}
        .map-body {{
            padding: 30px 34px 26px 34px;
        }}
        .route {{
            position: relative;
            height: 42px;
            margin: 0 8px 26px 8px;
            border-radius: 999px;
            background: linear-gradient(90deg, #f2c84b 0%, #1b8b69 100%);
            box-shadow: 0 8px 20px rgba(27, 139, 105, 0.18);
        }}
        .route::after {{
            content: "";
            position: absolute;
            right: -18px;
            top: -5px;
            border-left: 26px solid #1b8b69;
            border-top: 26px solid transparent;
            border-bottom: 26px solid transparent;
        }}
        .route-label {{
            position: absolute;
            left: 50%;
            top: 50%;
            transform: translateX(-50%);
            background: #ffe594;
            color: #17364a;
            border: 2px solid #e1bf46;
            border-radius: 999px;
            padding: 10px 36px;
            font-size: 22px;
            font-weight: 900;
            white-space: nowrap;
            margin-top: -24px;
        }}
        .map-grid {{
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 18px;
        }}
        .map-node {{
            display: grid;
            grid-template-columns: 64px 1fr;
            gap: 18px;
            align-items: center;
            min-height: 138px;
            padding: 22px 24px;
            border-radius: 22px;
            text-decoration: none;
            color: #111f25;
            background: #ffffff;
            border: 4px solid rgba(120, 166, 189, 0.85);
            box-shadow: 0 14px 28px rgba(8, 32, 51, 0.12);
            transition: transform 160ms ease, box-shadow 160ms ease, border-color 160ms ease;
        }}
        .map-node:hover {{
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 22px 42px rgba(8, 32, 51, 0.22);
            border-color: #f2c84b;
        }}
        .map-node.active {{
            border-color: #f2c84b;
            box-shadow: 0 0 0 7px rgba(242, 200, 75, 0.24), 0 22px 42px rgba(8, 32, 51, 0.22);
        }}
        .map-node strong {{
            display: block;
            font-size: 31px;
            font-weight: 950;
            line-height: 1.02;
            letter-spacing: 0;
            color: #0f1e25;
        }}
        .map-node em {{
            display: block;
            margin-top: 12px;
            color: #405760;
            font-size: 20px;
            font-style: normal;
            font-weight: 900;
            line-height: 1.15;
        }}
        .map-node b {{
            display: inline-block;
            margin-top: 14px;
            padding: 9px 16px;
            border-radius: 999px;
            color: white;
            font-size: 18px;
            font-weight: 950;
        }}
        .node-number {{
            width: 64px;
            height: 64px;
            display: grid;
            place-items: center;
            border-radius: 50%;
            color: white;
            font-size: 33px;
            font-weight: 950;
        }}
        .blue .node-number, .blue b {{
            background: #174b78;
        }}
        .green .node-number, .green b {{
            background: #176f58;
        }}
        .orange .node-number, .orange b {{
            background: #d97825;
        }}
        .purple .node-number, .purple b {{
            background: #5b3476;
        }}
        .rose .node-number, .rose b {{
            background: #9a5877;
        }}
        .focus {{
            margin: 0 8px 16px 8px;
            color: #0f1e25;
            font-size: 22px;
            font-weight: 950;
        }}
        .bottom-band {{
            display: grid;
            grid-template-columns: 1.1fr 1fr 1fr 1fr 1.5fr;
            overflow: hidden;
            margin-top: 22px;
            border-radius: 16px;
        }}
        .bottom-band span {{
            display: grid;
            place-items: center;
            min-height: 50px;
            color: white;
            font-size: 17px;
            font-weight: 900;
            text-align: center;
        }}
        .bottom-band span:nth-child(1) {{ background: #123d61; }}
        .bottom-band span:nth-child(2) {{ background: #1b8b69; }}
        .bottom-band span:nth-child(3) {{ background: #df7a24; }}
        .bottom-band span:nth-child(4) {{ background: #9a5877; }}
        .bottom-band span:nth-child(5) {{ background: #4c2a68; }}
        @media (max-width: 980px) {{
            .map-title {{
                font-size: 30px;
            }}
            .map-grid {{
                grid-template-columns: 1fr;
            }}
            .map-node strong {{
                font-size: 28px;
            }}
        }}
    </style>
    <div class="click-map">
        <div class="map-title">PHARMACEUTICAL DEVELOPMENT ONTOLOGY MAP</div>
        <p class="map-subtitle">Large, clickable ontology menu. Each domain opens its evidence page with guideline rationale.</p>
        <div class="map-body">
            <div class="route"><div class="route-label">DEVELOPMENT EVIDENCE FLOW</div></div>
            <div class="focus">RESEARCHER'S FOCUS: YOUNGNAM LEE</div>
            <div class="map-grid">
                {''.join(node_html)}
            </div>
            <div class="bottom-band">
                <span>MATERIAL + PRODUCT</span>
                <span>DEVELOPMENT</span>
                <span>CMC DOSSIER</span>
                <span>LIFECYCLE</span>
                <span>MODERNIZATION</span>
            </div>
        </div>
    </div>
    """
    components.html(html, height=850, scrolling=False)


st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 3rem;
        max-width: 1320px;
    }
    h1, h2, h3 {
        letter-spacing: 0;
    }
    .hero {
        background: radial-gradient(circle at 15% 15%, #d9eadf 0, transparent 24%),
                    linear-gradient(135deg, #172126 0%, #20363a 58%, #2e715e 100%);
        color: white;
        padding: 2rem 2.2rem;
        margin-bottom: 1.25rem;
        border: 1px solid #22383a;
        border-radius: 0.7rem;
    }
    .hero h1 {
        font-size: 3rem;
        line-height: 1.08;
        margin-bottom: 0.55rem;
        color: white;
    }
    .hero p {
        color: #d6e4df;
        font-size: 1.15rem;
        max-width: 960px;
    }
    .visual-map {
        border: 1px solid #d9d1c1;
        background: #fffdf8;
        border-radius: 0.7rem;
        overflow: hidden;
        margin: 0.6rem 0 1rem 0;
        box-shadow: 0 18px 45px rgba(23, 33, 38, 0.08);
    }
    .visual-map-head {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        gap: 2rem;
        padding: 1.2rem 1.35rem 0.2rem 1.35rem;
    }
    .visual-map-head h2 {
        margin: 0;
        font-size: 1.45rem;
    }
    .visual-map-head p {
        color: #687477;
        font-size: 0.95rem;
        max-width: 430px;
        margin: 0.25rem 0 0 0;
    }
    .eyebrow {
        display: inline-block;
        color: #1f6f55;
        background: #e7f2ec;
        padding: 0.22rem 0.5rem;
        border-radius: 0.3rem;
        font-size: 0.78rem;
        font-weight: 800;
        margin-bottom: 0.45rem;
        text-transform: uppercase;
    }
    .visual-map svg {
        width: 100%;
        height: auto;
        display: block;
    }
    div.stButton > button {
        width: 100%;
        min-height: 4.6rem;
        border-radius: 0.55rem;
        border: 1px solid #d9d1c1;
        background: #fffdf8;
        color: #1d2528;
        text-align: left;
        padding: 0.7rem 0.75rem;
        line-height: 1.18;
        font-weight: 700;
        box-shadow: 0 8px 18px rgba(23, 33, 38, 0.05);
    }
    div.stButton > button:hover {
        border-color: #2e715e;
        color: #1f6f55;
        background: #eef6f1;
    }
    .stage-caption {
        color: #687477;
        font-size: 0.8rem;
        margin-top: -0.5rem;
        min-height: 2.4rem;
    }
    .stage-guide {
        display: inline-block;
        color: #1f6f55;
        background: #e7f2ec;
        font-size: 0.75rem;
        font-weight: 800;
        padding: 0.18rem 0.42rem;
        border-radius: 0.25rem;
        margin-top: 0.15rem;
    }
    .selected-strip {
        background: linear-gradient(135deg, #172126 0%, #23373b 100%);
        color: white;
        padding: 1rem 1.15rem;
        margin: 0.9rem 0 1.1rem 0;
        border-radius: 0.55rem;
    }
    .selected-strip b {
        color: #d8eadf;
    }
    .panel {
        border: 1px solid #d9d1c1;
        background: #fffdf8;
        padding: 1rem 1.05rem;
        margin-bottom: 1rem;
    }
    .panel h3 {
        margin-top: 0;
        font-size: 1.25rem;
    }
    .rationale {
        background: linear-gradient(135deg, #172126 0%, #21383a 100%);
        color: white;
        padding: 1rem 1.2rem;
        margin: 0.8rem 0 1rem 0;
        border-radius: 0.55rem;
    }
    .rationale h3 {
        color: white;
        margin: 0 0 0.5rem 0;
        font-size: 1rem;
        text-transform: uppercase;
    }
    .chip {
        display: inline-block;
        background: #e7f2ec;
        color: #1f6f55;
        padding: 0.27rem 0.55rem;
        margin: 0.12rem;
        font-size: 0.82rem;
        font-weight: 700;
        border-radius: 0.35rem;
    }
    .ctd {
        display: inline-block;
        background: #e8f1f8;
        color: #236b9a;
        padding: 0.27rem 0.55rem;
        margin: 0.12rem;
        font-size: 0.82rem;
        font-weight: 700;
        border-radius: 0.35rem;
    }
    .small {
        color: #687477;
        font-size: 0.9rem;
    }
    .info-card, .list-card {
        border: 1px solid #d9d1c1;
        background: #fffdf8;
        padding: 1rem 1.05rem;
        margin-bottom: 1rem;
        min-height: 9rem;
        border-radius: 0.55rem;
        box-shadow: 0 10px 22px rgba(23, 33, 38, 0.05);
    }
    .info-card h3, .list-card h3 {
        margin: 0 0 0.55rem 0;
        font-size: 1.05rem;
    }
    .info-card p {
        color: #536064;
        line-height: 1.45;
        margin-bottom: 0;
    }
    .card-footer {
        color: #1f6f55;
        background: #e7f2ec;
        padding: 0.35rem 0.5rem;
        margin-top: 0.7rem;
        font-size: 0.82rem;
        font-weight: 800;
    }
    .list-card ul {
        margin: 0.35rem 0 0 1.1rem;
        padding: 0;
    }
    .list-card li {
        margin-bottom: 0.45rem;
        color: #536064;
        line-height: 1.35;
    }
    .guideline-card {
        border: 1px solid #d9d1c1;
        background: #fffdf8;
        padding: 0.9rem 1rem;
        margin-bottom: 0.75rem;
        border-radius: 0.55rem;
    }
    .guideline-card h4 {
        margin: 0 0 0.35rem 0;
        font-size: 1rem;
    }
    .guideline-card p {
        color: #536064;
        margin: 0.2rem 0;
        line-height: 1.35;
    }
    .evidence-panel {
        border: 1px solid #d9d1c1;
        background: #fffdf8;
        padding: 1rem;
        border-radius: 0.55rem;
        margin-bottom: 1rem;
    }
    .relationship-box {
        border: 1px solid #d9d1c1;
        background: #f8f4ea;
        padding: 1rem;
        border-radius: 0.55rem;
        font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        color: #253134;
        overflow-wrap: anywhere;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


st.markdown(
    """
    <div class="hero">
        <h1>Pharmaceutical Development Ontology</h1>
        <p>
        A visual navigation layer for drug development knowledge: material identity,
        product design, manufacturing, quality evidence, stability, regulatory
        documentation, lifecycle risk, and FDA modernization.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


query_category = st.query_params.get("category")
if query_category in ONTOLOGY:
    st.session_state.category = query_category
elif "category" not in st.session_state:
    st.session_state.category = list(ONTOLOGY.keys())[0]


render_process_image(st.session_state.category)

st.caption("Stage selector")
first_row = st.columns(5)
second_row = st.columns(4)
for index, (stage, caption, guide, theme) in enumerate(PROCESS_FLOW):
    row = first_row if index < 5 else second_row
    with row[index if index < 5 else index - 5]:
        if st.button(stage, key=f"stage_{stage}"):
            st.session_state.category = stage
            st.query_params["category"] = stage
        st.markdown(
            f"""
            <div class="stage-caption">
                {theme}<br><span class="stage-guide">{guide}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )


with st.sidebar:
    st.header("Ontology Menu")
    category = st.radio(
        "Development process",
        list(ONTOLOGY.keys()),
        index=list(ONTOLOGY.keys()).index(st.session_state.category),
        label_visibility="collapsed",
    )
    st.session_state.category = category
    st.query_params["category"] = category
    item = st.selectbox("Ontology item", list(ONTOLOGY[category]["items"].keys()))
    st.divider()
    st.caption("Use the menu above as the ontology tree. The selected item opens its detail page.")


category_data = ONTOLOGY[category]
item_data = category_data["items"][item]

primary_guides = " / ".join(item_data["guidelines"][:3])
st.markdown(
    f"""
    <div class="selected-strip">
        <b>{category}</b> · {category_data["description"]}<br>
        Selected item: <b>{item}</b> · Primary references: <b>{primary_guides}</b>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(f"## {item}")
render_card("Definition", item_data["definition"], "Ontology item", "green")

st.markdown(
    f"""
    <div class="rationale">
        <h3>Guideline rationale</h3>
        <p>{item_data["rationale"]}</p>
    </div>
    """,
    unsafe_allow_html=True,
)


summary_col, evidence_col = st.columns([1.2, 1])

with summary_col:
    render_list_card("Key Data Elements", item_data["data"][:4])
    with st.expander("See detailed information"):
        for detail in item_data["details"]:
            st.markdown(f"- {detail}")
        if len(item_data["data"]) > 4:
            st.markdown("**Additional data elements**")
            for datum in item_data["data"][4:]:
                st.markdown(f"- {datum}")
 
with evidence_col:
    st.markdown(
        f"""
        <div class="evidence-panel">
            <h3>CTD / Evidence Location</h3>
            {" ".join([f"<span class='ctd'>{location}</span>" for location in item_data["ctd"]])}
            <h3 style="margin-top:1rem;">Related Guidelines</h3>
            {" ".join([guideline_chip(guideline) for guideline in item_data["guidelines"]])}
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown("### Guideline Details")
guide_cols = st.columns(2)
for index, guideline_name in enumerate(item_data["guidelines"]):
    guideline = GUIDELINES[guideline_name]
    with guide_cols[index % 2]:
        st.markdown(
            f"""
            <div class="guideline-card">
                <h4>{guideline_name}: {guideline["title"]}</h4>
                <p><b>Scope:</b> {guideline["scope"]}</p>
                <p><b>Why it applies:</b> {guideline["rationale"]}</p>
                <p><a href="{guideline["url"]}" target="_blank">Open reference</a></p>
            </div>
            """,
            unsafe_allow_html=True,
        )


st.markdown("### Ontology Relationship")
relationship_examples = {
    "Drug Substance / API": "DrugSubstance --hasImpurity--> Impurity --controlledBy--> Specification --testedBy--> AnalyticalMethod",
    "Drug Product": "DrugProduct --hasCQA--> CQA --controlledBy--> Specification --monitoredBy--> StabilityStudy",
    "Excipient": "Excipient --hasFunctionalRole--> ExcipientRole --mayAffect--> CQA",
    "QTPP": "QTPP --definesTargetFor--> DrugProduct --drivesSelectionOf--> CQA",
    "CQA": "CQA --testedBy--> AnalyticalMethod --validatedBy--> MethodValidation",
    "CMA / CPP": "CMA/CPP --mayImpact--> CQA --mitigatedBy--> ControlStrategy",
    "Unit Operations": "UnitOperation --hasParameter--> CPP --affects--> CQA",
    "Process Validation": "ProcessValidation --verifies--> ManufacturingProcess --supports--> ControlStrategy",
    "Continuous Manufacturing": "ContinuousProcess --monitoredBy--> PAT --controlledBy--> RealTimeControlStrategy",
    "Specification": "Specification --contains--> TestItem --hasAcceptanceCriteria--> AcceptanceCriterion",
    "Analytical Method": "AnalyticalMethod --hasPurpose--> AnalyticalTargetProfile --validatedBy--> ICHQ2Validation",
    "Impurity Control": "Impurity --hasOrigin--> ProcessOrDegradation --controlledBy--> ControlStrategy",
    "Stability Study": "StabilityStudy --monitors--> CQA --supports--> ShelfLife",
    "Shelf Life and Storage": "ShelfLife --supportedBy--> StabilityData --appearsIn--> Labeling",
    "Nonclinical Evidence": "NonclinicalStudy --supports--> FirstInHumanExposure --summarizedIn--> CTDModule4",
    "Clinical Evidence": "ClinicalStudy --supports--> BenefitRisk --summarizedIn--> CTDModule5",
    "CTD Module 3": "QualityEvidence --submittedIn--> CTDModule3 --summarizedIn--> QOS",
    "DMF / Supplier Evidence": "SupplierEvidence --referencedBy--> Application --authorizedBy--> LOA",
    "Quality Risk Management": "RiskAssessment --prioritizes--> ControlAction --reviewedBy--> QualitySystem",
    "Lifecycle Change Management": "Change --impacts--> CQA/CPP/Method/Stability --managedBy--> Q12Strategy",
    "PQ/CMC Structured Data": "CMCDataElement --mapsTo--> CTDSection --supports--> StructuredReview",
    "NAMs Evidence": "NAMsModel --hasContextOfUse--> RegulatoryQuestion --integratedBy--> WeightOfEvidence",
    "AI Credibility": "AIModel --hasContextOfUse--> Decision --hasCredibilityEvidence--> ValidationPackage",
}
st.markdown(
    f"""
    <div class="relationship-box">
        {relationship_examples.get(item, "OntologyItem --alignedWith--> Guideline --supportedBy--> Evidence")}
    </div>
    """,
    unsafe_allow_html=True,
)


with st.expander("Full ontology index"):
    st.dataframe(flatten_items(), hide_index=True, use_container_width=True)
