@echo off
chcp 65001 > nul
title EditorGIF
echo ============================================================
echo      Iniciando EditorGIF (Video para GIF Transparente)
echo ============================================================
echo.
echo Abrindo a aplicacao no seu navegador...
python -m streamlit run ui/app.py
pause
