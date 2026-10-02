import os

# Load .env automatically (local runs). GitHub Actions injects vars directly,
# in which case this is a harmless no-op.
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
except ImportError:
    pass

# ─────────────────────────────────────────────────────────────────────────────
#  YouTube AI Agent Studio — Configuration
#  Channel: Mind Mechanics (decision psychology)
#  Values below were chosen for maximum view velocity — see README
#  ("Why these settings") for the research rationale.
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────
#  API Keys  (all free-tier, read from .env / environment)
# ─────────────────────────────────────────
GEMINI_API_KEY     = os.getenv("GEMINI_API_KEY",     "YOUR_GEMINI_API_KEY")
PEXELS_API_KEY     = os.getenv("PEXELS_API_KEY",     "YOUR_PEXELS_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "YOUR_ELEVENLABS_KEY")  # optional

# ─────────────────────────────────────────
#  Your Channel Identity
#  This text is the #1 lever for views: Gemini uses it to pick topics.
#  Specific niche + named reference channels + format rules = better topics.
# ─────────────────────────────────────────
CHANNEL_DESCRIPTION = """
Mind Mechanics — the psychology and neuroscience of decision-making.
Deep, story-driven explainers on why humans choose what they choose: cognitive
biases, behavioral economics, habit formation, persuasion & influence, risk
perception, the paradox of choice, money decisions, and how AI is reshaping
human judgment.

Style references: Hidden Brain, Lex Fridman, Freakonomics Radio, Andrew
Huberman, Kurzgesagt. Every video opens with a curiosity-gap hook ("Why do
smart people make dumb choices?"), tells one concrete human story, then unpacks
the science with zero jargon. Prefer topics with a trending or counter-intuitive
angle — e.g. dopamine and doomscrolling, why we procrastinate, anchoring in
negotiations, the sunk-cost trap, how algorithms hijack our choices.

Format: 8–12 minute long-form videos, one big idea each, ending with a
practical takeaway the viewer can use the same day.

Target audience: curious adults 25–40 who listen to Hidden Brain and Lex
Fridman, want to understand their own mind, and share videos that make them
say "I never thought about it that way."
"""
CHANNEL_NAME = "Mind Mechanics"   # shown on-screen and in upload metadata

# ─────────────────────────────────────────
#  Voice (Edge TTS — free, no API key)
#  en-US-AndrewNeural — warm, authoritative American male. The most battle-
#  tested narration voice in the edge-tts community, and confirmed by this
#  repo to emit word-level timing (required for caption sync). Fits the
#  Hidden Brain / Lex Fridman podcast register of the target audience.
#  Alternatives (also emit word timings):
#    en-GB-RyanNeural  — British, deep, cinematic (BBC-doc feel)
#    en-US-BrianNeural — US, calm, documentary
#    en-US-GuyNeural   — US, clear, neutral
# ─────────────────────────────────────────
VOICE_ID    = "en-US-AndrewNeural"
VOICE_RATE  = "-3%"     # slightly slower than speech → narration gravitas
VOICE_PITCH = "-2Hz"    # slightly deeper = more cinematic

# ─────────────────────────────────────────
#  AI Model
#  Starting model for the fallback chain — the system auto-switches
#  through all models below if quota or errors are hit.
#  gemini-2.5-flash is the highest-quality free option: better hooks and
#  scripts directly drive retention, so it's worth the smaller daily quota.
#  Options (free tier):
#    gemini-2.5-flash        — highest quality   (500 req/day)  ← chosen
#    gemma-4-31b-it          — Gemma 4 31B       (500 req/day)
#    gemini-2.0-flash        — recommended       (1500 req/day)
#    gemini-2.0-flash-lite   — fastest           (1500 req/day)
#    gemini-1.5-flash-001    — reliable fallback (1500 req/day)
# ─────────────────────────────────────────
GEMINI_MODEL = "gemini-2.5-flash"

# ─────────────────────────────────────────
#  Video Dimensions
# ─────────────────────────────────────────
VIDEO_WIDTH  = 1920
VIDEO_HEIGHT = 1080
VIDEO_FPS    = 24

# YouTube Shorts dimensions (9:16 vertical)
SHORTS_WIDTH  = 1080
SHORTS_HEIGHT = 1920
SHORTS_FPS    = 30

# ─── Visual Style ───────────────────────
# Ken Burns effect: how much to zoom/pan each image
KB_ZOOM_START = 1.00    # starting scale (1.0 = no zoom)
KB_ZOOM_END   = 1.10    # ending scale   (1.1 = 10% zoom in)

# Image crossfade duration (seconds)
# 0.0 = instant cut  |  0.5 = snappy  |  0.7 = smooth  |  1.2 = dreamy
# 0.7 keeps the calm documentary pacing this niche expects.
CROSSFADE_DURATION = 0.7

# Normal video B-roll cycling
# 7s per image (down from 10) → more visual change-ups, better retention.
BROLL_INTERVAL  = 7.0    # seconds each image stays on screen
BROLL_XFADE_DUR =  1.2   # crossfade duration (must be < BROLL_INTERVAL)

# Render quality preset (ffmpeg libx264)
# "ultrafast" = fastest/largest  |  "veryfast" = recommended  |  "medium" = best quality
# Kept ultrafast so the free GitHub Actions runner finishes inside its window.
RENDER_PRESET = "ultrafast"

# Overlay opacity: lower = more image visible but text harder to read (0–1)
# 0.55 = brighter, more engaging frames; captions remain legible on the
# pill backgrounds the renderer draws behind them.
OVERLAY_OPACITY = 0.55

# Colour palette — indigo + amber is one of the highest-CTR combinations
# for educational content (yellow/amber accent on a deep blue-black base
# reports +24–28% CTR uplift vs neutrals; blue also signals trust).
COLORS = {
    "background": (10,  10,  20),
    "overlay":    (0,   0,   0),
    "primary":    (99,  102, 241),   # indigo — brand colour
    "accent":     (167, 139, 250),   # purple
    "highlight":  (251, 191,  36),   # amber — titles / key words
    "white":      (255, 255, 255),
    "light":      (199, 210, 254),   # indigo-200
    "success":    (52,  211, 153),
    "red":        (239,  68,  68),
}

# Fonts — add your own .ttf paths for best results; system falls back gracefully
FONT_PATHS = {
    "bold":    [
        "C:/Windows/Fonts/Impact.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "/System/Library/Fonts/Supplemental/Impact.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "regular": [
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
    "light":   [
        "C:/Windows/Fonts/segoeuil.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
}

# ─────────────────────────────────────────
#  Review Server
# ─────────────────────────────────────────
REVIEW_PORT = 5050

# ─────────────────────────────────────────
#  Automation / headless mode
# ─────────────────────────────────────────
# When true (env AUTO_APPROVE=true), the pipeline skips the interactive
# Flask review dashboard and publishes directly. The GitHub Actions agent
# sets this; keep it false for local interactive runs.
AUTO_APPROVE = os.getenv("AUTO_APPROVE", "false").strip().lower() in (
    "1", "true", "yes", "on",
)

# ─────────────────────────────────────────
#  YouTube Upload
# ─────────────────────────────────────────
YOUTUBE_CLIENT_SECRET = "client_secret.json"   # OAuth credentials file (see SETUP.md)
YOUTUBE_SCOPES        = ["https://www.googleapis.com/auth/youtube.upload"]
VIDEO_CATEGORY_ID     = "27"       # 27 = Education
# Overridable via env/Actions variable so you can switch to "unlisted"
# without touching code while the channel is new.
VIDEO_PRIVACY         = os.getenv("VIDEO_PRIVACY", "public")   # public | unlisted | private

# ─────────────────────────────────────────
#  Background Music
#  Drop MP3/WAV files into the  music library/  folder.
#  Tracks are shuffled and looped automatically to match video length.
# ─────────────────────────────────────────
MUSIC_ENABLED     = True
MUSIC_VOLUME      = 0.12          # 0.0–1.0  (0.12 = subtle underscore)
MUSIC_LIBRARY_DIR = os.path.join(os.path.dirname(__file__), "music library")

# ─────────────────────────────────────────
#  Paths  (do not change unless you know what you're doing)
# ─────────────────────────────────────────
OUTPUT_DIR   = "output"
IMAGES_DIR   = "output/images"
