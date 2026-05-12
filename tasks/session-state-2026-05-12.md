# Session state — restart 2026-05-12

Both `magna-park` and `astra-removals` working trees are clean — last
commits already pushed (magna-park HEAD: a92c492 / astra-removals HEAD:
0c1136a). Nothing pending to commit.

## Where we left off

### MAGNA PARK — Google Ads campaign rebuild (PRIMARY current task)

Working through the 4-step Google Ads recovery plan documented in
`tasks/google-ads-progress.md`. State per step:

| Step | Status |
|---|---|
| 1. Install Google Tag on all pages | ✅ DONE — commit 0c2860b. gtag wired on 34 pages routing to AW-18025180682 + GT-T9C7SQKT. |
| 2. Fix call asset disapproval | ✅ Submitted 2026-05-06 — was "Pending - Under review". CHECK FIRST THING NEXT SESSION: ads.google.com → Astra account → Campaigns → Assets → Call. If still pending, ping Google support. If approved, the campaign-level "Limited" warning should clear. |
| 3a. Pause PMax "Rent a Storage Unit Today" | ✅ DONE 2026-05-06 — daily £4.70 spend stopped. |
| 3b. Build new Search campaign in Google Ads Editor | ⏳ IN PROGRESS — see "Editor pickup" below. |
| 4. Claim £380 promo credit | ⏳ NOT STARTED — Billing → Promotions. |

### Editor pickup — where to resume

Google Ads Editor is installed and the Astra Removals account
(503-609-1207) is downloaded. Inside Editor:

- New campaign created: **"Magna Park — Self Storage — Search"**
  - Status: **Paused** (intentional — keep paused until full review)
  - Networks: Google Search only (Display + Search Partners both off)
  - Daily budget: £10
  - Bid strategy: Manual CPC, default max CPC £2.50
  - 10 locations added: Bournemouth, Poole, Christchurch, Wimborne,
    Ferndown, Ringwood, Verwood, New Milton, Southbourne + 5-mile
    radius around BH11 9FA
- New ad group created under it: **"Self Storage Bournemouth (Core)"**
  - Max CPC: £2.50
  - Final URL:
    https://magnaparkselfstore.co.uk/self-storage-bournemouth.html
  - 9 keywords pending — Ricky abandoned the bulk-paste route after
    "Not importing" dropdown issue. Last instruction was "add them
    one at a time via + Add Keyword". Status when paused: keywords
    list showed 0 entries.
- RSA: NOT YET BUILT — Step 7 instructions still valid (15 headlines +
  4 descriptions pre-trimmed to fit Google's char limits, with pin
  positions for #1/#5/#15). Content lives in chat history; copy
  also at the master blueprint in repo:
  `magna-park/GOOGLE-ADS-CAMPAIGN.md`.
- Campaign-level negative keywords: NOT YET ADDED. List of ~24
  negatives in the blueprint.
- **Reminder**: after posting from Editor, set the campaign's
  Location options to "Presence: People in or regularly in your
  targeted locations" via the live web UI (it's a hidden setting
  in Editor). Default is "Presence or Interest" which is bad.

### MAGNA PARK — sister tracks (not changed this session)

- Static HTML site on Netlify, auto-deploys from `main` branch of
  github.com/Rickybarton138/MAGNA-PARK
- `auto-poster.py` runs 5x/week from Windows Task Scheduler via
  social-media-agent `.env`
- `ACTION-PLAN.md` lists 7 customer-acquisition steps, top one is
  the Google Ads verification deadline (originally 2026-05-13 —
  CHECK IF THIS PASSED. If ads paused, that's a separate fire to
  fight)

### ASTRA REMOVALS — separate workstream (latest activity)

Last commit `0c1136a` ("Audit findings: rotate leaked credentials,
fix env + dep gaps"). Multiple feature commits in this repo since
my last direct involvement:
- New /quote/{token}/confirm-date public form for customer date
  confirmation
- WhatsApp message body logging (whatsapp_logs.body column)
- MOD movements gained service_person_email/phone columns
- Quote attribution column (gclid / utm tracking)
- Several CRM UX iterations (tabbed customer detail, calendar view,
  filter-pill counts, action-first dashboard)

NO known outstanding Ricky-side asks on astra-removals as of this
restart. Stripe balance flow + WhatsApp media ingest both shipped
weeks ago.

## Pick-up checklist when resuming

1. Read this file
2. Check current state of the disapproved call asset in Google Ads
3. Open Google Ads Editor — should re-open with the in-progress
   "Magna Park — Self Storage — Search" campaign intact (Editor
   persists drafts locally)
4. Resume from "add 9 keywords manually" → then RSA → then
   campaign-level negatives → then "Post" button → then web-UI
   targeting-type fix
5. After posting + targeting fix, claim £380 promo credit

## Outstanding session memory

- Ricky has Google Ads Editor v2.12.6 installed and signed in with
  astraremovals@gmail.com
- Twilio Auth Token used earlier in chat: 1f55bd3ba00211189d398fd27a196b3d
  — this should be rolled when convenient (Console → Account → API
  Keys & Tokens → Roll). Not urgent.
