@echo off
REM Script para generar documentación HTML con Sphinx
REM Ejecutar desde la carpeta 'docs'

python -m sphinx source build/html

echo.
echo Documentación generada en: build/html/index.html
pause
