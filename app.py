import streamlit as st

st.set_page_config(
    page_title="Pharmaceutical Development Ontology",
    page_icon="P",
    layout="wide",
    initial_sidebar_state="collapsed",
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


def search_ontology(term):
    tokens = [token.lower() for token in term.split() if token.strip()]
    if not tokens:
        return []

    results = []
    for category, category_data in ONTOLOGY.items():
        for item, item_data in category_data["items"].items():
            weighted_text = " ".join(
                [
                    category,
                    item,
                    item,
                    item_data["definition"],
                    item_data["rationale"],
                    " ".join(item_data["details"]),
                    " ".join(item_data["data"]),
                    " ".join(item_data["ctd"]),
                    " ".join(item_data["guidelines"]),
                ]
            ).lower()
            score = sum(weighted_text.count(token) for token in tokens)
            if score:
                results.append((score, category, item, item_data))
    return sorted(results, key=lambda result: (-result[0], result[1], result[2]))


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


CASE_STUDY = {
    "title": "Revenue vs Trust: Bioequivalence Risk After Supplier Change",
    "summary": "A marketed product with major portfolio revenue failed comparative dissolution against the reference product after an API supplier change. Root cause pointed to API particle size distribution variability, requiring supplier requalification, remanufacturing, comparative dissolution, and a post-approval variation dossier.",
    "decision": "Leadership must decide whether to proactively raise a marketing authorization issue even when short-term revenue may be affected.",
    "signals": [
        "API particle size distribution",
        "supplier qualification",
        "comparative dissolution",
        "bioequivalence risk",
        "post-approval change",
        "variation dossier",
        "R&D / Quality / Regulatory / Commercial alignment",
    ],
    "category_links": {
        "1. Drug Entity": "API material attributes, supplier evidence, and DMF/CoA review become the first root-cause layer.",
        "2. Pharmaceutical Development": "CQA, CMA, and QTPP logic explain why API particle size can affect dissolution performance.",
        "3. Manufacturing Process": "Re-manufacturing and batch evidence are needed to prove the process restores intended performance.",
        "4. Quality System": "Dissolution method, specification linkage, and comparative test interpretation become decision-critical.",
        "5. Stability": "Stability commitments may need review if the new supplier or re-manufactured product changes quality risk.",
        "6. Safety and Efficacy": "Therapeutic performance and patient trust remain the final business justification.",
        "7. Regulatory Documentation": "Variation dossier, CTD Module 3 updates, and supplier evidence must be submission-ready.",
        "8. Risk and Lifecycle": "QRM, change control, CAPA, and stakeholder escalation govern the lifecycle response.",
        "9. FDA Modernization": "Structured CMC data can make supplier, material attribute, dissolution, and change impact traceable.",
    },
}


SITUATION_PLAYBOOKS = {
    "api_supplier_change": {
        "label": "API Supplier Change",
        "lead": "Use when an API supplier, DMF, route, particle size, polymorph, or CoA profile changes.",
        "category": "1. Drug Entity",
        "item": "Drug Substance / API",
        "checklist": [
            "Confirm supplier qualification, DMF/LOA status, and GMP evidence",
            "Compare API particle size, polymorph, water content, assay, and impurity profile",
            "Assess whether material attributes can affect dissolution, assay, content uniformity, or stability",
            "Manufacture representative batch and compare product performance",
            "Document change control, QRM conclusion, and regulatory reporting category",
        ],
        "evidence": [
            "Supplier qualification record",
            "DMF or supplier technical package",
            "API CoA and batch analysis",
            "Particle size / polymorph data",
            "Comparative dissolution",
            "Change control and QRM report",
        ],
        "ctd": ["3.2.S.2", "3.2.S.3", "3.2.S.4", "3.2.P.2", "3.2.P.5"],
        "guidelines": ["ICH Q11", "ICH Q9", "ICH Q10", "ICH Q12", "ICH M4"],
        "decision": "If the supplier change can affect a CQA, treat it as a lifecycle regulatory change and prepare comparative CMC evidence.",
    },
    "dissolution_failure": {
        "label": "Dissolution Failure",
        "lead": "Use when product dissolution is out of trend, non-equivalent, or inconsistent with the reference product.",
        "category": "4. Quality System",
        "item": "Analytical Method",
        "checklist": [
            "Confirm method suitability, medium, apparatus, rpm, sampling time, and analyst/equipment factors",
            "Compare API particle size, formulation composition, process parameters, and batch history",
            "Check whether dissolution is a CQA linked to QTPP and clinical/BE performance",
            "Run comparative dissolution and trend against historical approved batches",
            "Open deviation/CAPA and assess regulatory impact if approved quality may be affected",
        ],
        "evidence": [
            "Dissolution profile",
            "Analytical method and validation",
            "Batch record",
            "API material attributes",
            "OOS/OOT investigation",
            "CAPA and change impact assessment",
        ],
        "ctd": ["3.2.P.2", "3.2.P.3", "3.2.P.5", "3.2.P.8"],
        "guidelines": ["ICH Q8", "ICH Q9", "ICH Q6", "ICH Q2(R2)", "ICH Q14"],
        "decision": "If dissolution failure is linked to material or process change, connect Quality System evidence to Risk/Lifecycle and Regulatory Documentation.",
    },
    "cqa_spec_method": {
        "label": "CQA / Spec / Method",
        "lead": "Use when setting CQAs, specifications, acceptance criteria, analytical methods, or validation packages.",
        "category": "2. Pharmaceutical Development",
        "item": "CQA",
        "checklist": [
            "Define QTPP and identify patient-relevant CQAs",
            "Link each CQA to CMA, CPP, specification, analytical method, and stability monitoring",
            "Justify acceptance criteria using development, batch, safety, and stability data",
            "Confirm method purpose through ATP or intended use",
            "Validate methods and document lifecycle method knowledge",
        ],
        "evidence": [
            "QTPP/CQA assessment",
            "Risk ranking",
            "Specification justification",
            "Analytical procedure",
            "Method validation report",
            "Stability-indicating evidence",
        ],
        "ctd": ["3.2.P.2", "3.2.P.5", "3.2.P.8", "Module 2.3"],
        "guidelines": ["ICH Q8", "ICH Q9", "ICH Q6", "ICH Q2(R2)", "ICH Q14"],
        "decision": "A quality attribute becomes operationally useful only when it is connected to a test, criterion, control point, and lifecycle monitoring plan.",
    },
    "post_approval_change": {
        "label": "Post-Approval Change",
        "lead": "Use when formulation, process, site, supplier, specification, method, or packaging changes after approval.",
        "category": "8. Risk and Lifecycle",
        "item": "Lifecycle Change Management",
        "checklist": [
            "Describe the proposed change and affected product knowledge elements",
            "Map impact to CQA, CMA, CPP, analytical method, specification, and stability",
            "Define comparative evidence needed before implementation",
            "Decide reporting category and prepare variation dossier if required",
            "Update control strategy, PQS records, and post-change monitoring",
        ],
        "evidence": [
            "Change control",
            "QRM assessment",
            "Comparability protocol",
            "Batch and analytical comparison",
            "Stability commitment",
            "Variation dossier / CTD update",
        ],
        "ctd": ["3.2.S", "3.2.P.2", "3.2.P.3", "3.2.P.5", "3.2.P.8"],
        "guidelines": ["ICH Q9", "ICH Q10", "ICH Q12", "ICH M4"],
        "decision": "If established conditions or approved quality commitments are affected, prepare a structured regulatory change package.",
    },
}


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


def render_process_image(selected_category=None):
    st.markdown(
        """
        <div class="navigator-hero">
            <div class="navigator-kicker">Pharmaceutical Development Ontology Map</div>
            <h1>Development Evidence Navigator</h1>
            <p>Find the right quality, CMC, regulatory, and lifecycle evidence from the way a medicine is actually developed and manufactured.</p>
            <div class="hero-flow">
                <span>Material</span>
                <i></i>
                <span>Product</span>
                <i></i>
                <span>Process</span>
                <i></i>
                <span>Quality</span>
                <i></i>
                <span>Lifecycle</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def open_category(category):
    st.query_params["category"] = category
    if "item" in st.query_params:
        del st.query_params["item"]
    if "playbook" in st.query_params:
        del st.query_params["playbook"]
    st.session_state.category = category
    st.rerun()


def open_playbook(playbook_key):
    playbook = SITUATION_PLAYBOOKS[playbook_key]
    st.query_params["category"] = playbook["category"]
    st.query_params["item"] = playbook["item"]
    st.query_params["playbook"] = playbook_key
    st.session_state.category = playbook["category"]
    st.rerun()


def render_landing_navigation():
    st.markdown(
        """
        <div class="map-section">
            <span>Situation Shortcuts</span>
            <b>Start from the manufacturing problem you are facing now.</b>
        </div>
        """,
        unsafe_allow_html=True,
    )
    playbook_cols = st.columns(4)
    for index, (playbook_key, playbook) in enumerate(SITUATION_PLAYBOOKS.items()):
        with playbook_cols[index % 4]:
            st.markdown(
                f"""
                <div class="mini-map-card">
                    <b>{playbook["label"]}</b>
                    <span>{playbook["category"].split(".", 1)[1].strip()}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Open", key=f"playbook_{playbook_key}"):
                open_playbook(playbook_key)

    st.markdown(
        """
        <div class="map-section ontology">
            <span>Ontology Map</span>
            <b>Or open a knowledge domain directly. Each node is a clickable evidence object.</b>
        </div>
        <div class="flow-spine">
            <span>Material</span><i></i><span>Product Design</span><i></i><span>Manufacturing</span><i></i><span>Quality Evidence</span><i></i><span>Lifecycle</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    map_nodes = [
        ("1. Drug Entity", "01", "Drug Entity", "API | Product | Excipient", "Q11 Q7 Q8"),
        ("2. Pharmaceutical Development", "02", "Development", "QTPP | CQA | CMA/CPP", "Q8 Q9"),
        ("3. Manufacturing Process", "03", "Manufacturing", "Unit Ops | Validation", "Q10 Q13"),
        ("4. Quality System", "04", "Quality System", "Spec | Method | Impurity", "Q6 Q2 Q14"),
        ("5. Stability", "05", "Stability", "Shelf Life | Storage", "Q1"),
        ("6. Safety and Efficacy", "06", "Safety & Efficacy", "Nonclinical | Clinical", "M3 S E"),
        ("7. Regulatory Documentation", "07", "Regulatory Docs", "CTD | DMF | QOS", "M4 PQ/CMC"),
        ("8. Risk and Lifecycle", "08", "Risk & Lifecycle", "QRM | CAPA | Change", "Q9 Q10 Q12"),
        ("9. FDA Modernization", "09", "FDA Modernization", "Structured Data | AI | NAMs", "FDA ICH"),
    ]

    top_row = st.columns(4)
    for index, node in enumerate(map_nodes[:4]):
        category, number, title, objects, guides = node
        with top_row[index]:
            st.markdown(
                f"""
                <div class="ontology-node-card">
                    <div class="node-number">{number}</div>
                    <h3>{title}</h3>
                    <p>{objects}</p>
                    <span>Guideline: {guides}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Open Detail", key=f"map_node_{category}"):
                open_category(category)

    st.markdown(
        """
        <div class="map-midline">
            <span>Time-based proof</span>
            <span>Benefit-risk</span>
            <span>Submission</span>
            <span>Change control</span>
            <span>Modern evidence</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    bottom_row = st.columns(5)
    for index, node in enumerate(map_nodes[4:]):
        category, number, title, objects, guides = node
        with bottom_row[index]:
            st.markdown(
                f"""
                <div class="ontology-node-card compact">
                    <div class="node-number">{number}</div>
                    <h3>{title}</h3>
                    <p>{objects}</p>
                    <span>Guideline: {guides}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
            if st.button("Open Detail", key=f"map_node_{category}"):
                open_category(category)


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
    .navigator-hero {
        position: relative;
        overflow: hidden;
        background:
            linear-gradient(135deg, rgba(18, 61, 97, 0.96) 0%, rgba(23, 33, 38, 0.97) 48%, rgba(27, 139, 105, 0.94) 100%);
        color: white;
        padding: 2rem 2.2rem 1.4rem 2.2rem;
        border-radius: 0.8rem;
        border: 1px solid #1f4f5b;
        box-shadow: 0 22px 48px rgba(8, 32, 51, 0.16);
        margin-bottom: 1rem;
    }
    .navigator-hero:before {
        content: "";
        position: absolute;
        right: -8rem;
        top: -9rem;
        width: 24rem;
        height: 24rem;
        border-radius: 50%;
        background: rgba(242, 200, 75, 0.13);
    }
    .navigator-kicker {
        display: inline-block;
        background: rgba(255, 255, 255, 0.12);
        border: 1px solid rgba(255, 255, 255, 0.22);
        color: #d8edf6;
        padding: 0.3rem 0.6rem;
        border-radius: 999px;
        font-size: 0.78rem;
        font-weight: 900;
        text-transform: uppercase;
    }
    .navigator-hero h1 {
        position: relative;
        margin: 0.75rem 0 0.45rem 0;
        color: white;
        font-size: 3rem;
        line-height: 1.05;
    }
    .navigator-hero p {
        position: relative;
        max-width: 860px;
        color: #d6e4df;
        font-size: 1.05rem;
        margin: 0 0 1.1rem 0;
    }
    .hero-flow, .flow-spine, .map-midline {
        display: grid;
        align-items: center;
        gap: 0.55rem;
    }
    .hero-flow {
        grid-template-columns: auto 1fr auto 1fr auto 1fr auto 1fr auto;
        position: relative;
        max-width: 960px;
    }
    .hero-flow span, .flow-spine span, .map-midline span {
        display: inline-grid;
        place-items: center;
        min-height: 2rem;
        border-radius: 999px;
        font-weight: 900;
        white-space: nowrap;
    }
    .hero-flow span {
        background: rgba(255, 255, 255, 0.14);
        color: white;
        padding: 0.35rem 0.7rem;
        border: 1px solid rgba(255, 255, 255, 0.22);
    }
    .hero-flow i, .flow-spine i {
        height: 0.35rem;
        border-radius: 999px;
        background: linear-gradient(90deg, #f2c84b 0%, #1b8b69 100%);
    }
    .map-section {
        margin: 1rem 0 0.65rem 0;
        padding: 0.8rem 1rem;
        border-radius: 0.65rem;
        background: #f8fbfc;
        border: 1px solid #cddce3;
        display: flex;
        justify-content: space-between;
        gap: 1rem;
        align-items: center;
    }
    .map-section span {
        color: #17364a;
        font-size: 1.1rem;
        font-weight: 950;
    }
    .map-section b {
        color: #536064;
        font-size: 0.9rem;
    }
    .map-section.ontology {
        background: linear-gradient(135deg, #fffdf8 0%, #eef6f1 100%);
        border-color: #d9d1c1;
    }
    .flow-spine {
        grid-template-columns: auto 1fr auto 1fr auto 1fr auto 1fr auto;
        margin: 0.7rem 0 0.9rem 0;
        padding: 0.7rem 0.9rem;
        border-radius: 999px;
        background: #172126;
    }
    .flow-spine span {
        background: #ffffff;
        color: #17364a;
        padding: 0.25rem 0.55rem;
        font-size: 0.82rem;
    }
    .map-midline {
        grid-template-columns: repeat(5, 1fr);
        margin: 0.7rem 0;
    }
    .map-midline span {
        background: #e8f1f8;
        color: #236b9a;
        padding: 0.35rem 0.4rem;
        font-size: 0.78rem;
    }
    .mini-map-card, .ontology-node-card {
        border: 1px solid #cddce3;
        background: linear-gradient(135deg, #ffffff 0%, #f8fbfc 100%);
        border-radius: 0.7rem;
        padding: 0.9rem 0.95rem;
        min-height: 6.2rem;
        box-shadow: 0 12px 24px rgba(23, 33, 38, 0.07);
        margin-bottom: 0.35rem;
    }
    .mini-map-card b {
        display: block;
        color: #172126;
        font-size: 1rem;
        line-height: 1.15;
    }
    .mini-map-card span {
        display: inline-block;
        margin-top: 0.55rem;
        color: #1f6f55;
        font-size: 0.82rem;
        font-weight: 900;
    }
    .ontology-node-card {
        min-height: 9.2rem;
        position: relative;
        overflow: hidden;
    }
    .ontology-node-card:before {
        content: "";
        position: absolute;
        right: -2.8rem;
        top: -2.8rem;
        width: 7rem;
        height: 7rem;
        border-radius: 50%;
        background: rgba(46, 113, 94, 0.11);
    }
    .ontology-node-card .node-number {
        display: inline-grid;
        place-items: center;
        width: 2.4rem;
        height: 2.4rem;
        border-radius: 50%;
        background: #172126;
        color: white;
        font-weight: 950;
        margin-bottom: 0.55rem;
    }
    .ontology-node-card h3 {
        margin: 0;
        font-size: 1.02rem;
        color: #172126;
    }
    .ontology-node-card p {
        margin: 0.5rem 0 0.45rem 0;
        color: #536064;
        font-size: 0.86rem;
        line-height: 1.25;
    }
    .ontology-node-card span {
        display: inline-block;
        color: #236b9a;
        background: #e8f1f8;
        border-radius: 999px;
        padding: 0.25rem 0.5rem;
        font-size: 0.75rem;
        font-weight: 900;
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
        min-height: 2.7rem;
        border-radius: 0.7rem;
        border: 1px solid #cddce3;
        background: linear-gradient(135deg, #ffffff 0%, #f8fbfc 100%);
        color: #1d2528;
        text-align: center;
        padding: 0.45rem 0.75rem;
        line-height: 1.22;
        font-weight: 900;
        box-shadow: 0 12px 24px rgba(23, 33, 38, 0.07);
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
    .finder-panel {
        border: 1px solid #cddce3;
        background: #f8fbfc;
        padding: 1rem 1.05rem;
        margin: 0.8rem 0 1rem 0;
        border-radius: 0.65rem;
    }
    .finder-panel h3 {
        margin: 0 0 0.35rem 0;
        font-size: 1.15rem;
    }
    .finder-panel p {
        margin: 0 0 0.65rem 0;
        color: #536064;
        font-size: 0.95rem;
    }
    .result-card {
        border: 1px solid #d9d1c1;
        background: #fffdf8;
        padding: 0.8rem 0.9rem;
        border-radius: 0.55rem;
        margin-bottom: 0.65rem;
    }
    .result-card b {
        color: #172126;
    }
    .result-card span {
        display: inline-block;
        margin-top: 0.35rem;
        color: #1f6f55;
        font-size: 0.82rem;
        font-weight: 800;
    }
    .case-panel {
        border: 1px solid #c9dce6;
        background: linear-gradient(135deg, #f8fbfc 0%, #eef6f1 100%);
        padding: 1rem 1.1rem;
        margin: 0.8rem 0 1rem 0;
        border-radius: 0.65rem;
    }
    .case-panel h3 {
        margin: 0 0 0.45rem 0;
        font-size: 1.15rem;
    }
    .case-panel p {
        color: #536064;
        margin: 0.3rem 0;
        line-height: 1.42;
    }
    .case-signal {
        display: inline-block;
        margin: 0.18rem;
        padding: 0.28rem 0.55rem;
        border-radius: 999px;
        background: #e7f2ec;
        color: #1f6f55;
        font-size: 0.8rem;
        font-weight: 800;
    }
    .playbook-panel {
        border: 1px solid #b8d1df;
        background: linear-gradient(135deg, #edf6fb 0%, #f7fbfc 46%, #eef6f1 100%);
        padding: 1rem 1.1rem;
        margin: 0.8rem 0 1rem 0;
        border-radius: 0.65rem;
    }
    .playbook-panel h3 {
        margin: 0 0 0.3rem 0;
        font-size: 1.2rem;
    }
    .playbook-panel p {
        color: #536064;
        margin: 0.25rem 0 0.7rem 0;
        line-height: 1.42;
    }
    .playbook-chip {
        display: inline-block;
        background: #e8f1f8;
        color: #236b9a;
        padding: 0.28rem 0.55rem;
        margin: 0.15rem;
        font-size: 0.8rem;
        font-weight: 800;
        border-radius: 999px;
    }
    .landing-note {
        color: #536064;
        font-size: 0.95rem;
        font-weight: 800;
        margin: 0.85rem 0 0.45rem 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


query_category = st.query_params.get("category")
query_item = st.query_params.get("item")
query_playbook = st.query_params.get("playbook")
if query_category in ONTOLOGY:
    st.session_state.category = query_category
else:
    render_process_image()
    render_landing_navigation()
    st.stop()


if st.button("Back to Ontology Map"):
    for key in list(st.query_params.keys()):
        del st.query_params[key]
    st.rerun()

with st.sidebar:
    st.header("Ontology Menu")
    st.subheader("Situation Finder")
    for playbook_key, playbook in SITUATION_PLAYBOOKS.items():
        if st.button(playbook["label"], key=f"side_playbook_{playbook_key}"):
            open_playbook(playbook_key)
    st.divider()
    category = st.radio(
        "Development process",
        list(ONTOLOGY.keys()),
        index=list(ONTOLOGY.keys()).index(st.session_state.category),
        label_visibility="collapsed",
    )
    st.session_state.category = category
    st.query_params["category"] = category
    available_items = list(ONTOLOGY[category]["items"].keys())
    item_index = available_items.index(query_item) if query_item in available_items else 0
    item = st.selectbox("Ontology item", available_items, index=item_index)
    st.query_params["item"] = item
    st.divider()
    st.caption("Use the menu above as the ontology tree. The selected item opens its detail page.")


category_data = ONTOLOGY[category]
item_data = category_data["items"][item]
active_playbook = SITUATION_PLAYBOOKS.get(query_playbook)

st.markdown(
    """
    <div class="finder-panel">
        <h3>Quick Finder</h3>
        <p>Search the ontology while developing a drug: CQA, DMF, impurity, analytical method, shelf life, QRM, PQ/CMC, NAMs, AI credibility.</p>
    </div>
    """,
    unsafe_allow_html=True,
)
search_term = st.text_input(
    "Find ontology item",
    placeholder="Type a need, evidence item, CTD section, or guideline...",
    label_visibility="collapsed",
)
if search_term:
    results = search_ontology(search_term)[:6]
    if results:
        result_columns = st.columns(2)
        for index, (_, result_category, result_item, result_data) in enumerate(results):
            with result_columns[index % 2]:
                st.markdown(
                    f"""
                    <div class="result-card">
                        <b>{result_item}</b><br>
                        <span>{result_category} · {' / '.join(result_data["guidelines"][:3])}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Open", key=f"open_result_{index}_{result_category}_{result_item}"):
                    st.query_params["category"] = result_category
                    st.query_params["item"] = result_item
                    st.rerun()
    else:
        st.info("No ontology item matched that search term.")

if active_playbook:
    st.markdown(
        f"""
        <div class="playbook-panel">
            <h3>{active_playbook["label"]}</h3>
            <p>{active_playbook["lead"]}</p>
            <p><b>Decision:</b> {active_playbook["decision"]}</p>
            {" ".join([f"<span class='playbook-chip'>{guide}</span>" for guide in active_playbook["guidelines"]])}
            {" ".join([f"<span class='playbook-chip'>{section}</span>" for section in active_playbook["ctd"]])}
        </div>
        """,
        unsafe_allow_html=True,
    )
    playbook_check_col, playbook_evidence_col = st.columns(2)
    with playbook_check_col:
        render_list_card("Manufacturing Checklist", active_playbook["checklist"])
    with playbook_evidence_col:
        render_list_card("Evidence Basket", active_playbook["evidence"])

st.markdown(
    f"""
    <div class="case-panel">
        <h3>Process Case Lens: {CASE_STUDY["title"]}</h3>
        <p>{CASE_STUDY["category_links"].get(category, CASE_STUDY["summary"])}</p>
        <p><b>Decision lens:</b> {CASE_STUDY["decision"]}</p>
        {" ".join([f"<span class='case-signal'>{signal}</span>" for signal in CASE_STUDY["signals"]])}
    </div>
    """,
    unsafe_allow_html=True,
)

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
