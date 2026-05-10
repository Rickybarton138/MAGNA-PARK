# Google Ads Analysis — Pick up next session

## TL;DR — what we found
Magna Park's "Rent a Storage Unit Today" campaign is **a Performance Max** (PMax) sitting inside the **Astra Removals Google Ads account** (Customer ID `503-609-1207`, login `astraremovals@gmail.com`). It is NOT in a separate Magna Park account — that's why we couldn't find it earlier. The "Customer ID 895-216-2424" memory note was stale/wrong.

## Last 30 days performance (Apr 6 - May 5, 2026)
- Spend: **£140.46** (~£4.70/day, hitting daily budget cap)
- Impressions: 110,508
- Clicks: 795
- CTR: **0.72%** (poor — Search storage ads typically 3-5%)
- Avg CPC: **£0.18** (suspiciously cheap → mostly Display/YouTube clicks, not Search intent)
- **Conversions: 0** (because tracking isn't installed on the Magna Park site)
- Status: **Eligible (Limited)** — limited because **call asset is disapproved**

## Key diagnoses
1. **PMax is wrong campaign type** for a small local storage business. ~80% of impressions are Display/YouTube/Gmail filler, not real searchers. Search-only campaign would convert 5-10× better.
2. **No conversion tracking on magnaparkselfstore.co.uk** — Google has flagged "Install a Google tag on www.magnaparkselfstore.co.uk". Zero of 30 HTML pages have any gtag.
3. **Call asset disapproved** — limits delivery, easy fix in the Ads UI (Assets section).
4. **£380 promo credit pending** — unclaimed free spend.
5. Astra's own conversion tracking IS working: 73 quote requests + 4 phone call leads tracked in the same 30-day window.

## 4-step recommended plan

### 1. Install Google tag on Magna Park (BLOCKED on getting the ID)
- Need: AW conversion ID + label for the "Sign-up" conversion (currently flagged Misconfigured)
- Path in Ads: Goals → Conversions → Summary → click "Sign-up" row → "Tag setup" / "Use Google tag" → copy code snippet starting `gtag('event', 'conversion', {'send_to': 'AW-XXXXXXXXX/YYYYYYYY'});`
- Once Ricky pastes the snippet, Claude installs it across all 30 HTML pages (root + blog/), commits + pushes
- Conversion actions to consider for the static site: phone clicks on tel: links + "get directions" clicks (no form yet)

### 2. Fix the call asset disapproval
- In Ads UI: Assets → find the disapproved Call asset → click → fix issue (usually re-verify phone number ownership via SMS/voice code)
- This unblocks the campaign from "Limited" status

### 3. Decide on PMax → Search migration
- Pause "Rent a Storage Unit Today" PMax campaign
- Build proper Search campaign per `magna-park/GOOGLE-ADS-CAMPAIGN.md` blueprint (already documented — 6 ad groups, full negative keyword list, RSA copy ready to paste)
- Same £4.70/day budget would buy ~70 high-intent Search clicks at £2 each instead of 800 Display garbage clicks at 18p

### 4. Activate £380 promo credit
- Path: Billing → Promotions → claim. Free money sitting there.

## Where we left off
Last instruction Ricky was acting on: in Ads UI at Goals → Conversions → Summary, list shows:
- Sign-up — **Misconfigured** ← need to click this and screenshot the Tag setup page
- Phone call lead — Active
- Contact — Active
- Request quote — Active
- Get directions — Active

When Ricky resumes, the next click is: **click on "Sign-up" → screenshot the Tag setup page** so Claude can grab the AW-.../... ID and install the gtag.

## Side issues to flag tomorrow
- **Google Ads advertiser verification deadline is 2026-05-13** (per `ACTION-PLAN.md` + global memory). 7 days from today. If verification isn't started this week, ads pause when the deadline hits.
- Conversion action name "Sign-up" is misleading for a storage business — should probably be renamed to "Storage enquiry" or "Phone tap" once tracking is wired.

## Files this session touched
- Created `magna-park/CLAUDE.md` — project agent instructions (committed `398829d`)
- Created `magna-park/tasks/google-ads-analysis-2026-05-05.md` — this file
- Existing `magna-park/GOOGLE-ADS-CAMPAIGN.md` is the Search-campaign blueprint we'd execute in step 3
