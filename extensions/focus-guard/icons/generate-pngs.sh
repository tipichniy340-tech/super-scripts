#!/bin/bash
# Скрипт для генерации PNG из SVG (требует установленного imagemagick или inkscape)

# Если установлен convert (ImageMagick)
if command -v convert &> /dev/null; then
    convert -background none icons/icon16.svg icons/icon16.png
    convert -background none icons/icon48.svg icons/icon48.png
    convert -background none icons/icon128.svg icons/icon128.png
    echo "PNG иконки созданы с помощью ImageMagick"
elif command -v inkscape &> /dev/null; then
    inkscape --export-filename=icons/icon16.png --export-width=16 --export-height=16 icons/icon16.svg
    inkscape --export-filename=icons/icon48.png --export-width=48 --export-height=48 icons/icon48.svg
    inkscape --export-filename=icons/icon128.png --export-width=128 --export-height=128 icons/icon128.svg
    echo "PNG иконки созданы с помощью Inkscape"
else
    echo "Установите ImageMagick или Inkscape для конвертации SVG в PNG"
    echo "Или используйте онлайн-конвертер"
fi
