# GitHub — deploy profile magic

## 1. Push portfolio updates (CI + capstone)

```bash
cd genai-portfolio-five
git add .
git commit -m "Add agentic capstone, production API patterns, golden evals CI"
git push origin main
```

After push, open **Actions** tab — **Golden evals** should pass. Badge appears in README within a few minutes.

## 2. Profile README repo

Follow [../github-profile/PUSH-TO-GITHUB.md](../github-profile/PUSH-TO-GITHUB.md).

## 3. Pin six repos (github.com/divyapasupuleti → Customize your pins)

| # | Repository | Notes |
|---|------------|--------|
| 1 | **genai-portfolio-five** | Main portfolio |
| 2 | **divyapasupuleti** | Profile README (after you create it) |
| 3–6 | Your next public repos | Prefer active; archive stale WIP |

If you only maintain the portfolio, **one strong pin** beats six weak ones.

## 4. Topics on `genai-portfolio-five`

Settings → General → Topics:

`rag` `llm` `generative-ai` `agents` `fastapi` `mlops` `evaluation` `azure-openai` `python` `ireland`

## 5. LinkedIn

Use [../LINKEDIN-FEATURED.md](../LINKEDIN-FEATURED.md).

## 6. Resume PDF

```bash
cd interview-prep/docs
.venv/bin/python generate_agentic_fde_resume_pdf.py
```

Upload PDF to LinkedIn Featured.
