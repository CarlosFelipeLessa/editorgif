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

from core.video_processor import extract_frames, get_video_metadata
from core.bg_remover import get_rembg_session, process_frames_pipeline
from core.gif_compiler import compile_transparent_gif, compile_sprite_sheet, slice_frames_by_seconds
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
<div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap;">
    <div>
        <div class="hero-title">{t('hero_title')}</div>
        <div class="hero-subtitle">{t('hero_subtitle')}</div>
    </div>
    <div style="margin-bottom: 1rem;">
        <span class="badge-tech">{t('badge_onnx')}</span>
        <span class="badge-tech">{t('badge_ghost')}</span>
        <span class="badge-tech">{t('badge_defringe')}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Main container
col_left, col_right = st.columns([1, 1], gap="large")

with col_left:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader(t("step_1_title"))
    
    uploaded_file = st.file_uploader(
        t("upload_label"),
        type=["mp4", "webm", "mov", "avi", "gif"],
        help=t("upload_help")
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
        <div style="display: flex; gap: 12px; margin-bottom: 12px; flex-wrap: wrap;">
            <div style="background: rgba(255,255,255,0.05); padding: 8px 14px; border-radius: 8px;">
                <span style="color:#94a3b8; font-size: 0.8rem;">{t('meta_res')}</span><br>
                <b>{dim_w} x {dim_h} px</b>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 8px 14px; border-radius: 8px;">
                <span style="color:#94a3b8; font-size: 0.8rem;">{t('meta_frames')}</span><br>
                <b>{frames_count} {t('meta_frames_unit')}</b>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 8px 14px; border-radius: 8px;">
                <span style="color:#94a3b8; font-size: 0.8rem;">{t('meta_duration')}</span><br>
                <b>{total_duration:.2f} s (@ {fps} FPS)</b>
            </div>
            <div style="background: rgba(255,255,255,0.05); padding: 8px 14px; border-radius: 8px;">
                <span style="color:#94a3b8; font-size: 0.8rem;">{t('meta_size')}</span><br>
                <b>{gif_size_kb:.1f} KB</b>
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

        sliced_frames, start_idx, end_idx = slice_frames_by_seconds(
            st.session_state.rgba_frames,
            fps=fps,
            start_sec=trim_range[0],
            end_sec=trim_range[1]
        )

        sliced_duration = len(sliced_frames) / float(fps)
        st.info(t("trim_stats", start=trim_range[0], end=trim_range[1], duration=sliced_duration, frames=len(sliced_frames)))

        is_full_range = (len(sliced_frames) == len(st.session_state.rgba_frames)) and (start_idx == 0)

        if is_full_range:
            active_gif_bytes = st.session_state.gif_bytes
            active_sheet_bytes = st.session_state.sheet_bytes
        else:
            cache_key = f"trim_{start_idx}_{end_idx}_{len(sliced_frames)}"
            if st.session_state.get("cached_trim_key") != cache_key:
                trimmed_gif = compile_transparent_gif(sliced_frames, fps=fps)
                trimmed_sheet, _ = compile_sprite_sheet(sliced_frames, layout="horizontal")
                st.session_state["cached_trim_key"] = cache_key
                st.session_state["cached_trimmed_gif"] = trimmed_gif
                st.session_state["cached_trimmed_sheet"] = trimmed_sheet

            active_gif_bytes = st.session_state["cached_trimmed_gif"]
            active_sheet_bytes = st.session_state["cached_trimmed_sheet"]

        tab_trim, tab_orig = st.tabs([t("tab_trimmed"), t("tab_full")])

        with tab_trim:
            st.markdown(f"<b>{t('trim_preview_title')}</b>", unsafe_allow_html=True)
            b64_active_gif = base64.b64encode(active_gif_bytes).decode("utf-8")
            st.markdown(f"""
            <div class="checkerboard-box">
                <img src="data:image/gif;base64,{b64_active_gif}" style="max-width: 100%; max-height: 320px; object-fit: contain; image-rendering: auto;" alt="Trimmed Transparent Preview" />
            </div>
            """, unsafe_allow_html=True)

            if is_full_range:
                st.download_button(
                    label=t("btn_download_gif"),
                    data=active_gif_bytes,
                    file_name="sprite_animacao_transparente.gif",
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
                    file_name=f"sprite_recortado_{trim_range[0]:.2f}s_a_{trim_range[1]:.2f}s.gif",
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
            b64_full_gif = base64.b64encode(st.session_state.gif_bytes).decode("utf-8")
            st.markdown(f"""
            <div class="checkerboard-box">
                <img src="data:image/gif;base64,{b64_full_gif}" style="max-width: 100%; max-height: 320px; object-fit: contain; image-rendering: auto;" alt="Full Transparent Preview" />
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label=t("btn_download_full_gif", duration=total_duration),
                data=st.session_state.gif_bytes,
                file_name="sprite_animacao_completa.gif",
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
        <div class="checkerboard-box" style="color: #64748b; text-align: center;">
            <div style="font-size: 2.5rem; margin-bottom: 8px;">🕹️</div>
            <div>{t('empty_preview')}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
