# Google Ads — Magna Park progress

Last updated: 2026-05-06

## Account
- Customer ID: **503-609-1207** (Astra Removals — Magna Park campaign lives inside it, NOT a separate account)
- Login: astraremovals@gmail.com
- Conversion tag ID: AW-18025180682 / Google Tag: GT-T9C7SQKT

## Campaign: "Rent a Storage Unit Today"
- Type: Performance Max (will be replaced — see plan below)
- **Status: PAUSED** as of 2026-05-06
- Last 30-day perf before pause: £140.46 / 795 clicks / 110,508 impr / 0.72% CTR / £0.18 avg CPC / 0 tracked conversions
- Diagnosis: PMax wrong type for small local storage; ~80% of impressions are Display/YouTube garbage

## 4-step recovery plan

### ✅ 1. Install Google Tag on all pages — DONE 2026-05-05 (commit 0c2860b)
gtag installed on 34 HTML pages routing to AW-18025180682 + GT-T9C7SQKT.

### ✅ 2. Fix call asset disapproval — Submitted 2026-05-06
- Deleted disapproved asset
- Re-attached existing call asset to "Rent a Storage Unit Today" campaign
- Status: **Pending - Under review** at 9:33 AM
- If approved within 24h → done
- If rejected → manual voice-verify with auto-answer turned off (Option A from chat)

### ✅ 3a. Pause PMax campaign — DONE 2026-05-06
Spend stopped. £4.70/day saved.

### ⏳ 3b. Build new Search campaign — NOT STARTED
Blueprint exists at `magna-park/GOOGLE-ADS-CAMPAIGN.md` (2 campaigns, 6 ad groups, full keyword + negative + RSA + sitelink list ready). Build approach not yet chosen — Ricky to pick:
- (a) UI walkthrough — slow but novice-safe
- (b) Google Ads Editor — desktop app, pre-built file import
- (c) Outsource to agency

### ⏳ 4. Claim £380 promo credit — NOT STARTED
Path: Billing → Promotions → claim.

## Side issue
Google Ads advertiser verification deadline: **2026-05-13** (per ACTION-PLAN.md). 7 days from now. If not completed, ALL ads pause regardless of campaign config.
