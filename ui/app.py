"""
EditorGIF - Main Streamlit Application.
Converts videos into transparent animated GIFs and game sprites with AI background removal.
Includes full multilingual support (pt-BR / en-US).
"""
import base64
import os
import sys
import tempfile
from typing import Optional
import streamlit as st

# Add workspace root to sys.path so core modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from PIL import Image
from core.video_processor import extract_frames, get_video_metadata
from core.bg_remover import get_rembg_session, process_frames_pipeline
from core.gif_compiler import (
    compile_transparent_gif,
    compile_sprite_sheet,
    slice_frames_by_seconds,
    slice_sprite_sheet
)
from ui.styles import CUSTOM_CSS
from ui.i18n import get_text


st.set_page_config(
    page_title="EditorGIF",
    page_icon="👾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom styles
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


def init_state():
    if "lang" not in st.session_state:
        st.session_state.lang = "pt_BR"
    if "gif_bytes" not in st.session_state:
        st.session_state.gif_bytes = None
    if "sheet_bytes" not in st.session_state:
        st.session_state.sheet_bytes = None
    if "sheet_meta" not in st.session_state:
        st.session_state.sheet_meta = None
    if "frames_count" not in st.session_state:
        st.session_state.frames_count = 0
    if "dimensions" not in st.session_state:
        st.session_state.dimensions = (0, 0)
    if "last_processed_file" not in st.session_state:
        st.session_state.last_processed_file = None
    if "rgba_frames" not in st.session_state:
        st.session_state.rgba_frames = None
    if "fps" not in st.session_state:
        st.session_state.fps = 12
    if "speed_mult" not in st.session_state:
        st.session_state.speed_mult = 1.0


init_state()

# Sidebar: Language Selector
with st.sidebar:
    st.markdown("### 🌐 Configurações / Settings")
    selected_lang = st.selectbox(
        "Idioma / Language",
        options=["pt_BR", "en_US"],
        format_func=lambda x: "🇧🇷 Português (Brasil)" if x == "pt_BR" else "🇺🇸 English",
        index=0 if st.session_state.lang == "pt_BR" else 1,
        key="lang_select"
    )
    st.session_state.lang = selected_lang

    st.markdown("---")
    st.markdown(
        "**EditorGIF v1.0**\n\n"
        "Desenvolvido para criadores de jogos indie e animadores."
        if selected_lang == "pt_BR" else
        "**EditorGIF v1.0**\n\n"
        "Built for indie game developers and animators."
    )


def t(key: str, **kwargs) -> str:
    return get_text(key, lang=st.session_state.lang, **kwargs)


# Header Section
st.markdown(f"""
<div class="hero-container">
    <div>
        <div class="hero-badge">
            <span class="hero-badge-dot"></span>
            <span>AI SPRITE ENGINE v1.1</span>
        </div>
        <div class="hero-title">{t('hero_title')}</div>
        <div class="hero-subtitle">{t('hero_subtitle')}</div>
    </div>
    <div class="hero-badges-wrapper">
        <span class="badge-tech"><span class="badge-dot dot-cyan"></span>{t('badge_onnx')}</span>
        <span class="badge-tech"><span class="badge-dot dot-purple"></span>{t('badge_ghost')}</span>
        <span class="badge-tech"><span class="badge-dot dot-emerald"></span>{t('badge_defringe')}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main container
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(t("step_1_title"))
    
    input_mode = st.radio(
        t("input_mode_label"),
        options=["video", "sheet"],
        format_func=lambda x: t("input_mode_video") if x == "video" else t("input_mode_sheet"),
        horizontal=True,
        key="input_media_mode"
    )

    if input_mode == "video":
        uploaded_file = st.file_uploader(
            t("upload_label"),
            type=["mp4", "webm", "mov", "avi", "gif"],
            help=t("upload_help"),
            key="file_uploader_video"
        )

        if uploaded_file:
            # Reset output if new file uploaded
            if st.session_state.last_processed_file != uploaded_file.name:
                st.session_state.gif_bytes = None
                st.session_state.sheet_bytes = None
                st.session_state.sheet_meta = None
                st.session_state.rgba_frames = None
                st.session_state.pop("cached_trim_key", None)
                st.session_state.pop("cached_trimmed_gif", None)
                st.session_state.pop("cached_trimmed_sheet", None)
                st.session_state.last_processed_file = uploaded_file.name

            # Save to temp file for OpenCV/PIL reading
            tfile = tempfile.NamedTemporaryFile(delete=False, suffix=f"_{uploaded_file.name}")
            tfile.write(uploaded_file.read())
            tfile.flush()
            temp_path = tfile.name

            try:
                meta = get_video_metadata(temp_path)
                
                # Show original video or animated GIF player
                if uploaded_file.name.lower().endswith(".gif"):
                    st.image(temp_path)
                else:
                    st.video(temp_path)

                st.caption(
                    t("video_caption", width=meta.width, height=meta.height, duration=meta.duration_seconds, fps=meta.fps)
                )

                st.divider()
                st.subheader(t("step_2_title"))

                # Time Interval Trimming
                max_dur = max(0.1, float(meta.duration_seconds))
                default_end = min(max_dur, 3.0)
                time_range = st.slider(
                    t("time_slider_label"),
                    min_value=0.0,
                    max_value=max_dur,
                    value=(0.0, default_end),
                    step=0.05,
                    help=t("time_slider_help")
                )

                # Target Game FPS
                target_fps = st.select_slider(
                    t("target_fps_label"),
                    options=[6, 8, 10, 12, 15, 20, 24, 30],
                    value=12,
                    help=t("target_fps_help")
                )

                # Resolution Scale
                scale_percent = st.slider(
                    t("scale_slider_label"),
                    min_value=20,
                    max_value=100,
                    value=50,
                    step=5,
                    help=t("scale_slider_help")
                )

                # Advanced Settings Accordion
                with st.expander(t("advanced_title"), expanded=False):
                    model_name = st.selectbox(
                        t("model_label"),
                        options=["u2net", "isnet-general-use", "silueta", "birefnet-general"],
                        index=0,
                        help=t("model_help")
                    )
                    alpha_threshold = st.slider(
                        t("alpha_threshold_label"),
                        min_value=1,
                        max_value=250,
                        value=30,
                        help=t("alpha_threshold_help")
                    )
                    defringe = st.checkbox(
                        t("defringe_label"),
                        value=True,
                        help=t("defringe_help")
                    )
                    auto_crop = st.checkbox(
                        t("autocrop_label"),
                        value=False,
                        help=t("autocrop_help")
                    )

                st.markdown("<br>", unsafe_allow_html=True)
                process_btn = st.button(t("process_button"), use_container_width=True)

                if process_btn:
                    prog_bar = st.progress(0, text=t("prog_extract"))
                    
                    try:
                        # 1. Extraction
                        frames = extract_frames(
                            video_path=temp_path,
                            start_time=time_range[0],
                            end_time=time_range[1],
                            target_fps=target_fps,
                            scale_percent=scale_percent
                        )
                        
                        prog_bar.progress(20, text=t("prog_extracted", count=len(frames), model=model_name))
                        session = get_rembg_session(model_name)

                        # 2. AI Background Removal
                        def update_progress(current, total, msg):
                            percent = 20 + int((current / total) * 60)
                            prog_bar.progress(percent, text=t("prog_segment", current=current, total=total))

                        rgba_frames = process_frames_pipeline(
                            frames=frames,
                            session=session,
                            alpha_threshold=alpha_threshold,
                            defringe=defringe,
                            auto_crop=auto_crop,
                            progress_callback=update_progress
                        )

                        # 3. Compile GIF
                        prog_bar.progress(85, text=t("prog_gif"))
                        gif_bytes = compile_transparent_gif(rgba_frames, fps=target_fps)

                        # 4. Compile Sprite Sheet
                        prog_bar.progress(95, text=t("prog_sheet"))
                        sheet_bytes, sheet_meta = compile_sprite_sheet(rgba_frames, layout="horizontal")

                        prog_bar.progress(100, text=t("prog_done"))

                        # Store in session state
                        st.session_state.gif_bytes = gif_bytes
                        st.session_state.sheet_bytes = sheet_bytes
                        st.session_state.sheet_meta = sheet_meta
                        st.session_state.frames_count = len(rgba_frames)
                        st.session_state.dimensions = rgba_frames[0].size
                        st.session_state.rgba_frames = rgba_frames
                        st.session_state.fps = target_fps
                        st.session_state.pop("cached_trim_key", None)
                        st.session_state.pop("cached_trimmed_gif", None)
                        st.session_state.pop("cached_trimmed_sheet", None)
                        st.toast(t("toast_success"), icon="✅")

                    except Exception as e:
                        st.error(t("error_processing", error=str(e)))
                    finally:
                        try:
                            os.remove(temp_path)
                        except Exception:
                            pass

            except Exception as e:
                st.error(t("error_reading", error=str(e)))

    else:
        # Sprite Sheet Input Mode
        uploaded_sheet = st.file_uploader(
            t("upload_sheet_label"),
            type=["png", "webp", "jpg", "jpeg"],
            help=t("upload_sheet_help"),
            key="file_uploader_sheet"
        )

        if uploaded_sheet:
            if st.session_state.last_processed_file != uploaded_sheet.name:
                st.session_state.gif_bytes = None
                st.session_state.sheet_bytes = None
                st.session_state.sheet_meta = None
                st.session_state.rgba_frames = None
                st.session_state.pop("cached_trim_key", None)
                st.session_state.pop("cached_trimmed_gif", None)
                st.session_state.pop("cached_trimmed_sheet", None)
                st.session_state.last_processed_file = uploaded_sheet.name

            try:
                sheet_pil = Image.open(uploaded_sheet)
                sheet_w, sheet_h = sheet_pil.size
                has_alpha = "Sim / Yes (RGBA)" if sheet_pil.mode == "RGBA" else "Não / No (RGB)"

                # Preview the loaded sprite sheet
                st.image(sheet_pil, caption=t("sheet_caption", width=sheet_w, height=sheet_h, alpha=has_alpha), use_container_width=True)

                st.divider()
                st.subheader(t("step_2_title"))

                sheet_layout = st.radio(
                    t("sheet_layout_label"),
                    options=["horizontal", "grid"],
                    format_func=lambda x: t("sheet_layout_horizontal") if x == "horizontal" else t("sheet_layout_grid"),
                    horizontal=True
                )

                if sheet_layout == "horizontal":
                    cols = st.number_input(t("sheet_frames_count_label"), min_value=1, max_value=128, value=max(1, sheet_w // sheet_h if sheet_h > 0 else 4), step=1)
                    rows = 1
                else:
                    col_c1, col_c2 = st.columns(2)
                    with col_c1:
                        cols = st.number_input(t("sheet_cols_label"), min_value=1, max_value=64, value=4, step=1)
                    with col_c2:
                        rows = st.number_input(t("sheet_rows_label"), min_value=1, max_value=64, value=1, step=1)

                calc_frame_w = sheet_w // cols
                calc_frame_h = sheet_h // rows
                total_quadros = cols * rows

                st.caption(t("sheet_frame_calc", w=calc_frame_w, h=calc_frame_h, count=total_quadros))

                # Playback FPS
                sheet_fps = st.select_slider(
                    t("target_fps_label"),
                    options=[6, 8, 10, 12, 15, 20, 24, 30],
                    value=12,
                    help=t("target_fps_help")
                )

                # Optional AI Background Removal for Sprite Sheet
                apply_ai = st.checkbox(
                    t("sheet_ai_bg_label"),
                    value=(sheet_pil.mode != "RGBA"),
                    help=t("sheet_ai_bg_help")
                )

                if apply_ai:
                    with st.expander(t("advanced_title"), expanded=False):
                        model_name = st.selectbox(
                            t("model_label"),
                            options=["u2net", "isnet-general-use", "silueta", "birefnet-general"],
                            index=0,
                            help=t("model_help")
                        )
                        alpha_threshold = st.slider(
                            t("alpha_threshold_label"),
                            min_value=1,
                            max_value=250,
                            value=30,
                            help=t("alpha_threshold_help")
                        )
                        defringe = st.checkbox(
                            t("defringe_label"),
                            value=True,
                            help=t("defringe_help")
                        )
                        auto_crop = st.checkbox(
                            t("autocrop_label"),
                            value=False,
                            help=t("autocrop_help")
                        )

                st.markdown("<br>", unsafe_allow_html=True)
                process_sheet_btn = st.button(t("process_sheet_button"), use_container_width=True)

                if process_sheet_btn:
                    prog_bar = st.progress(0, text=t("prog_extract"))
                    try:
                        # 1. Slice Sprite Sheet
                        sliced_raw = slice_sprite_sheet(sheet_pil, columns=cols, rows=rows)
                        prog_bar.progress(30, text=f"Fatiados {len(sliced_raw)} quadros...")

                        if apply_ai:
                            session = get_rembg_session(model_name)
                            def update_progress(current, total, msg):
                                percent = 30 + int((current / total) * 50)
                                prog_bar.progress(percent, text=t("prog_segment", current=current, total=total))

                            rgba_frames = process_frames_pipeline(
                                frames=[f.convert("RGB") for f in sliced_raw],
                                session=session,
                                alpha_threshold=alpha_threshold,
                                defringe=defringe,
                                auto_crop=auto_crop,
                                progress_callback=update_progress
                            )
                        else:
                            rgba_frames = [f.convert("RGBA") for f in sliced_raw]

                        prog_bar.progress(85, text=t("prog_gif"))
                        gif_bytes = compile_transparent_gif(rgba_frames, fps=sheet_fps)

                        prog_bar.progress(95, text=t("prog_sheet"))
                        sheet_bytes, sheet_meta = compile_sprite_sheet(rgba_frames, layout="horizontal")

                        prog_bar.progress(100, text=t("prog_done"))

                        # Store in session state
                        st.session_state.gif_bytes = gif_bytes
                        st.session_state.sheet_bytes = sheet_bytes
                        st.session_state.sheet_meta = sheet_meta
                        st.session_state.frames_count = len(rgba_frames)
                        st.session_state.dimensions = rgba_frames[0].size
                        st.session_state.rgba_frames = rgba_frames
                        st.session_state.fps = sheet_fps
                        st.session_state.pop("cached_trim_key", None)
                        st.session_state.pop("cached_trimmed_gif", None)
                        st.session_state.pop("cached_trimmed_sheet", None)
                        st.toast(t("toast_success"), icon="✅")

                    except Exception as e:
                        st.error(t("error_processing", error=str(e)))

            except Exception as e:
                st.error(t("error_reading", error=str(e)))

    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(t("step_3_title"))

    if st.session_state.gif_bytes is not None and st.session_state.rgba_frames is not None:
        dim_w, dim_h = st.session_state.dimensions
        frames_count = st.session_state.frames_count
        gif_size_kb = len(st.session_state.gif_bytes) / 1024.0
        fps = st.session_state.fps
        total_duration = max(0.01, frames_count / float(fps))

        st.markdown(f"""
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-label">{t('meta_res')}</div>
                <div class="stat-value">{dim_w} × {dim_h} px</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">{t('meta_frames')}</div>
                <div class="stat-value">{frames_count} {t('meta_frames_unit')}</div>
            </div>
            <div class="stat-card">
                <div class="stat-label">{t('meta_duration')}</div>
                <div class="stat-value">{total_duration:.2f}s <span class="stat-sub">@{fps}fps</span></div>
            </div>
            <div class="stat-card">
                <div class="stat-label">{t('meta_size')}</div>
                <div class="stat-value">{gif_size_kb:.1f} KB</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown(f"#### {t('trim_section_title')}")
        st.caption(t("trim_section_help"))

        step_val = max(0.01, round(1.0 / fps, 3))
        max_time_val = float(round(total_duration, 2))
        trim_range = st.slider(
            t("trim_slider_label"),
            min_value=0.0,
            max_value=max_time_val,
            value=(0.0, max_time_val),
            step=step_val,
            help=t("trim_section_help")
        )

        speed_multiplier = st.select_slider(
            t("speed_slider_label"),
            options=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75, 2.0, 2.5, 3.0],
            value=1.0,
            format_func=lambda s: f"{s:.2f}x" if s != int(s) else f"{int(s)}.0x" if s == 1.0 or s == 2.0 or s == 3.0 else f"{s}x",
            help=t("speed_slider_help")
        )

        sliced_frames, start_idx, end_idx = slice_frames_by_seconds(
            st.session_state.rgba_frames,
            fps=fps,
            start_sec=trim_range[0],
            end_sec=trim_range[1]
        )

        effective_fps = max(1.0, fps * speed_multiplier)
        sliced_duration = len(sliced_frames) / float(effective_fps)
        st.info(t("trim_stats", start=trim_range[0], end=trim_range[1], duration=sliced_duration, frames=len(sliced_frames), speed=speed_multiplier))

        is_full_range = (len(sliced_frames) == len(st.session_state.rgba_frames)) and (start_idx == 0)

        # Sprite sheet depends only on sliced frames (speed does not alter static sprite sheet images)
        if is_full_range:
            active_sheet_bytes = st.session_state.sheet_bytes
        else:
            sheet_cache_key = f"sheet_{start_idx}_{end_idx}_{len(sliced_frames)}"
            if st.session_state.get("cached_sheet_key") != sheet_cache_key:
                trimmed_sheet, _ = compile_sprite_sheet(sliced_frames, layout="horizontal")
                st.session_state["cached_sheet_key"] = sheet_cache_key
                st.session_state["cached_trimmed_sheet"] = trimmed_sheet
            active_sheet_bytes = st.session_state["cached_trimmed_sheet"]

        # GIF depends on sliced frames AND speed_multiplier
        gif_cache_key = f"gif_{start_idx}_{end_idx}_{len(sliced_frames)}_{speed_multiplier}_{fps}"
        if is_full_range and speed_multiplier == 1.0:
            active_gif_bytes = st.session_state.gif_bytes
        else:
            if st.session_state.get("cached_trim_key") != gif_cache_key:
                trimmed_gif = compile_transparent_gif(sliced_frames, fps=fps, speed_multiplier=speed_multiplier)
                st.session_state["cached_trim_key"] = gif_cache_key
                st.session_state["cached_trimmed_gif"] = trimmed_gif
            active_gif_bytes = st.session_state["cached_trimmed_gif"]

        # Also compile full gif if speed_multiplier changed and someone looks at tab_orig
        full_gif_cache_key = f"full_gif_{len(st.session_state.rgba_frames)}_{speed_multiplier}_{fps}"
        if speed_multiplier == 1.0:
            active_full_gif_bytes = st.session_state.gif_bytes
        else:
            if st.session_state.get("cached_full_gif_key") != full_gif_cache_key:
                full_speed_gif = compile_transparent_gif(st.session_state.rgba_frames, fps=fps, speed_multiplier=speed_multiplier)
                st.session_state["cached_full_gif_key"] = full_gif_cache_key
                st.session_state["cached_full_speed_gif"] = full_speed_gif
            active_full_gif_bytes = st.session_state["cached_full_speed_gif"]

        tab_trim, tab_orig = st.tabs([t("tab_trimmed"), t("tab_full")])

        with tab_trim:
            st.markdown(f"<b>{t('trim_preview_title')}</b>", unsafe_allow_html=True)
            b64_active_gif = base64.b64encode(active_gif_bytes).decode("utf-8")
            st.markdown(f"""
            <div class="checkerboard-viewport">
                <div class="viewport-header">
                    <span class="viewport-dots"><span class="v-dot v-red"></span><span class="v-dot v-yellow"></span><span class="v-dot v-green"></span></span>
                    <span class="viewport-title">CHECKERBOARD VIEWPORT • RECORTE ATIVO</span>
                    <span class="viewport-status">TRIMMED</span>
                </div>
                <div class="checkerboard-box">
                    <img src="data:image/gif;base64,{b64_active_gif}" style="max-width: 100%; max-height: 320px; object-fit: contain; image-rendering: auto;" alt="Trimmed Transparent Preview" />
                </div>
            </div>
            """, unsafe_allow_html=True)

            speed_tag = f"_{speed_multiplier:.2f}x" if speed_multiplier != 1.0 else ""
            if is_full_range:
                st.download_button(
                    label=t("btn_download_gif"),
                    data=active_gif_bytes,
                    file_name=f"sprite_animacao_transparente{speed_tag}.gif",
                    mime="image/gif",
                    use_container_width=True
                )
                if active_sheet_bytes is not None:
                    st.download_button(
                        label=t("btn_download_sheet"),
                        data=active_sheet_bytes,
                        file_name="sprite_sheet_transparente.png",
                        mime="image/png",
                        use_container_width=True
                    )
            else:
                st.download_button(
                    label=t("btn_download_trimmed_gif", start=trim_range[0], end=trim_range[1]),
                    data=active_gif_bytes,
                    file_name=f"sprite_recortado_{trim_range[0]:.2f}s_a_{trim_range[1]:.2f}s{speed_tag}.gif",
                    mime="image/gif",
                    use_container_width=True
                )
                if active_sheet_bytes is not None:
                    st.download_button(
                        label=t("btn_download_trimmed_sheet", frames=len(sliced_frames)),
                        data=active_sheet_bytes,
                        file_name=f"sprite_sheet_recortado_{len(sliced_frames)}quadros.png",
                        mime="image/png",
                        use_container_width=True
                    )

        with tab_orig:
            st.markdown(f"<b>{t('preview_title')}</b>", unsafe_allow_html=True)
            b64_full_gif = base64.b64encode(active_full_gif_bytes).decode("utf-8")
            st.markdown(f"""
            <div class="checkerboard-viewport">
                <div class="viewport-header">
                    <span class="viewport-dots"><span class="v-dot v-red"></span><span class="v-dot v-yellow"></span><span class="v-dot v-green"></span></span>
                    <span class="viewport-title">CHECKERBOARD VIEWPORT • ANIMAÇÃO COMPLETA</span>
                    <span class="viewport-status">ORIGINAL</span>
                </div>
                <div class="checkerboard-box">
                    <img src="data:image/gif;base64,{b64_full_gif}" style="max-width: 100%; max-height: 320px; object-fit: contain; image-rendering: auto;" alt="Full Transparent Preview" />
                </div>
            </div>
            """, unsafe_allow_html=True)

            orig_duration = len(st.session_state.rgba_frames) / float(effective_fps)
            st.download_button(
                label=t("btn_download_full_gif", duration=orig_duration),
                data=active_full_gif_bytes,
                file_name=f"sprite_animacao_completa{speed_tag}.gif",
                mime="image/gif",
                use_container_width=True
            )
            if st.session_state.sheet_bytes is not None:
                st.download_button(
                    label=t("btn_download_full_sheet"),
                    data=st.session_state.sheet_bytes,
                    file_name="sprite_sheet_completa.png",
                    mime="image/png",
                    use_container_width=True
                )

        with st.expander(t("guide_title")):
            st.markdown(t("guide_content"))

    else:
        st.markdown(f"""
        <div class="checkerboard-viewport">
            <div class="viewport-header">
                <span class="viewport-dots"><span class="v-dot v-red"></span><span class="v-dot v-yellow"></span><span class="v-dot v-green"></span></span>
                <span class="viewport-title">CHECKERBOARD VIEWPORT</span>
                <span class="viewport-status">WAITING</span>
            </div>
            <div class="checkerboard-box empty-box">
                <div class="empty-icon">👾</div>
                <div class="empty-text">{t('empty_preview')}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
