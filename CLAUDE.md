# Magna Park Self Store — Project Agent Instructions

## Identity
**Project:** Magna Park Self Store — Bournemouth container self-storage marketing site + 5x/week social-media autoposter.
**Owner:** Ricky (rickybarton138@btinternet.com)
**Sister project:** `~/magna-park-crm` — Next.js + Supabase + Stripe booking/CRM stack (separate repo).
**Live URL:** magnaparkselfstore.co.uk (likely — check with deploy host before assuming)
**Google Business Profile:** active — posts in `gbp-posts/` are seeded by the auto-poster
**Google Ads Customer ID:** `457-230-3566` (login `magnaparkselfstore@gmail.com` — dedicated account, live + serving as of 2026-06-07; old IDs `895-216-2424` and Astra's `503-609-1207` are superseded). See global memory `magna-park-google-ads.md`

## Tech Stack
- **Marketing site:** static HTML / vanilla CSS / minimal JS — no framework, no build step. Hosted (likely Netlify or GitHub Pages — confirm via DNS + repo settings before deploying)
- **Pages:** `index.html` plus a fan of intent-based SEO landing pages (`*-storage-bournemouth.html`, `container-storage-dorset.html`, `house-move-storage-bournemouth.html`, etc.) and a `blog/` directory
- **Social autoposter:** `auto-poster.py` — Python 3 + `requests` + OpenAI for content + Meta Graph API for FB/IG. 5 content pillars, smart rotation, branded image generation, GBP-text output. Runs locally via Windows Task Scheduler (5×/week)
- **Credentials:** loaded from this project's own `~/magna-park/.env` (gitignored — see `.env.example`), keys: `META_PAGE_ACCESS_TOKEN`, `OPENAI_API_KEY`. The Facebook Page ID + Instagram account ID are hardcoded in `auto-poster.py` so no env var can redirect posts to the wrong account. Do NOT point the poster at the shared `~/social-media-agent/.env` — that file is used by other projects and once caused Magna Park posts to publish to the wrong Facebook page.
- **State:** `post-log.json` tracks past posts to avoid pillar/topic repetition
- **Generated artefacts:** `gbp-posts/*.txt` (per-day GBP post bodies), `social-images/*.png` (branded 1080×1080 images committed for traceability)

## Architecture
| Area | Where |
|---|---|
| Hero / lead pages | `index.html`, intent-based `*-bournemouth.html` files |
| Long-form content | `blog/` |
| Press / partnerships | `PRESS-RELEASE.md`, `REMOVAL-PARTNERSHIPS.md` |
| GBP listing | `GBP-LISTING-CONTENT.md`, `GBP-QA-SEEDING.md`, `gbp-posts/` |
| Action plan | `ACTION-PLAN.md` (7 prioritised customer-acquisition steps) |
| Submissions | `DIRECTORY-SUBMISSIONS.md` (citation/directory tracking) |
| SEO meta | `robots.txt`, `llms.txt`, `BingSiteAuth.xml`, `google0f5f5cc1b247f8c4.html` |

## Conventions
- HTML pages share the same brand colours and shell — duplicate the structure of an existing `*-storage-bournemouth.html` when adding a new landing page
- Page meta: title ≤ 60 chars, meta-description ≤ 155 chars, canonical pointing at the live domain
- Schema.org `SelfStorage` / `LocalBusiness` JSON-LD on every public page
- All commits should keep generated images alongside the code that produced them — the auto-poster commits its own `social-images/*.png` to the repo
- New SEO landing pages must be linked from `index.html` so they're crawlable

## Auto-poster (`auto-poster.py`)
- Entry: `python auto-poster.py --day mon|tue|wed|thu|fri` (one post per day, picks from 5 content pillars)
- Dry-run: `--dry-run` generates content + image without posting
- Schedule helper: `--schedule` prints Windows Task Scheduler setup commands
- All generated content is logged to `post-log.json` with hash of the topic so the next 4 weeks of runs avoid repetition
- Both Facebook + Instagram are posted in the same run; GBP post text is written to `gbp-posts/YYYYMMDD-<pillar>-gbp.txt` for manual paste (Meta API doesn't cover GBP from a 3rd-party app, so admin pastes those by hand or via the Google Business Profile MCP)

## Past lessons / gotchas
- Windows console encoding: `auto-poster.py` calls `sys.stdout.reconfigure(encoding="utf-8")` — keep it
- Meta tokens expire — when posts start failing with 190/200 codes, refresh `META_PAGE_ACCESS_TOKEN` in `~/magna-park/.env`
- Don't commit `.env` — credentials live in `~/magna-park/.env` (gitignored) and are loaded at runtime
- Local-only SQLite / browser caches don't apply here (static site)

## Agent Behaviour Rules
1. **Plan mode default** — enter plan mode for any 3+ step task (new landing page series, SEO migration, restructuring the auto-poster). Stop and re-plan on failure. Simple typo fix → just fix.
2. **Subagent strategy** — offload research/exploration to Explore agents; one focused task per subagent.
3. **Self-improvement loop** — after any user correction, append the lesson to `tasks/lessons.md` and check it at the start of each session.
4. **Verification before done** — for any deploy, hit the live URL and confirm changes rendered. For auto-poster changes, run `--dry-run` first before letting a real post fire.
5. **Demand elegance (balanced)** — challenge hacky solutions on non-trivial changes; for one-off content tweaks just ship.
6. **Autonomous bug fixing** — fix from logs/errors with zero context switching from Ricky.

## Task Management
- `tasks/todo.md` — current work + plans
- `tasks/lessons.md` — captured corrections / gotchas

## Core Principles
- **Simplicity first** — minimise code impact; this is a static site, don't over-engineer.
- **No laziness** — find root causes; senior-level standards on anything that ships to production.
- **One source of truth** — page copy lives in HTML, social copy lives in `auto-poster.py` content pillars, listing copy in `GBP-LISTING-CONTENT.md`. Don't fork these.
- **Sister-project aware** — the CRM/booking flow is in `~/magna-park-crm` (Next.js). Public-facing booking buttons on this site link to that domain — don't reimplement booking here.
