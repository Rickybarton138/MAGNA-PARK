"""
Magna Park Self Store — Content Engine & Automated Social Media Poster
======================================================================
5 content pillars, smart rotation, platform-specific content,
branded image generation, GBP post output, 5 posts/week scheduling.

Usage:
    python auto-poster.py --day mon              # Generate + publish Monday's post
    python auto-poster.py --day wed --dry-run    # Generate only, don't publish
    python auto-poster.py --schedule             # Print Task Scheduler setup commands
"""

import os
import sys
import json
import random
import hashlib
import argparse
import subprocess
import requests
from datetime import datetime, date
from pathlib import Path
from collections import Counter
from dotenv import load_dotenv

# Fix Windows console encoding for emojis
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

# Load credentials from this project's OWN .env — NOT the shared
# ~/social-media-agent/.env. That shared file was repointed to a different
# project, which silently published Magna Park posts to the wrong Facebook page.
load_dotenv(Path(__file__).parent / ".env")

# === CONFIG ===
# Page + Instagram IDs are HARDCODED on purpose — they identify the Magna Park
# accounts and must never be overridable by an env var another project controls.
PAGE_ID = "1012907521897286"          # Magna Park Self Store Ltd — Facebook Page
IG_ACCOUNT_ID = "17841480657315464"   # Magna Park — Instagram Business account
PAGE_TOKEN = os.getenv("META_PAGE_ACCESS_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

BASE_DIR = Path(__file__).parent
LOG_FILE = BASE_DIR / "post-log.json"
IMAGE_DIR = BASE_DIR / "social-images"
GBP_DIR = BASE_DIR / "gbp-posts"
IG_IMAGE_BASE = "https://raw.githubusercontent.com/Rickybarton138/MAGNA-PARK/main/social-images/"

# Ensure output directories exist
IMAGE_DIR.mkdir(exist_ok=True)
GBP_DIR.mkdir(exist_ok=True)

# === BUSINESS CONTEXT ===
BUSINESS_CONTEXT = """
Magna Park Self Store — foam insulated 20ft shipping container storage in Bournemouth.
- Price: £55/week, NO VAT, no hidden fees
- Location: 106 Provence Dr, Bournemouth, BH11 9FA
- Phone: 01202 113255
- Website: www.magnaparkselfstore.co.uk
- Features: 24/7 access with personal pin code, CCTV security, perimeter fencing, foam insulated (no condensation), flexible terms (no long contracts), drive-up access
- A single 20ft container fits contents of a 3-bed house (1,360 cubic feet)
- Cheaper than big chains (Big Yellow, Safestore charge £120-200/month + VAT)
- Perfect for: moving house, business overflow, vehicle/classic car storage, renovation clearout, seasonal storage, downsizing, uni storage
"""

# === 5 CONTENT PILLARS ===
PILLARS = {
    "PROMO": {
        "weight": 0.20,
        "color": (34, 139, 34),       # Green
        "description": "Direct storage promotion, pricing, offers",
        "topics": [
            "Price comparison — £55/week no VAT vs Big Yellow and Safestore charging £120-200/month PLUS VAT. That's potentially half the cost. Do the maths.",
            "No hidden fees — no admin charges, no padlock fees, no insurance upsell pressure. Just £55/week all-in. Transparent pricing.",
            "Flexible terms — no long contracts, no minimum stay. Need it for 2 weeks while you move? Fine. Need it for 2 years? Also fine.",
            "Size value — a 20ft container is 1,360 cubic feet. That fits the contents of a 3-bed house. One container, sorted.",
            "Drive-up access — no lifts, no corridors, no trolleys. Pull your van right up to your container door. Load and go.",
            "First week offer / referral — tell a friend, get a discount. Mention this post when you call. Limited time promotion.",
        ],
    },
    "TIPS": {
        "weight": 0.25,
        "color": (30, 144, 255),       # Blue
        "description": "Moving tips, packing advice, declutter guides, storage hacks",
        "topics": [
            "Packing tips — use wardrobe boxes for clothes, bubble wrap for fragile items, label everything on TWO sides. Pack heavy items in small boxes.",
            "Declutter guide — the 12-month rule. If you haven't used it in a year, donate or bin it. Less stuff = smaller move = less stress.",
            "Storage organisation hacks — put items you'll need first at the front. Create an aisle down the middle. Use shelving to maximise vertical space.",
            "Moving day checklist — book van, redirect post, notify utilities, defrost freezer 24hrs before, keep valuables with you.",
            "How to protect furniture in storage — use dust sheets, stand sofas on end, put pallets under items, leave space for airflow (our foam insulation helps too).",
            "How to estimate storage space — use the room-by-room method. 1-bed = 10x5, 2-bed = 10x10, 3-bed = 20ft container.",
            "Seasonal wardrobe swap — store off-season clothes in vacuum bags in your container. Saves wardrobe space at home, keeps everything clean and dry.",
        ],
    },
    "LOCAL": {
        "weight": 0.20,
        "color": (255, 140, 0),        # Orange
        "description": "Bournemouth community content, local events, support local",
        "topics": [
            "Support local Bournemouth — we're a local family business, not a faceless chain. Your money stays in the community.",
            "Bournemouth location convenience — just off the A341, easy access from Kinson, Bear Cross, Wallisdown, Canford Heath. 10 mins from town centre.",
            "Local business storage — Bournemouth small businesses use us for stock overflow, tools, market stall equipment. Cheaper than renting a unit on an industrial estate.",
            "Bournemouth events tie-in — mention a local event, festival, or community moment. Connect storage to the local lifestyle.",
            "Bournemouth property market — houses selling fast? Buyers need somewhere to store while chains complete. We bridge that gap.",
            "University storage — Bournemouth Uni and AUB students: store your stuff over summer instead of hauling it home. Collect in September.",
        ],
    },
    "STORIES": {
        "weight": 0.20,
        "color": (148, 103, 189),      # Purple
        "description": "Customer scenarios, before/after, relatable situations",
        "topics": [
            "The renovation story — family needed to clear the house for a full kitchen refit. Stored everything for 6 weeks, moved it all back. No damage, no stress.",
            "The downsizer — retired couple moving from a 4-bed to a 2-bed bungalow. Couldn't bear to part with everything at once. Stored the extras while they decided.",
            "The eBay seller — online business grew faster than the spare room could handle. Our container became their warehouse at a fraction of the cost.",
            "The between-houses panic — completion dates didn't line up. 2-week gap with nowhere to put a house full of furniture. We saved the day.",
            "The classic car enthusiast — needed secure, dry, insulated storage for a project car over winter. CCTV and foam insulation sealed the deal.",
            "The young professional — first flat too small for all their stuff. Weekend warrior who stores bikes, camping gear, and seasonal kit with us.",
        ],
    },
    "SEASONAL": {
        "weight": 0.15,
        "color": (220, 53, 69),        # Red
        "description": "Tied to current month/season/events",
        "topics": [
            "January — New Year, new space. Declutter after Christmas. Start the year with a clear home and a clear head.",
            "February — half-term clear-out. Kids' old toys, outgrown clothes, baby gear you're saving 'just in case'. Store it.",
            "March/April — spring clean. The classic declutter season. If your garage is full of stuff, move it to us and get your car back inside.",
            "May/June — moving season kicks off. House sales peak in spring. Get ahead and book your container before the rush.",
            "July/August — summer holiday. Store your stuff while you travel. Or clear the spare room before guests arrive.",
            "September — back to uni. Students returning to Bournemouth, collect your stored items. New students, we'll keep your stuff safe.",
            "October/November — autumn tidy. Garden furniture, BBQ, summer toys. Swap them for winter gear. Rotate your storage.",
            "December — Christmas overflow. Tree, decorations, gifts bought early. Need space at home? We've got space for you.",
        ],
    },
}

# === DAY-SPECIFIC PILLAR PREFERENCES ===
# Each day has boosted weights for certain pillars
DAY_PILLAR_BOOSTS = {
    "mon": {"TIPS": 1.5, "STORIES": 1.3},         # Monday motivation / helpful tips
    "tue": {"PROMO": 1.4, "LOCAL": 1.2},            # Tuesday promotions
    "wed": {"LOCAL": 1.5, "STORIES": 1.3},          # Midweek community
    "thu": {"TIPS": 1.3, "SEASONAL": 1.4},          # Thursday tips + seasonal
    "fri": {"LOCAL": 1.5, "STORIES": 1.3, "SEASONAL": 1.2},  # Friday fun / local
}

TONES = ["casual", "friendly", "direct", "conversational", "warm", "upbeat"]


# =====================================================================
# LOGGING
# =====================================================================

def load_log():
    """Load the post log from JSON file."""
    if LOG_FILE.exists():
        try:
            return json.loads(LOG_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return []
    return []


def save_log(log):
    """Save the post log to JSON file."""
    LOG_FILE.write_text(json.dumps(log, indent=2, ensure_ascii=False), encoding="utf-8")


# =====================================================================
# SMART TOPIC ROTATION
# =====================================================================

def pick_pillar_and_topic(log, day="mon"):
    """
    Select a pillar and topic using weighted rotation.
    - Never repeat the same pillar back-to-back
    - Underused pillars get boosted
    - Day-specific boosts applied
    """
    # Get the last pillar used (to avoid back-to-back)
    last_pillar = None
    if log:
        last_pillar = log[-1].get("pillar")

    # Count pillar usage in recent history (last 20 posts)
    recent = log[-20:]
    pillar_counts = Counter(entry.get("pillar") for entry in recent)

    # Calculate weights with catch-up mechanism
    pillar_names = list(PILLARS.keys())
    weights = {}
    total_recent = max(len(recent), 1)

    for name in pillar_names:
        base_weight = PILLARS[name]["weight"]
        actual_usage = pillar_counts.get(name, 0) / total_recent
        # If underused, boost; if overused, reduce
        usage_ratio = max(0.3, base_weight / max(actual_usage, 0.01))
        usage_ratio = min(usage_ratio, 3.0)  # Cap the boost

        weight = base_weight * usage_ratio

        # Apply day-specific boost
        day_boosts = DAY_PILLAR_BOOSTS.get(day, {})
        if name in day_boosts:
            weight *= day_boosts[name]

        # Zero out last pillar to prevent back-to-back
        if name == last_pillar and len(pillar_names) > 1:
            weight = 0.0

        weights[name] = weight

    # Normalize weights
    total_weight = sum(weights.values())
    if total_weight == 0:
        # Fallback: equal weights excluding last pillar
        for name in pillar_names:
            weights[name] = 1.0 if name != last_pillar else 0.0
        total_weight = sum(weights.values())

    # Weighted random selection
    r = random.uniform(0, total_weight)
    cumulative = 0
    chosen_pillar = pillar_names[0]
    for name in pillar_names:
        cumulative += weights[name]
        if r <= cumulative:
            chosen_pillar = name
            break

    # Pick a topic within the pillar, avoiding recently used ones
    topics = PILLARS[chosen_pillar]["topics"]
    recent_topics = [
        entry.get("topic_index")
        for entry in log[-10:]
        if entry.get("pillar") == chosen_pillar
    ]
    available = [i for i in range(len(topics)) if i not in recent_topics]
    if not available:
        available = list(range(len(topics)))

    # For SEASONAL, pick the most relevant topic based on current month
    if chosen_pillar == "SEASONAL":
        month = datetime.now().month
        # Map months to topic indices (topics are ordered Jan-Dec roughly)
        month_map = {
            1: 0, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3,
            7: 4, 8: 4, 9: 5, 10: 6, 11: 6, 12: 7,
        }
        preferred = month_map.get(month, 0)
        if preferred in available:
            topic_index = preferred
        else:
            topic_index = random.choice(available)
    else:
        topic_index = random.choice(available)

    return chosen_pillar, topic_index, topics[topic_index]


# =====================================================================
# AI CONTENT GENERATION
# =====================================================================

def generate_content(pillar, topic_text, tone):
    """
    Generate platform-specific content for Facebook, Instagram, and GBP.
    Returns dict with keys: facebook, instagram, gbp.
    """
    current_month = datetime.now().strftime("%B %Y")
    current_season = _get_season()

    prompt = f"""You are a social media content writer for Magna Park Self Store, a local self-storage business in Bournemouth.

CONTENT PILLAR: {pillar} — {PILLARS[pillar]['description']}
TOPIC: {topic_text}
TONE: {tone}
CURRENT DATE: {current_month} ({current_season})

BUSINESS DETAILS:
{BUSINESS_CONTEXT}

Generate THREE versions of this post. Return them as a JSON object with these exact keys:

"facebook": A Facebook post. Conversational, friendly, 150-300 words. Can include a link to the website. Use 2-3 emojis naturally. Include a clear call to action (phone or website). Add 5-8 hashtags at the end. Never use the phrases 'game changer', 'look no further', or 'hidden gem'.

"instagram": An Instagram caption. Shorter than Facebook (80-150 words). More emoji-friendly (4-6 emojis). 15-20 relevant hashtags at the end (mix of broad and niche). No links in caption (mention 'link in bio' if needed). Punchy opening line to grab attention. Never use the phrases 'game changer', 'look no further', or 'hidden gem'.

"gbp": A Google Business Profile post. Maximum 300 characters including spaces. Must include a CTA like 'Call us', 'Book today', or 'Visit our website'. Very concise and direct. No hashtags. Include the phone number 01202 113255.

Return ONLY the JSON object, no markdown code fences, no extra text."""

    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {OPENAI_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": "gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a social media copywriter. Always respond with valid JSON only."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.85,
            "max_tokens": 1200,
        },
    )
    response.raise_for_status()
    raw = response.json()["choices"][0]["message"]["content"].strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("\n", 1)[1] if "\n" in raw else raw[3:]
    if raw.endswith("```"):
        raw = raw[:-3]
    if raw.startswith("json"):
        raw = raw[4:]
    raw = raw.strip()

    return json.loads(raw)


def _get_season():
    """Return the current season for the UK."""
    month = datetime.now().month
    if month in (3, 4, 5):
        return "Spring"
    elif month in (6, 7, 8):
        return "Summer"
    elif month in (9, 10, 11):
        return "Autumn"
    else:
        return "Winter"


# =====================================================================
# BRANDED IMAGE GENERATION
# =====================================================================

def generate_branded_image(pillar, topic_text):
    """
    Generate a branded image using Pillow with pillar-specific colors.
    Returns the filename of the generated image.
    """
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("WARNING: Pillow not installed. Run: pip install Pillow")
        print("Falling back to default image.")
        return "post-template.png"

    width, height = 1080, 1080
    bg_color = PILLARS[pillar]["color"]

    # Create gradient-style background
    img = Image.new("RGB", (width, height), bg_color)
    draw = ImageDraw.Draw(img)

    # Draw a darker overlay rectangle for text area
    overlay_color = tuple(max(0, c - 40) for c in bg_color)
    draw.rectangle([60, 250, 1020, 830], fill=overlay_color, outline=None)

    # Draw accent lines
    accent_color = tuple(min(255, c + 80) for c in bg_color)
    draw.rectangle([60, 250, 1020, 260], fill=accent_color)
    draw.rectangle([60, 820, 1020, 830], fill=accent_color)

    # Load fonts (try system fonts, fall back to default)
    def _load_font(size, bold=False):
        font_names = [
            "arialbd.ttf" if bold else "arial.ttf",
            "Arial Bold.ttf" if bold else "Arial.ttf",
            "calibrib.ttf" if bold else "calibri.ttf",
        ]
        for font_name in font_names:
            try:
                return ImageFont.truetype(font_name, size)
            except OSError:
                continue
        # Try Windows font path
        for font_name in font_names:
            try:
                return ImageFont.truetype(f"C:/Windows/Fonts/{font_name}", size)
            except OSError:
                continue
        return ImageFont.load_default()

    font_title = _load_font(52, bold=True)
    font_body = _load_font(36)
    font_tagline = _load_font(28)
    font_pillar = _load_font(24, bold=True)

    # Draw pillar badge
    pillar_label = pillar.upper()
    draw.rounded_rectangle([60, 180, 60 + len(pillar_label) * 18 + 40, 240], radius=10, fill=accent_color)
    draw.text((80, 192), pillar_label, fill="white", font=font_pillar)

    # Business name
    draw.text((540, 290), "MAGNA PARK", fill="white", font=font_title, anchor="mt")
    draw.text((540, 355), "SELF STORE", fill=accent_color, font=font_title, anchor="mt")

    # Topic text (wrapped)
    short_topic = topic_text.split("—")[0].strip() if "—" in topic_text else topic_text[:50]
    _draw_wrapped_text(draw, short_topic, font_body, "white", 540, 440, 880)

    # Price callout
    draw.text((540, 620), "From just £55/week", fill=accent_color, font=font_body, anchor="mt")
    draw.text((540, 670), "NO VAT  |  No Hidden Fees", fill="white", font=font_tagline, anchor="mt")

    # Bottom info
    draw.text((540, 740), "24/7 Access  |  CCTV  |  Foam Insulated", fill="white", font=font_tagline, anchor="mt")
    draw.text((540, 780), "01202 113255  |  magnaparkselfstore.co.uk", fill=accent_color, font=font_tagline, anchor="mt")

    # Bottom bar with address
    draw.rectangle([0, 980, 1080, 1080], fill=overlay_color)
    draw.text((540, 1020), "106 Provence Dr, Bournemouth, BH11 9FA", fill="white", font=font_tagline, anchor="mt")

    # Generate unique filename
    date_str = datetime.now().strftime("%Y%m%d")
    slug = pillar.lower()
    filename = f"{date_str}-{slug}.png"
    filepath = IMAGE_DIR / filename
    img.save(filepath, "PNG", quality=95)
    print(f"Image generated: {filepath}")

    return filename


def _draw_wrapped_text(draw, text, font, fill, x, y, max_width):
    """Draw text centered and wrapped within max_width."""
    words = text.split()
    lines = []
    current_line = ""
    for word in words:
        test_line = f"{current_line} {word}".strip()
        bbox = draw.textbbox((0, 0), test_line, font=font)
        if bbox[2] - bbox[0] <= max_width:
            current_line = test_line
        else:
            if current_line:
                lines.append(current_line)
            current_line = word
    if current_line:
        lines.append(current_line)

    line_height = 50
    total_height = len(lines) * line_height
    start_y = y
    for i, line in enumerate(lines):
        draw.text((x, start_y + i * line_height), line, fill=fill, font=font, anchor="mt")


# =====================================================================
# GIT: PUSH IMAGE TO GITHUB
# =====================================================================

def push_image_to_github(filename):
    """Add, commit, and push the new image so Instagram can access it via raw URL."""
    try:
        repo_dir = str(BASE_DIR)
        filepath = str(IMAGE_DIR / filename)
        subprocess.run(["git", "add", filepath], cwd=repo_dir, check=True, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", f"Add social image: {filename}"],
            cwd=repo_dir, check=True, capture_output=True,
        )
        result = subprocess.run(
            ["git", "push"], cwd=repo_dir, check=True, capture_output=True, text=True,
        )
        print(f"Image pushed to GitHub: {filename}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"WARNING: Git push failed: {e.stderr if hasattr(e, 'stderr') else e}")
        return False
    except FileNotFoundError:
        print("WARNING: git not found in PATH. Image not pushed.")
        return False


# =====================================================================
# PUBLISHING
# =====================================================================

def publish_to_facebook(content):
    """Publish a post to the Facebook Page."""
    response = requests.post(
        f"https://graph.facebook.com/v21.0/{PAGE_ID}/feed",
        data={"message": content, "access_token": PAGE_TOKEN},
    )
    response.raise_for_status()
    return response.json().get("id")


def publish_to_instagram(content, image_url):
    """Publish a photo post to Instagram via Facebook Graph API."""
    # Step 1: Create media container
    container_resp = requests.post(
        f"https://graph.facebook.com/v21.0/{IG_ACCOUNT_ID}/media",
        data={
            "image_url": image_url,
            "caption": content,
            "access_token": PAGE_TOKEN,
        },
    )
    container_resp.raise_for_status()
    container_id = container_resp.json()["id"]

    # Step 2: Publish the container
    publish_resp = requests.post(
        f"https://graph.facebook.com/v21.0/{IG_ACCOUNT_ID}/media_publish",
        data={
            "creation_id": container_id,
            "access_token": PAGE_TOKEN,
        },
    )
    publish_resp.raise_for_status()
    return publish_resp.json().get("id")


def save_gbp_post(pillar, gbp_content):
    """Save GBP post to file for later manual posting or API integration."""
    date_str = datetime.now().strftime("%Y%m%d")
    filename = f"{date_str}-{pillar.lower()}-gbp.txt"
    filepath = GBP_DIR / filename
    filepath.write_text(gbp_content, encoding="utf-8")
    print(f"GBP post saved: {filepath}")
    return filename


# =====================================================================
# SCHEDULING
# =====================================================================

def print_schedule_commands():
    """Print Windows Task Scheduler commands for 5 posts/week."""
    script_path = str(BASE_DIR / "auto-poster.py")
    python_path = sys.executable

    print("\n" + "=" * 70)
    print("WINDOWS TASK SCHEDULER SETUP — 5 Posts/Week")
    print("=" * 70)
    print("\nRun these commands in an ELEVATED (Admin) PowerShell:\n")

    schedule = [
        ("mon", "Monday",    "19:30"),
        ("tue", "Tuesday",   "12:00"),
        ("wed", "Wednesday", "18:00"),
        ("thu", "Thursday",  "12:00"),
        ("fri", "Friday",    "17:00"),
    ]

    for day, day_name, time in schedule:
        task_name = f"MagnaPark_AutoPost_{day_name}"
        cmd = (
            f'schtasks /create /tn "{task_name}" /tr '
            f'"\"{python_path}\" \"{script_path}\" --day {day}" '
            f'/sc weekly /d {day[:3].upper()} /st {time} /f'
        )
        print(f"# {day_name} at {time}")
        print(cmd)
        print()

    print("To delete all tasks:")
    for day, day_name, _ in schedule:
        print(f'schtasks /delete /tn "MagnaPark_AutoPost_{day_name}" /f')
    print()
    print("To view all tasks:")
    print('schtasks /query /tn "MagnaPark_AutoPost_*" /fo TABLE')
    print("=" * 70)


# =====================================================================
# MAIN
# =====================================================================

def main():
    parser = argparse.ArgumentParser(description="Magna Park Self Store — Content Engine")
    parser.add_argument("--day", choices=["mon", "tue", "wed", "thu", "fri"],
                        default=_get_today_short(),
                        help="Day of week for content selection (default: today)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Generate content but don't publish")
    parser.add_argument("--schedule", action="store_true",
                        help="Print Task Scheduler setup commands and exit")
    args = parser.parse_args()

    if args.schedule:
        print_schedule_commands()
        return

    # Validate credentials
    if not args.dry_run:
        if not PAGE_TOKEN:
            print("ERROR: META_PAGE_ACCESS_TOKEN not set in ~/magna-park/.env")
            return
    if not OPENAI_API_KEY:
        print("ERROR: OPENAI_API_KEY not set in ~/magna-park/.env")
        return

    log = load_log()
    pillar, topic_index, topic_text = pick_pillar_and_topic(log, day=args.day)
    tone = random.choice(TONES)

    print(f"\n{'=' * 60}")
    print(f"MAGNA PARK CONTENT ENGINE — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'=' * 60}")
    print(f"Day:    {args.day.upper()}")
    print(f"Pillar: {pillar} ({PILLARS[pillar]['description']})")
    print(f"Topic:  {topic_text[:80]}...")
    print(f"Tone:   {tone}")
    print(f"Mode:   {'DRY RUN' if args.dry_run else 'LIVE PUBLISH'}")
    print(f"{'=' * 60}\n")

    # --- Generate AI content ---
    print("[1/5] Generating AI content for all platforms...")
    try:
        content = generate_content(pillar, topic_text, tone)
    except Exception as e:
        print(f"FATAL: Content generation failed: {e}")
        return

    fb_content = content.get("facebook", "")
    ig_content = content.get("instagram", "")
    gbp_content = content.get("gbp", "")

    print(f"\n--- FACEBOOK ---\n{fb_content}\n")
    print(f"--- INSTAGRAM ---\n{ig_content}\n")
    print(f"--- GBP ({len(gbp_content)} chars) ---\n{gbp_content}\n")

    # --- Generate branded image ---
    print("[2/5] Generating branded image...")
    image_filename = generate_branded_image(pillar, topic_text)
    image_url = f"{IG_IMAGE_BASE}{image_filename}"

    # --- Push image to GitHub ---
    git_pushed = False
    if not args.dry_run:
        print("[3/5] Pushing image to GitHub...")
        git_pushed = push_image_to_github(image_filename)
        if not git_pushed:
            # Fall back to existing template image
            image_url = f"{IG_IMAGE_BASE}post-template.png"
            print(f"Falling back to: {image_url}")
    else:
        print("[3/5] Skipping GitHub push (dry run)")

    # --- Publish ---
    fb_post_id = None
    ig_post_id = None
    fb_success = False
    ig_success = False

    if not args.dry_run:
        # Facebook
        print("[4/5] Publishing to Facebook...")
        try:
            fb_post_id = publish_to_facebook(fb_content)
            fb_success = True
            print(f"Facebook SUCCESS — Post ID: {fb_post_id}")
        except Exception as e:
            print(f"Facebook FAILED: {e}")

        # Instagram
        print("[5/5] Publishing to Instagram...")
        try:
            ig_post_id = publish_to_instagram(ig_content, image_url)
            ig_success = True
            print(f"Instagram SUCCESS — Post ID: {ig_post_id}")
        except Exception as e:
            print(f"Instagram FAILED: {e}")
    else:
        print("[4/5] Skipping Facebook publish (dry run)")
        print("[5/5] Skipping Instagram publish (dry run)")

    # --- Save GBP post ---
    gbp_filename = save_gbp_post(pillar, gbp_content)

    # --- Log everything ---
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "day": args.day,
        "pillar": pillar,
        "topic_index": topic_index,
        "topic": topic_text[:80],
        "tone": tone,
        "image": image_filename,
        "image_pushed": git_pushed,
        "fb_post_id": fb_post_id,
        "fb_success": fb_success if not args.dry_run else None,
        "ig_post_id": ig_post_id,
        "ig_success": ig_success if not args.dry_run else None,
        "gbp_file": gbp_filename,
        "dry_run": args.dry_run,
        "content": {
            "facebook": fb_content,
            "instagram": ig_content,
            "gbp": gbp_content,
        },
    }
    log.append(log_entry)
    save_log(log)

    # --- Summary ---
    print(f"\n{'=' * 60}")
    print("SUMMARY")
    print(f"{'=' * 60}")
    print(f"Pillar:    {pillar}")
    print(f"Image:     {image_filename}")
    if not args.dry_run:
        print(f"Facebook:  {'OK' if fb_success else 'FAILED'} ({fb_post_id or 'N/A'})")
        print(f"Instagram: {'OK' if ig_success else 'FAILED'} ({ig_post_id or 'N/A'})")
    else:
        print(f"Facebook:  DRY RUN (not published)")
        print(f"Instagram: DRY RUN (not published)")
    print(f"GBP:       Saved to gbp-posts/{gbp_filename}")
    print(f"Log:       Updated post-log.json ({len(log)} total entries)")
    print(f"{'=' * 60}\n")


def _get_today_short():
    """Return today's day as a 3-letter lowercase string."""
    days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
    return days[datetime.now().weekday()]


if __name__ == "__main__":
    main()
