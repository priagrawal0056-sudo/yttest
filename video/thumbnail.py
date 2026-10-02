"""
Thumbnail Generator
===================
Programmatically renders a 1280×720 YouTube thumbnail — the single biggest
CTR lever on the platform:

  • Hero image from the script's first illustrated section, slightly blurred
    so text pops
  • Dark overlay + bottom gradient for guaranteed text contrast
  • Video title in large bold caps, bottom-anchored, with the LAST line in
    the brand highlight colour (the two-tone title pattern common in
    high-CTR educational thumbnails)
  • Channel-name badge in the brand primary colour

No AI image generation, no API keys — Pillow + the brand palette from
config.py. Failures are non-fatal: the pipeline continues without one.

Public API
----------
  create_thumbnail(script, image_map, output_dir) -> str   (path to JPEG)
"""

import os
import re
import unicodedata

from PIL import Image, ImageDraw, ImageFilter, ImageFont

import config

THUMB_W, THUMB_H = 1280, 720
_MARGIN_X        = 72
_MARGIN_BOTTOM   = 88
_MAX_LINES       = 3
_JPEG_QUALITY    = 92


# ══════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════

def _clean_title(title: str) -> str:
    """Strip emojis/symbols (DejaVu can't draw them) and collapse whitespace."""
    cleaned = "".join(
        ch for ch in title
        if unicodedata.category(ch) not in ("So", "Sk", "Cn", "Cs")
        and ord(ch) not in (0xFE0F, 0x200D)
    )
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned or "WATCH THIS"


def _load_font(size: int, weight: str = "bold") -> ImageFont.ImageFont:
    for path in config.FONT_PATHS.get(weight, []):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _pick_hero_image(image_map: dict):
    """First available image, preferring the lowest section id."""
    if not image_map:
        return None
    for key in sorted(image_map.keys()):
        val = image_map[key]
        if isinstance(val, list):
            val = val[0] if val else None
        if val and os.path.exists(val):
            return val
    return None


def _cover_crop(img: Image.Image, w: int, h: int) -> Image.Image:
    """Resize-to-cover then centre-crop (like CSS object-fit: cover)."""
    scale   = max(w / img.width, h / img.height)
    resized = img.resize((int(img.width * scale) + 1,
                          int(img.height * scale) + 1), Image.LANCZOS)
    left = (resized.width  - w) // 2
    top  = (resized.height - h) // 2
    return resized.crop((left, top, left + w, top + h))


def _wrap_lines(draw, words, font, max_width):
    lines, line = [], []
    for word in words:
        trial = " ".join(line + [word])
        if draw.textlength(trial, font=font) <= max_width or not line:
            line.append(word)
        else:
            lines.append(" ".join(line))
            line = [word]
    if line:
        lines.append(" ".join(line))
    return lines


def _fit_title(draw, title, max_width):
    """Largest font size that wraps to ≤ _MAX_LINES and fits vertically."""
    for size in range(110, 44, -4):
        font  = _load_font(size)
        lines = _wrap_lines(draw, title.split(), font, max_width)
        if len(lines) <= _MAX_LINES:
            line_h = font.size * 1.18
            if len(lines) * line_h <= THUMB_H - _MARGIN_BOTTOM - 110:
                return font, lines
    font  = _load_font(48)
    lines = _wrap_lines(draw, title.split(), font, max_width)[:_MAX_LINES]
    return font, lines


# ══════════════════════════════════════════════════════════════
#  PUBLIC API
# ══════════════════════════════════════════════════════════════

def create_thumbnail(script: dict, image_map: dict, output_dir: str) -> str:
    """Render output/thumbnail.jpg from the script + downloaded images."""
    title = _clean_title(script.get("title", config.CHANNEL_NAME)).upper()

    # ── Background: hero image or brand-coloured fallback ─────
    canvas = Image.new("RGB", (THUMB_W, THUMB_H), config.COLORS["background"])
    hero = _pick_hero_image(image_map)
    if hero:
        try:
            base = _cover_crop(Image.open(hero).convert("RGB"), THUMB_W, THUMB_H)
            base = base.filter(ImageFilter.GaussianBlur(1.5))
            canvas.paste(base)
        except Exception as e:
            print(f"   ⚠ Could not use hero image for thumbnail: {e}")

    draw = ImageDraw.Draw(canvas, "RGBA")

    # ── Dark overlay + bottom gradient for text legibility ────
    overlay_alpha = int(255 * getattr(config, "OVERLAY_OPACITY", 0.55))
    draw.rectangle((0, 0, THUMB_W, THUMB_H), fill=(0, 0, 0, overlay_alpha))
    grad_start = THUMB_H // 3
    for y in range(grad_start, THUMB_H):
        alpha = int(190 * (y - grad_start) / (THUMB_H - grad_start))
        draw.line([(0, y), (THUMB_W, y)], fill=(0, 0, 0, alpha))

    # ── Title: bottom-anchored, last line in highlight colour ─
    font, lines = _fit_title(draw, title, THUMB_W - 2 * _MARGIN_X)
    line_h    = int(font.size * 1.18)
    y         = THUMB_H - _MARGIN_BOTTOM - len(lines) * line_h
    white     = config.COLORS["white"]
    highlight = config.COLORS["highlight"]
    for i, line in enumerate(lines):
        color = highlight if i == len(lines) - 1 else white
        draw.text(
            (_MARGIN_X, y), line, font=font, fill=color,
            stroke_width=max(2, font.size // 24), stroke_fill=(0, 0, 0, 255),
        )
        y += line_h

    # ── Channel badge (top-left) ──────────────────────────────
    try:
        primary    = config.COLORS["primary"]
        badge_font = _load_font(34)
        badge_text = config.CHANNEL_NAME.upper()
        bw = int(draw.textlength(badge_text, font=badge_font)) + 44
        bh = 58
        draw.rounded_rectangle((40, 40, 40 + bw, 40 + bh),
                               radius=14, fill=primary + (235,))
        draw.text((62, 51), badge_text, font=badge_font, fill=white)
    except Exception:
        pass   # badge is cosmetic — never fail the render for it

    out_path = os.path.join(output_dir, "thumbnail.jpg")
    canvas.convert("RGB").save(out_path, "JPEG", quality=_JPEG_QUALITY)
    size_kb = os.path.getsize(out_path) // 1024
    print(f"   ✅ Thumbnail rendered: {out_path} ({size_kb} KB)")
    return out_path
