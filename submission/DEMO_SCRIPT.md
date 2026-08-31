# RepoMedic Demo Script — target: ~2 minutes

1. **Opening — 10 sec**
   “This is RepoMedic, an evidence-driven repair agent running on Google Cloud Run.”

2. **Show Cloud Run — 15 sec**
   Briefly show the Cloud Run service page or service URL.
   Show that the live service is deployed.

3. **Explain the workflow — 15 sec**
   “The bundled repository has a real bug. RepoMedic first runs its tests instead of asking the model to guess.”

4. **Run the agent — 45 sec**
   Open the live `.run.app` page.
   Click **Run repair agent**.
   Keep the execution continuous and unedited.

5. **Show proof — 25 sec**
   Point out:
   - action trace;
   - Gemini 3.5 model;
   - diagnosis;
   - selected patch;
   - failing test output before;
   - passing test output after.

6. **Architecture — 10 sec**
   Show `ARCHITECTURE.svg`.
   “Cloud Run hosts the service. Deterministic Python tools execute and validate actions. Gemini, through Google’s GenAI SDK, chooses the evidence-supported repair.”

7. **Close — 5 sec**
   “RepoMedic does not merely recommend a fix. It acts, then proves whether the action worked.”
