# brettberger.me

Personal landing page — links to projects, writing, and profiles. Static HTML/CSS, no build step.

## Editing

Open `index.html`:
- Replace the `[bracketed placeholders]` with your real tagline and links.
- Each link is an `<li>` in the `.links` list — copy/paste one to add more, or delete one you don't need.
- Update the `href="#"` values to real URLs.

Open in a browser directly (double-click `index.html`) to preview changes — no server needed.

## Deploying

Recommended: [Vercel](https://vercel.com) or [Netlify](https://netlify.com) — both have a free tier, auto-deploy on git push, and support custom domains.

1. Push this folder to a GitHub repo.
2. Import the repo in Vercel/Netlify (framework preset: "Other" / static site, no build command, output directory: `/`).
3. In the host's dashboard, add `brettberger.me` as a custom domain.
4. At your domain registrar (GoDaddy), update the DNS records to the ones the host gives you — typically an `A` record for the root domain and a `CNAME` for `www`.

DNS changes can take a few minutes to a few hours to propagate.
