# 👾 EditorGIF

**EditorGIF** is an open-source, production-ready desktop tool designed for game developers, animators, and digital artists. It converts video clips into game-ready transparent GIFs and 32-bit Sprite Sheets using state-of-the-art AI background segmentation (rembg / ONNX).

---

## 🌟 Key Features

- 🌐 **Suporte Nativo a Português (PT-BR)**: Interface totalmente em Português do Brasil por padrão, com alternador rápido de idioma (PT-BR / EN).
- 🧠 **AI Background Removal**: Frame-by-frame foreground extraction powered by ONNX neural networks (`u2net`, `isnet-general-use`, `birefnet-general`, `silueta`).
- 🎮 **Game-Engine Ready GIF Compilation**:
  - **Disposal Method 2 (`restore to background`)**: Eliminates ghosting and trailing character artifacts across loops.
  - **1-bit Alpha Defringing & Thresholding**: Prevents dark/white edge halos and color bleeding.
- 🖼️ **Dual Output Formats**:
  - **Transparent GIF (`.gif`)**: Ideal for lightweight previews, web embeds, and direct animation playback.
  - **32-bit Sprite Sheet (`.png`)**: Perfect for Godot (`AnimatedSprite2D`), Unity (Sprite Editor), and Phaser.
- 🎛️ **Granular Controls**:
  - Exact time interval trimming (Start / End seconds).
  - Target game FPS selection (6, 8, 10, 12, 15, 20, 24, 30 FPS).
  - Resolution scaling (20% to 100%).
  - Alpha cutoff sensitivity slider.
  - Auto-crop bounding box to keep the character centered without blank margins.
- ✂️ **Recorte Temporal Pós-Transparência (Download por Segundos)**: Escolha os segundos exatos de início e fim para recortar e baixar o GIF transparente instantaneamente, sem precisar reprocessar a IA.
- 📁 **Suporte a Vídeos e GIFs**: Aceita formatos MP4, WebM, MOV, AVI e também `.gif` pré-existentes.
- 🏁 **Checkerboard Live Preview**: Live base64-rendered preview on a cyber checkerboard canvas to inspect transparency before downloading.

---

## 🚀 Quick Start (Como Executar)

### 1. Clonar o Repositório
```bash
git clone https://github.com/CarlosFelipeLessa/editorgif.git
cd editorgif
```

### 2. Requisitos & Instalação de Dependências
- Python 3.10+ (testado no Python 3.14 x64 Windows)
- Navegador Web moderno

```bash
pip install -r requirements.txt
```

### 3. Iniciar o Programa
No Windows, dê um duplo-clique no arquivo:
```bash
run_app.bat
```
Ou execute diretamente pelo terminal:
```bash
python -m streamlit run ui/app.py
```

---

## 📁 Project Architecture

```
editorgif/
├── core/
│   ├── __init__.py
│   ├── video_processor.py    # OpenCV video reading, interval trimming, FPS resample, scaling
│   ├── bg_remover.py         # rembg ONNX session management, alpha thresholding & defringing
│   └── gif_compiler.py       # GIF89a transparency palette quantization (disposal=2) & Sprite Sheet
├── ui/
│   ├── __init__.py
│   ├── app.py                # Streamlit user interface with state management & live download
│   ├── i18n.py               # Multilingual translations (Português PT-BR / English)
│   └── styles.py             # Custom CSS, cyber-dark theme & checkerboard canvas
├── test_pipeline.py          # End-to-end automated smoke test
├── run_app.bat               # Windows one-click launcher
├── requirements.txt          # Python dependencies
├── gemini.md                 # Project constitution & architectural rules
├── task_plan.md              # BLAST execution roadmap
├── findings.md               # Technical research log
└── progress.md               # Execution & test records
```

---

## 🎮 Game Engine Integration Guide

### Godot 4.x
1. Import the generated `sprite_sheet_transparent.png`.
2. Add an `AnimatedSprite2D` node to your Scene.
3. Under **Frames**, create a new `SpriteFrames`.
4. Add frames from the sprite sheet and specify the number of horizontal frames (`Hframes`).

### Unity
1. Drag `sprite_sheet_transparent.png` into your `Assets/Sprites` folder.
2. In the Inspector:
   - **Texture Type**: `Sprite (2D and UI)`
   - **Sprite Mode**: `Multiple`
   - **Filter Mode**: `Point (no filter)` (if pixel art) or `Bilinear`
3. Click **Sprite Editor** -> **Slice** -> By Grid / Cell Count.

### Web / Phaser
```javascript
this.load.spritesheet('hero_attack', 'sprite_sheet_transparent.png', {
    frameWidth: 64,
    frameHeight: 64
});
```

---

## 📄 License
MIT License. Free for commercial and indie game projects.
