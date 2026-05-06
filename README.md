# Pharmaceutical Development Ontology

An English Streamlit app for exploring the pharmaceutical development process as an ontology.

The app provides a clickable process menu and detailed pages for each ontology item, including:

- A modern SVG-based visual ontology evidence map at the top of the app
- Concrete sub-concepts inside each process node, such as CQA, CPP, specifications, methods, CTD, DMF, PQ-CMC, NAMs, and AI
- Stage selector cards for moving through the development process
- Definition and detailed information
- Key data elements
- CTD / evidence location
- Related ICH and FDA guidelines
- Guideline rationale explaining why each guideline applies
- Ontology relationship examples

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repository.
2. Go to https://share.streamlit.io/.
3. Select the repository, branch, and `app.py`.
4. Deploy.
