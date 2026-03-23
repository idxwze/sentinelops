# SentinelOps

SentinelOps is a polished Gradio MVP for an AI Incident Copilot focused on reliability and security triage. It is designed as a high-fidelity university UI/UX prototype that also feels credible enough for a portfolio, internship, or CV showcase.

## What it does

- Presents a realistic on-call dashboard with a three-panel incident response layout
- Lets the user select mock incidents and inspect service health, summaries, and live-looking operational metrics
- Visualizes time-series signals for latency, error rate, CPU, and request volume
- Surfaces ranked incident hypotheses with confidence and next recommended checks
- Includes a deterministic AI-style copilot chat tied to the selected incident
- Supports English and French UI labels
- Includes accessibility-oriented controls for text size and high-contrast viewing
- Uses only mock JSON data so it is easy to run, review, and extend

## Why this project

This MVP explores how AI-assisted incident response can be presented in a way that supports fast understanding instead of generic chat. The product direction is aimed at junior SRE and DevOps users who need help identifying likely causes, affected systems, and the safest next action during an incident.

## Portfolio-ready summary

SentinelOps is an AI incident triage dashboard prototype that combines observability views, incident hypotheses, dependency impact mapping, and an assistant-style analysis panel into a single internal-tool experience. The interface demonstrates product thinking, systems awareness, bilingual UX support, accessibility considerations, and high-fidelity dashboard design using Python and Gradio.

## Project structure

```text
sentinelops/
├── app.py
├── requirements.txt
├── README.md
└── data/
    ├── incidents.json
    ├── metrics.json
    └── hypotheses.json
```

## Local setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app locally:

```bash
python app.py
```

4. Open the local Gradio URL shown in the terminal.

## Hugging Face Spaces deployment

This project is compatible with Hugging Face Spaces using the Gradio SDK.

- Upload the repository contents to a new Gradio Space
- Keep `app.py` at the repository root
- Keep `requirements.txt` at the repository root
- Ensure the `data/` folder is committed with the JSON mock data

Gradio Spaces will install the dependencies from `requirements.txt` and launch the app automatically.

## Notes for extension

- Replace the deterministic copilot logic with a real LLM backend later if needed
- Move data-loading, charting, and i18n helpers into separate modules once the MVP grows
- Add incident timelines, annotation layers, and user journey flows for deeper coursework evaluation
