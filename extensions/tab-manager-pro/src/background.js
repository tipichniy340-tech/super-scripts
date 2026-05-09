// Tab Manager Pro - Background Service Worker

// Listen for extension installation
chrome.runtime.onInstalled.addListener((details) => {
  if (details.reason === 'install') {
    console.log('Tab Manager Pro installed successfully!');
    // Initialize storage with default values
    chrome.storage.local.set({
      settings: {
        theme: 'default',
        showFavIcons: true,
        maxTabsDisplay: 100
      }
    });
  }
});

// Keep track of tab count for badge
async function updateBadge() {
  try {
    const tabs = await chrome.tabs.query({});
    const count = tabs.length;
    
    if (count > 9) {
      chrome.action.setBadgeText({ text: '9+' });
    } else if (count > 0) {
      chrome.action.setBadgeText({ text: count.toString() });
    } else {
      chrome.action.setBadgeText({ text: '' });
    }
    
    chrome.action.setBadgeBackgroundColor({ color: '#667eea' });
  } catch (error) {
    console.error('Error updating badge:', error);
  }
}

// Listen for tab changes
chrome.tabs.onCreated.addListener(updateBadge);
chrome.tabs.onRemoved.addListener(updateBadge);
chrome.tabs.onActivated.addListener(updateBadge);

// Initialize badge on startup
updateBadge();

// Handle keyboard shortcuts
chrome.commands.onCommand.addListener(async (command) => {
  if (command === '_execute_action') {
    // Open popup programmatically if needed
    console.log('Tab Manager Pro shortcut activated');
  }
});
