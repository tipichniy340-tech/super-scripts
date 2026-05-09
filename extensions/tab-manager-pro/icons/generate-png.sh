#!/bin/bash
# Script to convert SVG icons to PNG for Chrome Web Store submission

# Check if imagemagick is installed
if ! command -v convert &> /dev/null; then
    echo "ImageMagick is required. Install with: sudo apt-get install imagemagick"
    exit 1
fi

# Convert SVG to PNG
convert -background none icons/icon16.svg icons/icon16.png
convert -background none icons/icon48.svg icons/icon48.png
convert -background none icons/icon128.svg icons/icon128.png

echo "PNG icons generated successfully!"
ls -la icons/*.png
