# 🗂️ Tab Manager Pro

A powerful browser extension for managing your tabs efficiently. Built with Manifest V3 for Chrome, Edge, and other Chromium-based browsers.

## ✨ Features

- 🔍 **Smart Search** - Quickly find tabs by title or URL
- 📊 **Tab Statistics** - See total tab count at a glance
- 🗑️ **Close Duplicates** - Remove duplicate tabs with one click
- ➡️ **Close Tabs to Right** - Clean up tabs to the right of current tab
- 📁 **Group by Domain** - Automatically organize tabs by website domain
- ⌨️ **Keyboard Shortcut** - Quick access with `Ctrl+Shift+T` (or `Cmd+Shift+T` on Mac)
- 🎨 **Beautiful UI** - Modern gradient design with smooth animations
- 🚀 **Performance** - Lightweight and fast

## 📦 Installation

### Development Mode

1. **Download the extension:**
   ```bash
   git clone <repository-url>
   cd extensions/tab-manager-pro
   ```

2. **Load in Chrome/Edge:**
   - Open Chrome/Edge and go to `chrome://extensions/` (or `edge://extensions/`)
   - Enable "Developer mode" (toggle in top-right corner)
   - Click "Load unpacked"
   - Select the `tab-manager-pro` folder
   - The extension icon should appear in your toolbar

3. **Pin the extension:**
   - Click the puzzle piece icon in the toolbar
   - Find "Tab Manager Pro" and click the pin icon

## 🎯 Usage

### Opening the Extension
- Click the extension icon in your toolbar
- Or use keyboard shortcut: `Ctrl+Shift+T` (`Cmd+Shift+T` on Mac)

### Managing Tabs
1. **Search**: Type in the search box to filter tabs by title or URL
2. **Navigate**: Click any tab to switch to it
3. **Close**: Click the × button to close individual tabs
4. **Close Duplicates**: Remove all duplicate tabs instantly
5. **Close to Right**: Close all tabs to the right of the active tab
6. **Group by Domain**: Organize tabs into groups by website

### Badge Indicator
The extension badge shows the number of open tabs (displays "9+" for 10 or more tabs).

## 🛠️ Technical Details

- **Manifest Version**: 3 (latest)
- **Permissions**: 
  - `tabs` - Manage browser tabs
  - `tabGroups` - Create and manage tab groups
  - `storage` - Store user preferences
  - `sessions` - Access session data
- **Background**: Service Worker (efficient, event-driven)
- **UI**: HTML5, CSS3, Vanilla JavaScript

## 📁 Project Structure

```
tab-manager-pro/
├── manifest.json          # Extension configuration
├── src/
│   ├── popup.html         # Main popup interface
│   ├── popup.js           # Popup logic
│   ├── styles.css         # Styling
│   └── background.js      # Service worker
└── icons/
    ├── icon16.svg         # 16x16 icon
    ├── icon48.svg         # 48x48 icon
    └── icon128.svg        # 128x128 icon
```

## 🚀 Publishing to Chrome Web Store

1. **Prepare for publishing:**
   - Convert SVG icons to PNG format
   - Create screenshots (1280x800 or 640x400)
   - Write a compelling description
   - Set up developer account ($5 one-time fee)

2. **Package the extension:**
   - Go to `chrome://extensions/`
   - Click "Pack extension"
   - Select the `tab-manager-pro` folder
   - Download the `.crx` and `.pem` files

3. **Submit to Chrome Web Store:**
   - Visit [Chrome Web Store Developer Dashboard](https://chrome.google.com/webstore/devconsole)
   - Create a new item
   - Upload the `.zip` file (not .crx)
   - Fill in store listing details
   - Submit for review

## 🔒 Privacy & Security

- No data collection
- All operations performed locally
- No external servers or analytics
- Open source - code is transparent

## 🤝 Contributing

Contributions are welcome! Please see our main repository's [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see main repository [LICENSE](../../LICENSE)

## 🙏 Acknowledgments

Built with ❤️ using modern web technologies.

---

**Enjoy managing your tabs like a pro!** 🎉
