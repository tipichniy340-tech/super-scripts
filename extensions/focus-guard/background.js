// Focus Guard - Background Service Worker

// Initialize default settings on install
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.set({
    blockList: ['facebook.com', 'twitter.com', 'instagram.com', 'youtube.com', 'tiktok.com'],
    isBlockingEnabled: false,
    stats: { focusTime: 0, sessions: 0, blocked: 0 }
  });
});

// Block websites when blocking is enabled
chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  // Only process main frame navigations
  if (details.frameId !== 0) return;

  chrome.storage.sync.get(['blockList', 'isBlockingEnabled'], (result) => {
    const { blockList = [], isBlockingEnabled = false } = result;
    
    if (!isBlockingEnabled) return;

    const url = new URL(details.url);
    const hostname = url.hostname.replace('www.', '');

    if (blockList.some(site => hostname === site || hostname.endsWith('.' + site))) {
      // Block the site
      chrome.tabs.update(details.tabId, { url: chrome.runtime.getURL('blocked.html') });
      
      // Update blocked count in stats
      chrome.storage.sync.get(['stats'], (statResult) => {
        const stats = statResult.stats || { focusTime: 0, sessions: 0, blocked: 0 };
        stats.blocked += 1;
        chrome.storage.sync.set({ stats });
        
        // Notify popup
        chrome.runtime.sendMessage({ type: 'SITE_BLOCKED' });
      });
    }
  });
}, { url: [{ schemes: ['http', 'https'] }] });

// Handle keyboard shortcuts
chrome.commands.onCommand.addListener((command) => {
  if (command === 'toggle-blocking') {
    chrome.storage.sync.get(['isBlockingEnabled'], (result) => {
      const newState = !result.isBlockingEnabled;
      chrome.storage.sync.set({ isBlockingEnabled: newState });
      
      // Show notification
      chrome.notifications.create({
        type: 'basic',
        iconUrl: 'icons/icon128.png',
        title: 'Focus Guard',
        message: newState ? 'Блокировка включена' : 'Блокировка выключена'
      });
    });
  } else if (command === 'start-pomodoro') {
    chrome.tabs.create({ url: chrome.runtime.getURL('popup.html') });
  }
});

// Alarm for timer notifications (alternative to popup timer)
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'pomodoro-complete') {
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon128.png',
      title: 'Focus Guard',
      message: 'Помодоро сессия завершена! Сделайте перерыв.'
    });
  } else if (alarm.name === 'break-complete') {
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon128.png',
      title: 'Focus Guard',
      message: 'Перерыв окончен! Пора вернуться к работе.'
    });
  }
});

// Context menu for quick adding sites to blocklist
chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'add-to-blocklist',
    title: 'Добавить сайт в чёрный список',
    contexts: ['page']
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'add-to-blocklist') {
    try {
      const url = new URL(info.pageUrl);
      const hostname = url.hostname.replace('www.', '');
      
      chrome.storage.sync.get(['blockList'], (result) => {
        const sites = result.blockList || [];
        if (!sites.includes(hostname)) {
          sites.push(hostname);
          chrome.storage.sync.set({ blockList: sites });
          
          chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icons/icon128.png',
            title: 'Focus Guard',
            message: `Сайт ${hostname} добавлен в чёрный список`
          });
        } else {
          chrome.notifications.create({
            type: 'basic',
            iconUrl: 'icons/icon128.png',
            title: 'Focus Guard',
            message: `Сайт ${hostname} уже в чёрном списке`
          });
        }
      });
    } catch (e) {
      console.error('Invalid URL:', e);
    }
  }
});
