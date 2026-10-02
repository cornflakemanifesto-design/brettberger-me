# brettberger.me

Personal landing page — links to projects, writing, and profiles. FastAPI + Jinja2, content-managed through a password-protected admin page (same pattern as the All Creatures of Pikes Peak site).

## Editing content

Visit `/admin` on the live site (or `http://localhost:8000/admin` locally) and sign in with the `ADMIN_PASSWORD` env var. From there you can edit:
- Name, avatar initials, tagline, footer name
- Every link (title, subtitle, URL) — add or remove rows freely
- The full color scheme, separately for light and dark mode

Changes save to `content.json` immediately — no redeploy needed. "Reset to defaults" restores everything from `content_seed.json`.

## Running locally

```
pip install -r requirements.txt
ADMIN_PASSWORD=whatever uvicorn main:app --reload
```

Then open `http://localhost:8000`.

## Deploying

Deployed on Render (`render.yaml` included) at the same account as the other projects. `ADMIN_PASSWORD` is set in the Render dashboard's environment variables (not committed). `content.json` lives on a persistent disk so edits survive deploys.

Custom domain `brettberger.me` points at this Render service — DNS is managed at GoDaddy.
