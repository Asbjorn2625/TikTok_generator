# TikTok Generator

Automatically generate TikTok-ready videos with AI-narrated stories and synced subtitles.

Give it a YouTube video (for background footage) and a topic — it uses a local Llama2 model to write a short story, converts it to speech with TikTok's TTS API, crops the video to 9:16, and overlays timed subtitles. Out comes a video ready to upload.

## How It Works

1. **Download** — Grabs a 720p video from YouTube as background footage
2. **Crop** — Converts to TikTok's 9:16 portrait aspect ratio
3. **Generate audio** — Llama2 writes a story based on your topic, then TikTok's TTS API voices it
4. **Align** — Syncs the narration audio to a random segment of the background video
5. **Subtitle** — Uses Whisper to transcribe the audio with word-level timestamps and burns in subtitles

## Prerequisites

- Docker with NVIDIA GPU support (for Ollama/Llama2)
- An NVIDIA GPU

## Getting Started

```bash
# Clone the repo
git clone https://github.com/Asbjorn2625/TikTok_generator.git
cd TikTok_generator

# Build and start the container (pulls the llama2-uncensored model automatically)
docker compose up --build
```

## Usage

```python
from Lib.Generator import Tiktok as tt

vid = tt.TikTok_generator(
    filename="MyTikTok",
    url="https://www.youtube.com/watch?v=VIDEO_ID"
)

# You'll be prompted: "What is the subject of your Tiktok?"

vid.download_video()
vid.crop_video()
vid.generate_audio()
vid.align_video_and_audio()
vid.add_subtitles()
```

Or use the `main()` method to run the full pipeline (minus subtitles):

```python
vid.main()
```

## Project Structure

```
app/
  main.py                    # Entry point / example usage
  Lib/
    Generator/
      Tiktok.py              # TikTok_generator class (core pipeline)
    TTS/
      Text2Speech.py         # TikTok TTS API wrapper
Configs/
  policy.xml                 # ImageMagick security policy
Dockerfile
docker-compose.yaml
requirements.txt
```

## Available TTS Voices

The TTS module supports 60+ voices including:

- **Disney** — Ghost Face, Chewbacca, C3PO, Stitch, Stormtrooper, Rocket
- **English** — AU, UK, and US male/female voices
- **European** — French, German, Spanish
- **Americas** — Spanish MX, Portuguese BR
- **Asian** — Indonesian, Japanese, Korean
- **Singing** — Alto, Tenor, Warmy Breeze, Sunshine Soon
- **Other** — Narrator, Wacky, Peaceful

Change the voice in `generate_audio()` by passing a different voice ID to `TiktokTTS()` (e.g. `en_male_narration`).

## License

MIT
