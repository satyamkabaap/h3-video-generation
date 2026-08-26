# 🎬 H3 Video Generation

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## ✨ Overview

Local text-to-video generation using the **MiniMax H3** model, optimized for low VRAM (4GB GPUs). Generate high-quality video clips with audio synchronization, all running offline on your RTX 3050/4050 or similar.

## 🎥 Demo

<div align="center">
  <table>
    <tr>
      <th>Eagle Flight</th>
      <th>Stormy Night</th>
    </tr>
    <tr>
      <td><img src="assets/eagle_preview.gif" width="320"/></td>
      <td><img src="assets/storm_preview.gif" width="320"/></td>
    </tr>
  </table>
  <p><em>Generated with H3 Video Generation – no post-processing.</em></p>
</div>

## 🚀 Features

- **Text-to-Video**: Turn prompts into 5-9 second clips.
- **Audio Sync**: Automatic voice-over generation (via Edge TTS or custom audio).
- **Low VRAM**: Optimized for 4GB GPUs (RTX 3050/3060/4050).
- **Offline First**: No API keys required; runs entirely locally.
- **Flexible**: Adjust length, FPS, seed, and guidance scale.
- **Easy Install**: Single-command setup with `uv` or `pip`.

## 🛠️ Installation

```bash
# Clone the repo
git clone https://github.com/satyamkabaap/h3-video-generation.git
cd h3-video-generation

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
# or using uv (faster)
uv pip install -r requirements.txt
```

## ▶️ Usage

### Basic Text-to-Video
```bash
python h3_run.py --prompt "A majestic eagle soaring over mountains at sunset" --length 125
```

### With Custom Audio
```bash
python h3_run.py --prompt "A futuristic cityscape at night" --audio "my_voiceover.wav"
```

### Advanced Options
```bash
python h3_run.py --help
```

## 📊 Results

| Setting | VRAM Usage | Speed (approx.) | Quality |
|---------|------------|-----------------|---------|
| Default (768x448) | ~3.8 GB | ~200s/3s clip | High detail |
| Low VRAM (608p) | ~3.2 GB | ~150s/3s clip | Good |

*Measured on RTX 3050 4GB laptop GPU.*

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

## 📜 License

Distributed under the MIT License. See `LICENSE` for more information.

## 🙏 Acknowledgments

- [MiniMax H3](https://github.com/Vchitect/LTX-Video) team for the model.
- [sd.cpp](https://github.com/Andreyst/Open-Generative-AI) for efficient inference.
- Edge TTS for free, high-quality voice synthesis.

---

Made with ❤️ for the open-source AI video community.