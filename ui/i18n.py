"""
Internationalization (i18n) strings for EditorGIF.
Supports Portuguese (pt-BR) and English (en-US).
"""

MESSAGES = {
    "pt_BR": {
        "page_title": "EditorGIF",
        "hero_title": "👾 EditorGIF",
        "hero_subtitle": "Converta vídeos em GIFs transparentes e Sprite Sheets para jogos com Inteligência Artificial",
        "badge_onnx": "⚡ Segmentação IA ONNX",
        "badge_ghost": "🎮 Prevenção de Fantasma (Disposal=2)",
        "badge_defringe": "✨ Defringe Alfa 1-Bit",
        
        "language_select": "Idioma / Language",
        
        "step_1_title": "1. Carregar Vídeo",
        "upload_label": "Envie o vídeo ou GIF do personagem (MP4, WebM, MOV, AVI, GIF)",
        "upload_help": "Envie clipes curtos de ações de personagens, ataques, animações paradas ou de caminhada.",
        "video_caption": "ℹ️ Original: {width}x{height} | {duration:.2f}s | {fps:.1f} FPS",
        
        "step_2_title": "2. Controles de Animação e IA",
        "time_slider_label": "Intervalo de Tempo da Animação (segundos)",
        "time_slider_help": "Selecione o momento exato de início e fim do ciclo da animação do personagem.",
        "target_fps_label": "FPS Alvo do Jogo",
        "target_fps_help": "10-15 FPS é o padrão da indústria para ciclos de animação de jogos 2D indie/pixel art.",
        "scale_slider_label": "Escala de Resolução (%)",
        "scale_slider_help": "Reduz a resolução para coincidir com a escala do sprite no jogo e acelerar o processamento da IA.",
        
        "advanced_title": "🛠️ Configurações Avançadas de Transparência e Otimização",
        "model_label": "Modelo de IA para Segmentação",
        "model_help": "u2net é o modelo padrão de uso geral. silueta é ultraleve.",
        "alpha_threshold_label": "Sensibilidade Alfa (Corte de Borda da Máscara)",
        "alpha_threshold_help": "Pixels com alfa abaixo deste limiar tornam-se 100% transparentes (elimina halos borrados).",
        "defringe_label": "Defringe de Borda (Limpeza de halos e vazamento de cores)",
        "defringe_help": "Zera os canais de cor dos pixels transparentes para evitar contornos indesejados.",
        "autocrop_label": "Corte Automático na Silhueta do Personagem",
        "autocrop_help": "Recorta as margens transparentes vazias ao redor do personagem de forma uniforme em todos os frames.",
        
        "process_button": "⚡ Processar e Gerar GIF Transparente",
        "prog_extract": "Extraindo e reamostrando quadros do vídeo...",
        "prog_extracted": "Extraídos {count} quadros. Carregando Modelo de IA ({model})...",
        "prog_segment": "Segmentação IA: Quadro {current} de {total}...",
        "prog_gif": "Compilando GIF transparente (Disposal=2)...",
        "prog_sheet": "Compilando Sprite Sheet de 32-bits...",
        "prog_done": "Concluído com sucesso! ✨",
        "toast_success": "GIF Transparente e Sprite Sheet gerados com sucesso!",
        "error_processing": "Erro durante o processamento: {error}",
        "error_reading": "Erro ao ler o vídeo: {error}",
        
        "step_3_title": "3. Visualização e Download do Asset",
        "meta_res": "Resolução:",
        "meta_frames": "Total de Quadros:",
        "meta_frames_unit": "quadros",
        "meta_size": "Tamanho do Arquivo:",
        "meta_duration": "Duração Total:",
        "preview_title": "Pré-visualização da Animação Transparente (Fundo Xadrez):",
        
        "trim_section_title": "✂️ Recortar e Ajustar Velocidade do GIF",
        "trim_section_help": "Escolha os segundos de início e fim e a velocidade de reprodução para baixar o GIF sem reprocessar a IA.",
        "trim_slider_label": "Intervalo de Segundos do Recorte",
        "speed_slider_label": "⚡ Velocidade de Reprodução do GIF",
        "speed_slider_help": "Aumente a velocidade (ex: 1.5x, 2.0x, 3.0x) para tornar a animação do GIF mais rápida, ou diminua para câmera lenta.",
        "trim_stats": "⏱️ Início: {start:.2f}s | Fim: {end:.2f}s | Duração: {duration:.2f}s ({frames} quadros) | Velocidade: {speed}x",
        "trim_preview_title": "Pré-visualização da Animação:",
        "tab_trimmed": "✂️ Animação Recortada",
        "tab_full": "🎬 Animação Completa",
        
        "btn_download_gif": "⬇️ Baixar GIF Transparente (.gif)",
        "btn_download_sheet": "⬇️ Baixar Sprite Sheet do Jogo (.png)",
        "btn_download_trimmed_gif": "⬇️ Baixar GIF Recortado ({start:.2f}s a {end:.2f}s)",
        "btn_download_trimmed_sheet": "⬇️ Baixar Sprite Sheet Recortado ({frames} quadros)",
        "btn_download_full_gif": "⬇️ Baixar GIF Completo ({duration:.2f}s)",
        "btn_download_full_sheet": "⬇️ Baixar Sprite Sheet Completo",
        
        "guide_title": "🎮 Guia de Integração em Game Engines",
        "guide_content": """
- **Godot Engine**:
  - GIF: Importe direto ou use a **Sprite Sheet (.png)** em um nó `AnimatedSprite2D`. Defina `Hframes` para a quantidade total de quadros.
- **Unity**:
  - Use a **Sprite Sheet (.png)**. No Inspector da textura, marque *Sprite Mode* como *Multiple*, abra o *Sprite Editor* e fatie por grade ou contagem de células.
- **Phaser / Web Game Engines**:
  - Carregue o spritesheet via código com `this.load.spritesheet('heroi', 'sprite_sheet_transparent.png', { frameWidth, frameHeight })`.
""",
        "empty_preview": "Sua animação transparente aparecerá aqui rodando em loop sobre este fundo xadrez assim que for processada."
    },
    
    "en_US": {
        "page_title": "EditorGIF",
        "hero_title": "👾 EditorGIF",
        "hero_subtitle": "Convert live videos into game-ready transparent GIFs & Sprite Sheets with AI",
        "badge_onnx": "⚡ ONNX AI Segmentation",
        "badge_ghost": "🎮 Disposal=2 Ghost Prevention",
        "badge_defringe": "✨ 1-Bit Alpha Defringe",
        
        "language_select": "Language / Idioma",
        
        "step_1_title": "1. Ingest Video",
        "upload_label": "Upload character video or GIF (MP4, WebM, MOV, AVI, GIF)",
        "upload_help": "Upload short clips of character actions, attacks, idle or walk animations.",
        "video_caption": "ℹ️ Original: {width}x{height} | {duration:.2f}s | {fps:.1f} FPS",
        
        "step_2_title": "2. Animation & AI Controls",
        "time_slider_label": "Animation Time Interval (seconds)",
        "time_slider_help": "Select the exact start and end moment of the character animation loop.",
        "target_fps_label": "Target Game FPS",
        "target_fps_help": "10-15 FPS is the industry standard for 2D indie/pixel game animation cycles.",
        "scale_slider_label": "Resolution Scale (%)",
        "scale_slider_help": "Reduces resolution to match game sprite scale and accelerate AI processing.",
        
        "advanced_title": "🛠️ Advanced Transparency & Optimization Settings",
        "model_label": "AI Segmentation Model",
        "model_help": "u2net is the standard general-purpose model. silueta is lightweight.",
        "alpha_threshold_label": "Alpha Threshold (Edge Matte Cutoff)",
        "alpha_threshold_help": "Pixels with alpha below this threshold are made 100% transparent.",
        "defringe_label": "Edge Defringing (Clean background color halos)",
        "defringe_help": "Zeros out transparent pixel color channels to prevent matte color bleed.",
        "autocrop_label": "Auto-Crop to Character Silhouette",
        "autocrop_help": "Crops empty transparent margins around the character uniformly across all frames.",
        
        "process_button": "⚡ Process & Generate Transparent GIF",
        "prog_extract": "Extracting and resampling video frames...",
        "prog_extracted": "Extracted {count} frames. Loading AI Model ({model})...",
        "prog_segment": "AI Segmentation: Frame {current} of {total}...",
        "prog_gif": "Compilando transparent GIF (Disposal=2)...",
        "prog_sheet": "Compilando 32-bit Sprite Sheet...",
        "prog_done": "Done! ✨",
        "toast_success": "Transparent GIF and Sprite Sheet generated successfully!",
        "error_processing": "Error during processing: {error}",
        "error_reading": "Error reading video: {error}",
        
        "step_3_title": "3. Game Asset Preview & Download",
        "meta_res": "Resolution:",
        "meta_frames": "Total Frames:",
        "meta_frames_unit": "frames",
        "meta_size": "File Size:",
        "meta_duration": "Total Duration:",
        "preview_title": "Transparent Animation Preview (Checkerboard Canvas):",
        
        "trim_section_title": "✂️ Trim & Adjust GIF Speed",
        "trim_section_help": "Choose the start/end seconds and playback speed multiplier to download the GIF without re-running AI processing.",
        "trim_slider_label": "Trim Interval (seconds)",
        "speed_slider_label": "⚡ GIF Playback Speed",
        "speed_slider_help": "Increase speed (e.g. 1.5x, 2.0x, 3.0x) to make the GIF animate faster, or decrease for slow motion.",
        "trim_stats": "⏱️ Start: {start:.2f}s | End: {end:.2f}s | Duration: {duration:.2f}s ({frames} frames) | Speed: {speed}x",
        "trim_preview_title": "Animation Preview:",
        "tab_trimmed": "✂️ Trimmed Animation",
        "tab_full": "🎬 Full Animation",
        
        "btn_download_gif": "⬇️ Download Transparent GIF (.gif)",
        "btn_download_sheet": "⬇️ Download Game Sprite Sheet (.png)",
        "btn_download_trimmed_gif": "⬇️ Download Trimmed GIF ({start:.2f}s to {end:.2f}s)",
        "btn_download_trimmed_sheet": "⬇️ Download Trimmed Sprite Sheet ({frames} frames)",
        "btn_download_full_gif": "⬇️ Download Full GIF ({duration:.2f}s)",
        "btn_download_full_sheet": "⬇️ Download Full Sprite Sheet",
        
        "guide_title": "🎮 Game Engine Integration Guide",
        "guide_content": """
- **Godot Engine**:
  - GIF: Drop into project, or use the **Sprite Sheet (.png)** with an `AnimatedSprite2D` node. Set `Hframes` to the total frame count.
- **Unity**:
  - Use the **Sprite Sheet (.png)**. In Sprite Import settings, set *Sprite Mode* to *Multiple*, open *Sprite Editor*, and slice by grid/cell count.
- **Phaser / Web Game Engines**:
  - Load the sprite sheet using `this.load.spritesheet('character', 'sprite_sheet_transparent.png', { frameWidth, frameHeight })`.
""",
        "empty_preview": "Your transparent animation will appear here looping over this checkerboard canvas once processed."
    }
}


def get_text(key: str, lang: str = "pt_BR", **kwargs) -> str:
    """
    Returns the localized string for the given key and language.
    """
    lang_dict = MESSAGES.get(lang, MESSAGES["pt_BR"])
    text = lang_dict.get(key, MESSAGES["en_US"].get(key, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
