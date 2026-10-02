# 🎬 Mind Mechanics — Autonomous Faceless YouTube Studio

A 100% free, fully automated AI pipeline that **researches, scripts, narrates,
renders, and uploads** faceless YouTube videos — configured for the
**Mind Mechanics** channel (psychology of decision-making) and driven by a
scheduled **GitHub Actions agent** that runs the whole pipeline autonomously,
every day, with zero human interaction.

Based on [raunakpatil/youtube-agentic-ai-studio](https://github.com/raunakpatil/youtube-agentic-ai-studio).

```
GitHub Actions (daily 14:30 UTC)
        │
        ▼
  Research [Gemini] → Script [Gemini] → Images [Pexels]
        → Narration [Edge TTS] → Video render [MoviePy]
        → Auto-approve → Upload [YouTube Data API]
```

---

## ⚙️ Channel configuration (and why these values)

All tuning lives in [`config.py`](config.py). The choices below were picked to
maximise views quickly for this niche:

| Setting | Value | Why it wins |
|---|---|---|
| `CHANNEL_NAME` | **Mind Mechanics** | Short, alliterative, instantly brandable. |
| `CHANNEL_DESCRIPTION` | Decision psychology + behavioral economics, story-driven, curiosity-gap hooks | This text drives Gemini's topic research. Naming reference channels (Hidden Brain, Lex Fridman, Freakonomics, Huberman), concrete topic angles (dopamine/duomscrolling, sunk cost, anchoring) and the 25–40 audience is what turns generic topics into shareable ones. |
| `VOICE_ID` | **en-US-AndrewNeural** | The most battle-tested free narration voice in the edge-tts community — warm, authoritative, podcast register that matches the target audience — and confirmed to emit the word-level timings this renderer needs for caption sync. `en-GB-RyanNeural` is the drop-in alternative for a BBC-doc feel. |
| `VOICE_RATE` / `VOICE_PITCH` | `-3%` / `-2Hz` | Slightly slower + deeper = narration gravitas without dragging retention. |
| `GEMINI_MODEL` | **gemini-2.5-flash** | Highest script quality on the free tier — hooks and scripts are the #1 retention lever; the 8-model fallback chain absorbs its smaller quota. |
| `COLORS.primary` / `highlight` | Indigo `(99,102,241)` + amber `(251,191,36)` | Amber-on-deep-blue is one of the highest-CTR pairings for educational content (reported +24–28% CTR uplift vs neutrals), and blue signals trust. |
| `CROSSFADE_DURATION` | `0.7` | Smooth, documentary pacing this niche expects. |
| `BROLL_INTERVAL` | `7.0` (was 10) | More frequent visual change-ups = better attention/retention. |
| `OVERLAY_OPACITY` | `0.55` (was 0.62) | Brighter frames keep viewers engaged; captions stay legible on their pill backgrounds. |
| `VIDEO_CATEGORY_ID` | `27` (Education) | Correct shelf + advertiser-friendly. |

> **One-click lever while the channel is new:** set the repo *variable*
> `VIDEO_PRIVACY=unlisted` (Settings → Secrets and variables → Actions →
> Variables) to review each daily video before making it public.

---

## 🖥️ Run locally (optional)

```bash
pip install -r requirements.txt
cp .env.example .env        # then paste your GEMINI_API_KEY + PEXELS_API_KEY
python pipeline.py          # full pipeline + browser review dashboard
# or: python gui.py         # visual dashboard at http://localhost:7842
```

Free keys: [Gemini](https://aistudio.google.com/apikey) (1500 req/day) ·
[Pexels](https://www.pexels.com/api/) (200 req/h).

Full first-time guide (including YouTube OAuth): [`SETUP.md`](SETUP.md).

---

## 🤖 The autonomous GitHub Actions agent

The workflow [`.github/workflows/youtube-agent.yml`](.github/workflows/youtube-agent.yml)
runs **daily at 14:30 UTC** (≈10:30 AM US Eastern — indexed before the US
evening peak) and can also be triggered manually from the **Actions** tab.
It sets `AUTO_APPROVE=true`, which skips the interactive review step and
publishes directly (see `pipeline.py`).

### Activate it — 4 secrets

Add these under **Settings → Secrets and variables → Actions → Repository secrets**:

| Secret | Required | What it is |
|---|---|---|
| `GEMINI_API_KEY` | ✅ | Free key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey) |
| `PEXELS_API_KEY` | ✅ | Free key from [pexels.com/api](https://www.pexels.com/api/) |
| `YT_CLIENT_SECRET_B64` | for upload | `base64 -w0 client_secret.json` from your Google Cloud OAuth client |
| `YT_TOKEN_PICKLE_B64` | for upload | `base64 -w0 youtube_token.pickle` (see below) |

### Generating the YouTube token (one-time, ~3 min)

GitHub Actions can't do an interactive OAuth sign-in, so create the refresh
token once on your own machine:

```bash
# 1. Put your real client_secret.json (Google Cloud Console, Desktop app OAuth
#    client with YouTube Data API v3 enabled, your account as Test User) in
#    this folder, then:
python - <<'EOF'
from uploader.youtube import _get_service
_get_service()          # opens a browser, you sign in once
print("youtube_token.pickle created ✅")
EOF

# 2. Encode both files into secrets (Linux/macOS):
base64 -w0 client_secret.json    > /tmp/cs.b64
base64 -w0 youtube_token.pickle  > /tmp/tok.b64
# then paste each file's content into the corresponding repo secret
```

> ⚠️ While your Google Cloud OAuth app is in **Testing** mode, refresh tokens
> expire after 7 days — publish the OAuth consent screen (or re-generate the
> pickle) to keep the daily agent uploading unattended.

### Behavior without upload secrets

The agent still runs the full pipeline — research, script, narration, render —
and saves `final_video.mp4`, `script.json`, and `research.json` as workflow
**artifacts** (14-day retention), so you can grab the video and upload it
manually until OAuth is configured.

---

## 📁 Project structure

```
├── pipeline.py              ← full pipeline (AUTO_APPROVE aware)
├── gui.py                   ← visual dashboard (local use)
├── config.py                ← channel identity, voice, colours, video style
├── .github/workflows/youtube-agent.yml   ← the autonomous agent
├── agents/                  ← Gemini researcher + scriptwriter (fallback chain)
├── video/                   ← Edge-TTS narrator, Pexels stock, MoviePy renderer
├── review/                  ← Flask approval dashboard (skipped in CI)
├── uploader/                ← YouTube Data API v3 upload
└── music library/           ← drop MP3s here for background music
```

## 💡 Operational tips for maximum views

1. **Cadence** — daily uploads compound recommendations; the cron already does this.
2. **Watch the artifacts** for the first week and prune bad topic angles by
   adding them to `banned_topics.txt`.
3. **Titles/thumbnails come from the script agent** — the curiosity-gap
   instructions in `CHANNEL_DESCRIPTION` are what make them clicky.
4. **Music** — add 2–3 royalty-free ambient tracks to `music library/` for a
   retention boost at 12% volume (already configured).
