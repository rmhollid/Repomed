# RepoMedic — Devpost Submission Draft

## Tagline
An evidence-driven repair agent that proves its fixes by rerunning the code.

## Inspiration
Software-repair agents are useful only when their actions are inspectable and their claims can be validated. RepoMedic was built around a simple rule: diagnosis is not enough; the agent must act, and the resulting code must prove the repair.

## What it does
RepoMedic operates on a deliberately broken demonstration repository. It runs the unit tests to collect real failure evidence, generates a bounded set of auditable candidate patches, and gives Gemini 3.5 Flash the source, test evidence, and candidate diffs. Gemini selects the repair supported by the evidence. RepoMedic then applies that patch in an isolated workspace and executes the same test suite again.

The result page shows the complete action trace, Gemini's diagnosis and decision, the exact unified diff, and the before/after test output.

## How we built it
RepoMedic is a Python/Flask service deployed on Google Cloud Run. Gemini 3.5 Flash is invoked through the Google GenAI SDK. Deterministic Python tools perform repository copying, test execution, candidate-patch construction, patch application, and validation. Gemini performs the reasoning step that connects failure evidence to the appropriate repair action.

This separation keeps the system auditable: language-model judgment chooses an action, while deterministic tools execute and verify it.

## Google technologies used
- Gemini 3.5 Flash
- Google GenAI SDK
- Google Cloud Run
- Cloud Build / Artifact Registry as part of Cloud Run source deployment

## Challenges
The main design challenge was making a small agentic workflow both reliable and honest. Instead of letting the model freely rewrite arbitrary code, RepoMedic constrains the repair surface and exposes the evidence that led to the action. The public demo also avoids executing arbitrary uploaded code.

## Accomplishments
- Full diagnosis → action → verification cycle
- Real unit tests before and after repair
- Explicit patch diff
- Google-hosted live proof of action
- Narrow public execution surface for reproducibility and safety

## What we learned
Agentic software does not need a massive tool surface to demonstrate meaningful autonomy. A small system can be convincing when each action has evidence, a clear state transition, and an objective validation step.

## What's next
The next version would add sandboxed arbitrary-repository analysis, broader candidate-generation tools, multi-file repairs, and repository integrations while retaining the same evidence-first validation contract.

## AI assistance disclosure
AI coding assistance was used in creating the new contest project. The submitted application itself uses Gemini 3.5 Flash through Google's GenAI SDK as an explicit runtime reasoning component.
