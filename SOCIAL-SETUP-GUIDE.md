# Magna Park Self Storage — Social Media Setup Guide

## Platform 1: Facebook (Already Have Page)

You already have a Facebook Page. You just need to get API credentials so Claude can post automatically.

### Step 1: Get Your Page ID
1. Go to your Magna Park Facebook Page
2. Click **About** (left sidebar)
3. Scroll to the bottom — your **Page ID** is a number like `123456789012345`
4. Copy it

### Step 2: Get a Page Access Token
1. Go to **https://developers.facebook.com**
2. Log in with the Facebook account that is admin of the Magna Park page
3. Click **My Apps** (top right) → **Create App**
4. Choose **Business** type → click Next
5. App name: `Magna Park Social` → Create
6. Once created, go to **App Dashboard** → left sidebar → **Add Product** → find **Facebook Login** → click **Set Up**
7. Now go to **https://developers.facebook.com/tools/explorer/**
8. Select your app from the dropdown (top right)
9. Click **Get User Access Token**
10. Check these permissions:
    - `pages_show_list`
    - `pages_read_engagement`
    - `pages_manage_posts`
    - `pages_manage_metadata`
    - `publish_to_groups` (if posting to groups too)
11. Click **Generate Access Token** → authorize in the popup
12. Now in the API Explorer, change the dropdown from "User Token" to your **Page** (Magna Park Self Storage)
13. Click **Generate Access Token** again — this gives you the **Page Access Token**
14. Copy this token

### Step 3: Make the Token Long-Lived (Important!)
Short-lived tokens expire in 1 hour. You need a long-lived one.

1. Go to **https://developers.facebook.com/tools/debug/accesstoken/**
2. Paste your token → click **Debug**
3. Click **Extend Access Token** at the bottom
4. Copy the new long-lived token (lasts 60 days)
5. For a permanent (never-expiring) page token, use the Graph API:
   ```
   GET /me/accounts?access_token=YOUR_LONG_LIVED_USER_TOKEN
   ```
   The `access_token` field in the response for your page is permanent.

### Step 4: Give Me These Values
- **META_PAGE_ID:** `your page ID number`
- **META_PAGE_ACCESS_TOKEN:** `your long-lived page access token`

---

## Platform 2: X (Twitter)

### Step 1: Create X Account for Magna Park
1. Go to **https://x.com/i/flow/signup**
2. Use email: `magnaparkselfstore@outlook.com` (or create a dedicated one)
3. Choose handle: `@MagnaParkStore` or `@MagnaParkBH` (check availability)
4. Complete signup, verify email
5. Fill in profile:
   - **Name:** Magna Park Self Storage
   - **Bio:** Foam insulated 20ft container storage in Bournemouth. £55/week, no VAT, 24/7 access. 📍 BH11 9FA | 📞 01202 113255
   - **Location:** Bournemouth, Dorset
   - **Website:** https://magnaparkselfstore.co.uk
   - **Profile pic:** Use the Magna Park logo (MAGNA PARK LOGO.PNG in your project folder)
   - **Header:** Use the facebook cover SVG or create a banner showing the containers

### Step 2: Apply for X Developer Account
1. Go to **https://developer.x.com/en/portal/petition/essential/basic-info**
2. Sign in with the Magna Park X account
3. You'll need to:
   - Verify your phone number (add one if not already)
   - Describe your use case: "Automated posting of business updates and storage promotions for our self-storage business in Bournemouth"
4. Accept the developer agreement
5. This usually gets **instant approval** for Free tier (enough for posting)

### Step 3: Create an App & Get API Keys
1. Once approved, go to **https://developer.x.com/en/portal/dashboard**
2. Click **+ Create Project**
   - Project name: `Magna Park Social`
   - Use case: `Making a bot` or `Managing social media`
3. Click **+ Create App** within the project
   - App name: `MagnaParkAutoPost`
4. You'll see your keys. Save ALL of these:
   - **API Key** (also called Consumer Key)
   - **API Key Secret** (also called Consumer Secret)
5. Now click **App Settings** → **Keys and tokens** tab
6. Under **Authentication Tokens**, click **Generate** for:
   - **Access Token**
   - **Access Token Secret**
7. **IMPORTANT:** Set App permissions to **Read and Write**
   - Go to App Settings → User authentication settings → Edit
   - Set **App permissions** to **Read and write**
   - Set **Type of App** to **Web App, Automated App or Bot**
   - Callback URL: `https://magnaparkselfstore.co.uk` (doesn't matter for bot use)
   - Website URL: `https://magnaparkselfstore.co.uk`
   - Save

### Step 4: Give Me These Values
- **X_API_KEY:** `your API key`
- **X_API_SECRET:** `your API key secret`
- **X_ACCESS_TOKEN:** `your access token`
- **X_ACCESS_TOKEN_SECRET:** `your access token secret`

---

## Platform 3: TikTok

### Step 1: Create TikTok Business Account
1. Download TikTok app on your phone (or go to **https://www.tiktok.com/signup**)
2. Sign up with email: `magnaparkselfstore@outlook.com`
3. Choose username: `@magnaparkselfstore` or `@magnaparkbournemouth`
4. Once account is created, go to **Settings & Privacy** → **Account** → **Switch to Business Account**
5. Select category: **Real Estate** or **Local Service**
6. Fill in profile:
   - **Name:** Magna Park Self Storage
   - **Bio:** Foam insulated container storage in Bournemouth 📦 £55/week | No VAT | 24/7 access | Link below 👇
   - **Website:** https://magnaparkselfstore.co.uk
   - **Profile pic:** Magna Park logo
   - **Email:** magnaparkselfstore@outlook.com

### Step 2: Apply for TikTok Business API (For Automated Posting)
**Note: This takes 1-2 weeks for approval. You can post manually via the app immediately, and we'll automate once approved.**

1. Go to **https://developers.tiktok.com/**
2. Click **Sign Up** → use your TikTok business account credentials
3. Once logged into the developer portal:
   - Click **Manage apps** → **Create app**
   - App name: `Magna Park Social`
   - Description: "Automated social media posting for Magna Park Self Storage, a container storage business in Bournemouth, UK"
   - App icon: Upload Magna Park logo
4. Under **Products**, add:
   - **Content Posting API** — this is what allows automated posting
   - **Video Upload** (if available)
5. Fill in the required business verification:
   - Business name: Magna Park Self Storage (or your registered company name)
   - Business website: https://magnaparkselfstore.co.uk
   - Business type: Local Service
6. Submit for review
7. You'll receive an email when approved (typically 5-10 business days)

### Step 3: Get API Credentials (After Approval)
1. Once approved, go to your app in the developer portal
2. You'll see:
   - **Client Key** (App ID)
   - **Client Secret**
3. You'll also need to set up OAuth 2.0:
   - Redirect URI: `https://magnaparkselfstore.co.uk/tiktok-callback`
   - Scopes: `video.publish`, `video.upload`
4. Generate an access token through the OAuth flow

### Step 4: Start Posting Manually NOW (While Waiting for API)
Don't wait for API approval. Start posting immediately:

1. Use the TikTok app on your phone
2. Film the videos described in `social-content/week1-tiktok.md`
3. Post 3x per week (Mon/Wed/Fri)
4. Use these hashtags on every post: #bournemouth #storage #selfstorage #containerstorage #dorset
5. Once API is approved, we'll automate everything

### Step 4 (After API Approval): Give Me These Values
- **TIKTOK_CLIENT_KEY:** `your client key`
- **TIKTOK_CLIENT_SECRET:** `your client secret`
- **TIKTOK_ACCESS_TOKEN:** `your OAuth access token`

---

## Quick Summary — What You Need to Do

| Step | Platform | Time | Difficulty |
|------|----------|------|-----------|
| 1 | **Facebook** — Get Page ID + Access Token from Meta Developer Tools | 15 mins | Medium |
| 2 | **X** — Create account, apply for developer access, get 4 API keys | 20 mins | Easy (instant approval) |
| 3 | **TikTok** — Create business account, apply for API (takes 1-2 weeks) | 10 mins + wait | Easy |
| 4 | **TikTok** — Start posting manually from phone while waiting for API | Ongoing | Easy |

**Total active time: ~45 minutes**

Once you have the credentials, give them to me and I'll configure the MCP server to autopost on schedule. Content for the first month is already generated and saved in `social-content/`.

---

## Posting Schedule

| Day | Facebook | X | TikTok |
|-----|----------|---|--------|
| Monday | 7:30pm — Feature post | 8am — Quick tip | Video post |
| Wednesday | — | 12pm — Value post | Video post |
| Thursday | 12pm — Edu/value post | — | — |
| Friday | — | 5pm — Weekend hook | Video post |

**Total: 8 posts/week across 3 platforms**
