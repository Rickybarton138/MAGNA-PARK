"""
Generate Meta ad creatives for the Magna Park launch campaign.

Outputs four PNGs into social-images/meta-ads/:
  ad1-price-offer.png        1080x1080   FB/IG feed
  ad2-problem-solution.png   1080x1080   FB/IG feed
  ad3-trust-local.png        1080x1080   FB/IG feed
  ad4-story.png              1080x1920   Stories / Reels

These are designed to stand alone OR be used as the text overlay on a real
site photo (drop a photo behind, blur, layer this on top in any editor).
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = Path(__file__).parent / "social-images" / "meta-ads"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# --- Brand ---
GREEN = (45, 90, 61)        # #2d5a3d
GREEN_DARK = (30, 60, 41)
PAPER = (248, 246, 243)     # #f8f6f3
INK = (26, 26, 26)          # #1a1a1a
ACCENT = (255, 107, 53)     # #ff6b35 (offer / FREE)
WHITE = (255, 255, 255)
MUTED = (210, 215, 210)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = (
        ["arialbd.ttf", "Arial Bold.ttf", "calibrib.ttf"]
        if bold
        else ["arial.ttf", "Arial.ttf", "calibri.ttf"]
    )
    for n in names:
        for path in (n, f"C:/Windows/Fonts/{n}"):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def _wrap(draw, text, font, max_width):
    lines, current = [], ""
    for word in text.split():
        test = (current + " " + word).strip()
        if draw.textbbox((0, 0), test, font=font)[2] <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _draw_centered_lines(draw, lines, font, y, width, fill, line_gap=12):
    h_total = 0
    sizes = []
    for ln in lines:
        bbox = draw.textbbox((0, 0), ln, font=font)
        sizes.append((bbox[2] - bbox[0], bbox[3] - bbox[1]))
        h_total += bbox[3] - bbox[1] + line_gap
    y_cursor = y
    for ln, (w, h) in zip(lines, sizes):
        draw.text(((width - w) // 2, y_cursor), ln, font=font, fill=fill)
        y_cursor += h + line_gap


def _brand_footer(draw, w: int, y_top: int):
    draw.rectangle([0, y_top, w, y_top + 100], fill=GREEN_DARK)
    sub = _font(28, bold=True)
    info = _font(24)
    draw.text((w // 2, y_top + 22), "MAGNA PARK SELF STORE", font=sub, fill=WHITE, anchor="mt")
    draw.text(
        (w // 2, y_top + 58),
        "magnaparkselfstore.co.uk  |  01202 113255",
        font=info,
        fill=MUTED,
        anchor="mt",
    )


def _badge(draw, x, y, text, font, fg, bg, pad_x=22, pad_y=10, radius=12):
    tw = draw.textbbox((0, 0), text, font=font)[2]
    th = draw.textbbox((0, 0), text, font=font)[3]
    draw.rounded_rectangle(
        [x, y, x + tw + 2 * pad_x, y + th + 2 * pad_y],
        radius=radius,
        fill=bg,
    )
    draw.text((x + pad_x, y + pad_y), text, font=font, fill=fg)


# ============================================================
# Ad 1 — Price / offer angle (1080x1080)
# ============================================================
def ad1():
    w, h = 1080, 1080
    img = Image.new("RGB", (w, h), GREEN)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 16], fill=ACCENT)

    # eyebrow badge
    _badge(d, 80, 80, "LAUNCH OFFER", _font(28, bold=True), GREEN, ACCENT)

    # big headline
    f_huge = _font(130, bold=True)
    f_big = _font(96, bold=True)
    f_body = _font(38)
    f_lead = _font(48, bold=True)

    d.text((w // 2, 220), "4 WEEKS", font=f_huge, fill=WHITE, anchor="mt")
    d.text((w // 2, 360), "FREE", font=f_huge, fill=ACCENT, anchor="mt")
    d.text((w // 2, 510), "STORAGE BOURNEMOUTH", font=f_lead, fill=WHITE, anchor="mt")

    # body
    body_lines = _wrap(
        d,
        "Secure 20ft insulated containers · 24/7 drive-up access · CCTV. "
        "Then £55/week, no long contracts.",
        f_body,
        w - 180,
    )
    _draw_centered_lines(d, body_lines, f_body, 610, w, MUTED)

    # save callout
    _badge(d, w // 2 - 200, 820, "SAVE £330", _font(44, bold=True), WHITE, GREEN_DARK)
    # the badge is left-aligned by x; rebuild centred manually
    txt = "SAVE £330"
    f_save = _font(44, bold=True)
    tw = d.textbbox((0, 0), txt, font=f_save)[2]
    # blank out the earlier left-aligned attempt
    d.rectangle([0, 800, w, 900], fill=GREEN)
    badge_w = tw + 60
    bx = (w - badge_w) // 2
    d.rounded_rectangle([bx, 810, bx + badge_w, 880], radius=16, fill=GREEN_DARK)
    d.text((w // 2, 822), txt, font=f_save, fill=WHITE, anchor="mt")

    _brand_footer(d, w, h - 100)
    out = OUT_DIR / "ad1-price-offer.png"
    img.save(out, "PNG", optimize=True)
    return out


# ============================================================
# Ad 2 — Problem / solution (1080x1080)
# ============================================================
def ad2():
    w, h = 1080, 1080
    img = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, w, 16], fill=GREEN)

    # eyebrow
    _badge(d, 80, 70, "BOURNEMOUTH", _font(28, bold=True), WHITE, GREEN)

    f_hook = _font(76, bold=True)
    f_sub = _font(42)
    f_body = _font(36)
    f_cta = _font(46, bold=True)

    hook_lines = _wrap(d, "Moving, renovating, or run out of space?", f_hook, w - 160)
    _draw_centered_lines(d, hook_lines, f_hook, 200, w, INK, line_gap=18)

    # divider
    d.rectangle([w // 2 - 60, 460, w // 2 + 60, 468], fill=ACCENT)

    sub_lines = _wrap(
        d,
        "Store it 5 minutes from home. Dry, secure 20ft "
        "containers with 24/7 drive-up access.",
        f_sub,
        w - 160,
    )
    _draw_centered_lines(d, sub_lines, f_sub, 510, w, INK, line_gap=10)

    body_lines = _wrap(
        d,
        "First 4 weeks free · Then £55/week · No long tie-in",
        f_body,
        w - 200,
    )
    _draw_centered_lines(d, body_lines, f_body, 740, w, GREEN, line_gap=8)

    # CTA pill
    txt = "Get Your Quote →"
    tw = d.textbbox((0, 0), txt, font=f_cta)[2]
    bw = tw + 80
    bx = (w - bw) // 2
    d.rounded_rectangle([bx, 860, bx + bw, 940], radius=40, fill=GREEN)
    d.text((w // 2, 872), txt, font=f_cta, fill=WHITE, anchor="mt")

    _brand_footer(d, w, h - 100)
    out = OUT_DIR / "ad2-problem-solution.png"
    img.save(out, "PNG", optimize=True)
    return out


# ============================================================
# Ad 3 — Trust / local (1080x1080)
# ============================================================
def ad3():
    w, h = 1080, 1080
    img = Image.new("RGB", (w, h), GREEN_DARK)
    d = ImageDraw.Draw(img)
    # paper card centred for warmth + readability
    card_x1, card_y1, card_x2, card_y2 = 80, 200, w - 80, h - 200
    d.rounded_rectangle([card_x1, card_y1, card_x2, card_y2], radius=32, fill=PAPER)

    # top tag
    _badge(d, 80, 80, "FAMILY-RUN · BOURNEMOUTH", _font(26, bold=True), GREEN_DARK, ACCENT)

    f_quote = _font(56, bold=True)
    f_body = _font(34)
    f_tag = _font(28, bold=True)

    lines = _wrap(d, "Locally-owned storage that picks up the phone.", f_quote, card_x2 - card_x1 - 100)
    _draw_centered_lines(d, lines, f_quote, card_y1 + 80, w, INK, line_gap=14)

    body = _wrap(
        d,
        "Family-run container storage at 106 Provence Drive. "
        "Insulated, CCTV-monitored, drive-up access whenever you need it.",
        f_body,
        card_x2 - card_x1 - 120,
    )
    _draw_centered_lines(d, body, f_body, card_y1 + 320, w, INK, line_gap=8)

    # offer line
    d.text(
        (w // 2, card_y2 - 130),
        "Your first month — on us.",
        font=_font(40, bold=True),
        fill=GREEN,
        anchor="mt",
    )
    d.text(
        (w // 2, card_y2 - 80),
        "01202 113255",
        font=f_tag,
        fill=GREEN_DARK,
        anchor="mt",
    )

    _brand_footer(d, w, h - 100)
    out = OUT_DIR / "ad3-trust-local.png"
    img.save(out, "PNG", optimize=True)
    return out


# ============================================================
# Ad 4 — Story / Reels (1080x1920 vertical)
# ============================================================
def ad4():
    w, h = 1080, 1920
    img = Image.new("RGB", (w, h), GREEN)
    d = ImageDraw.Draw(img)
    # bold accent strip top + bottom
    d.rectangle([0, 0, w, 24], fill=ACCENT)
    d.rectangle([0, h - 140, w, h], fill=GREEN_DARK)

    # photo zone placeholder (top 45% — drop a real container shot here later)
    photo_h = int(h * 0.45)
    d.rectangle([0, 24, w, 24 + photo_h], fill=GREEN_DARK)
    f_ph = _font(34)
    d.text(
        (w // 2, 24 + photo_h // 2 - 30),
        "[ drop your real container photo here ]",
        font=f_ph,
        fill=MUTED,
        anchor="mm",
    )
    d.text(
        (w // 2, 24 + photo_h // 2 + 20),
        "1080 × ~860 px",
        font=_font(26),
        fill=MUTED,
        anchor="mm",
    )

    # offer block on the green
    y = 24 + photo_h + 80
    f_huge = _font(140, bold=True)
    f_lead = _font(54, bold=True)
    f_body = _font(38)
    f_cta = _font(48, bold=True)

    d.text((w // 2, y), "4 WEEKS", font=f_huge, fill=WHITE, anchor="mt")
    y += 160
    d.text((w // 2, y), "FREE", font=f_huge, fill=ACCENT, anchor="mt")
    y += 200
    d.text((w // 2, y), "STORAGE", font=f_lead, fill=WHITE, anchor="mt")
    y += 80
    d.text((w // 2, y), "BOURNEMOUTH", font=f_lead, fill=WHITE, anchor="mt")
    y += 110

    body_lines = _wrap(
        d,
        "20ft insulated containers · 24/7 drive-up access · CCTV · £55/wk after",
        f_body,
        w - 160,
    )
    _draw_centered_lines(d, body_lines, f_body, y, w, MUTED, line_gap=8)

    # CTA
    txt = "Tap to Get a Quote →"
    tw = d.textbbox((0, 0), txt, font=f_cta)[2]
    bw = tw + 100
    bx = (w - bw) // 2
    cta_y = h - 280
    d.rounded_rectangle([bx, cta_y, bx + bw, cta_y + 100], radius=50, fill=ACCENT)
    d.text((w // 2, cta_y + 22), txt, font=f_cta, fill=GREEN_DARK, anchor="mt")

    # footer
    d.text(
        (w // 2, h - 100),
        "MAGNA PARK SELF STORE",
        font=_font(30, bold=True),
        fill=WHITE,
        anchor="mt",
    )
    d.text(
        (w // 2, h - 62),
        "magnaparkselfstore.co.uk  |  01202 113255",
        font=_font(24),
        fill=MUTED,
        anchor="mt",
    )

    out = OUT_DIR / "ad4-story.png"
    img.save(out, "PNG", optimize=True)
    return out


if __name__ == "__main__":
    files = [ad1(), ad2(), ad3(), ad4()]
    print("\nGenerated:")
    for f in files:
        print(f"  {f}")
