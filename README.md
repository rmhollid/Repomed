# RepoMedic

RepoMedic is a deliberately narrow, evidence-driven software repair agent built for the 2026 All Things Agentic Hackathon.

## What it does

A single click launches a complete repair workflow against a bundled broken Python repository:

1. creates an isolated working copy;
2. runs the repository's real unit tests;
3. captures the failure;
4. generates a bounded set of auditable candidate patches;
5. sends the source, failure evidence, and candidates to Gemini 3.5 Flash;
6. Gemini selects the repair it believes is supported by the evidence;
7. RepoMedic applies only that selected patch;
8. RepoMedic runs the real tests again;
9. the UI displays the action trace, diagnosis, patch diff, and before/after validation.

This demonstrates action rather than chat: the agent changes executable state and validates the consequence.

## Required Google technologies

- **Gemini 3.5 Flash** (`gemini-3.5-flash`)
- **Google GenAI SDK** (`google-genai`)
- **Google Cloud Run**

## Local validation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python validate.py
```

## Local live run

```bash
export GEMINI_API_KEY="YOUR_KEY"
gunicorn --bind :8080 --workers 1 --threads 8 --timeout 120 app:app
```

Open `http://localhost:8080`.

## Cloud Run deployment

Prerequisites:

- authenticated `gcloud` CLI;
- a Google Cloud project;
- Gemini API key;
- billing/API access required by your Google Cloud account.

```bash
export GOOGLE_CLOUD_PROJECT="YOUR_PROJECT_ID"
export GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
chmod +x deploy.sh
./deploy.sh
```

The script enables Cloud Run, Cloud Build, and Artifact Registry, then deploys from source and prints the public service URL.

## Architecture

See `submission/ARCHITECTURE.svg`.

## Security scope

The public contest demo intentionally does **not** execute arbitrary user-uploaded repositories. It operates only on the bundled demonstration repository copied into a temporary workspace for each run. This keeps the public proof-of-action narrow and reproducible.

## New-work disclosure

RepoMedic was created as a new standalone contest entry. The implementation uses standard open-source dependencies and the Google GenAI SDK. AI coding assistance may be disclosed in the final competition submission as required by the competition rules.

## License

MIT
