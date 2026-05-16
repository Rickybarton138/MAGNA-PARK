"""
get-fb-token.py  —  Refresh the Magna Park Facebook Page access token.

WHAT IT DOES
  1. Exchanges a short-lived User token for a long-lived one.
  2. Pulls the PERMANENT Page access token for the Magna Park page.
  3. Writes it into ~/magna-park/.env  (META_PAGE_ACCESS_TOKEN=...).
  4. Verifies the token works.
  5. Offers to delete the 8 misplaced Magna Park posts from the Dugout AI page
     (only if that page is on the same account).

BEFORE YOU RUN — get two things ready:

  A) App Secret for the "Magna Park Social" app
       developers.facebook.com  ->  your apps  ->  Magna Park Social
       ->  App settings  ->  Basic  ->  App secret  ->  Show

  B) A short-lived User token
       developers.facebook.com/tools/explorer
       ->  pick the "Magna Park Social" app (top-right dropdown)
       ->  Permissions: add these five —
              pages_show_list
              pages_read_engagement
              pages_manage_posts
              instagram_basic
              instagram_content_publish
       ->  click "Generate Access Token", approve, copy the token

THEN, in a terminal:   python get-fb-token.py
(Run it in a real terminal so the prompts work — not via the `!` shortcut.)
"""

import sys
import getpass
from pathlib import Path

import requests

APP_ID = "1487523209572253"          # "Magna Park Social" Meta app
PAGE_ID = "1012907521897286"         # Magna Park Self Store Ltd — Facebook Page
DUGOUT_PAGE_ID = "1046428451892361"  # Dugout AI / football-analyzer page
GRAPH = "https://graph.facebook.com/v21.0"
ENV_PATH = Path(__file__).parent / ".env"

# The 8 Magna Park posts that were published to the Dugout AI page by mistake.
MISPLACED_POSTS = [
    "1046428451892361_122102947910848655",
    "1046428451892361_122103447296848655",
    "1046428451892361_122104318088848655",
    "1046428451892361_122104318514848655",
    "1046428451892361_122105857046848655",
    "1046428451892361_122106398630848655",
    "1046428451892361_122107532792848655",
    "1046428451892361_122108380826848655",
]


def die(msg):
    print(f"\n  FAILED: {msg}")
    sys.exit(1)


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    print("=== Magna Park Facebook token refresh ===\n")
    app_secret = getpass.getpass("Paste the App Secret (input hidden): ").strip()
    short_token = input("Paste the short-lived User token: ").strip()
    if not app_secret or not short_token:
        die("Both values are required.")

    # 1. short-lived user token -> long-lived user token
    print("\n[1/4] Exchanging for a long-lived user token...")
    j = requests.get(f"{GRAPH}/oauth/access_token", params={
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": app_secret,
        "fb_exchange_token": short_token,
    }).json()
    if "error" in j:
        die(j["error"].get("message"))
    long_token = j["access_token"]
    print("  OK")

    # 2. find the Magna Park page + its (permanent) page token
    print("[2/4] Fetching page tokens...")
    j = requests.get(f"{GRAPH}/me/accounts",
                     params={"access_token": long_token, "limit": 100}).json()
    if "error" in j:
        die(j["error"].get("message"))
    pages = j.get("data", [])
    print(f"  Pages on this account: {', '.join(p['name'] for p in pages) or '(none)'}")
    page = next((p for p in pages if p["id"] == PAGE_ID), None)
    if not page:
        die(f"Magna Park page ({PAGE_ID}) not found on this account. "
            "Check the token came from an account that admins the page, "
            "and that pages_show_list was granted.")
    page_token = page["access_token"]
    print(f"  OK — got a permanent token for: {page['name']}")

    # 3. verify the page token works
    print("[3/4] Verifying the page token...")
    j = requests.get(f"{GRAPH}/{PAGE_ID}",
                     params={"fields": "name,fan_count", "access_token": page_token}).json()
    if "error" in j:
        die(j["error"].get("message"))
    print(f"  OK — {j.get('name')} ({j.get('fan_count', '?')} followers)")

    # 4. write into .env, preserving every other line
    print("[4/4] Writing token into .env...")
    lines = ENV_PATH.read_text(encoding="utf-8").splitlines() if ENV_PATH.exists() else []
    out, done = [], False
    for ln in lines:
        if ln.startswith("META_PAGE_ACCESS_TOKEN="):
            out.append(f"META_PAGE_ACCESS_TOKEN={page_token}")
            done = True
        else:
            out.append(ln)
    if not done:
        out.append(f"META_PAGE_ACCESS_TOKEN={page_token}")
    ENV_PATH.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"  OK — saved to {ENV_PATH}")

    # 5. optional: clean up the Dugout AI page
    dugout = next((p for p in pages if p["id"] == DUGOUT_PAGE_ID), None)
    if dugout:
        print(f"\nThe Dugout AI page ('{dugout['name']}') is also on this account.")
        ans = input("Delete the 8 misplaced Magna Park posts from it now? [y/N]: ").strip().lower()
        if ans == "y":
            dt = dugout["access_token"]
            removed = 0
            for pid in MISPLACED_POSTS:
                jg = requests.get(f"{GRAPH}/{pid}",
                                  params={"fields": "message", "access_token": dt}).json()
                if "error" in jg:
                    print(f"  skip   {pid} — {jg['error'].get('message')}")
                    continue
                if "magna park" not in (jg.get("message") or "").lower():
                    print(f"  skip   {pid} — not a Magna Park post, left alone")
                    continue
                jd = requests.delete(f"{GRAPH}/{pid}", params={"access_token": dt}).json()
                if jd.get("success") is True:
                    print(f"  deleted {pid}")
                    removed += 1
                else:
                    print(f"  fail   {pid} — {jd}")
            print(f"  Removed {removed} post(s) from the Dugout AI page.")
        else:
            print("  Skipped — you can delete those 8 posts manually any time.")
    else:
        print("\n(Dugout AI page isn't on this account — delete those 8 posts manually.)")

    print("\nDone. Test posting with:  python auto-poster.py --day mon --dry-run")


if __name__ == "__main__":
    main()
