// Tab Manager Pro - Popup Script

let allTabs = [];
let filteredTabs = [];

// Initialize popup
document.addEventListener('DOMContentLoaded', async () => {
  await loadTabs();
  setupEventListeners();
});

// Load all tabs
async function loadTabs() {
  try {
    allTabs = await chrome.tabs.query({});
    filteredTabs = [...allTabs];
    renderTabs(filteredTabs);
    updateStats();
  } catch (error) {
    console.error('Error loading tabs:', error);
  }
}

// Render tabs list
function renderTabs(tabs) {
  const tabsList = document.getElementById('tabsList');
  
  if (tabs.length === 0) {
    tabsList.innerHTML = `
      <div class="empty-state">
        <div class="empty-state-icon">📑</div>
        <p>No tabs found</p>
      </div>
    `;
    return;
  }

  tabsList.innerHTML = tabs.map(tab => `
    <div class="tab-item ${tab.active ? 'active' : ''}" data-tab-id="${tab.id}">
      <img class="tab-icon" src="${tab.favIconUrl || 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22>🌐</text></svg>'}" alt="">
      <div class="tab-info">
        <div class="tab-title">${escapeHtml(tab.title)}</div>
        <div class="tab-url">${escapeHtml(tab.url)}</div>
      </div>
      <div class="tab-actions">
        <button class="tab-close" data-tab-id="${tab.id}" title="Close tab">×</button>
      </div>
    </div>
  `).join('');

  // Add click listeners
  document.querySelectorAll('.tab-item').forEach(item => {
    item.addEventListener('click', async (e) => {
      if (!e.target.classList.contains('tab-close')) {
        const tabId = parseInt(item.dataset.tabId);
        await chrome.tabs.update(tabId, { active: true });
        window.close();
      }
    });
  });

  document.querySelectorAll('.tab-close').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      e.stopPropagation();
      const tabId = parseInt(btn.dataset.tabId);
      await chrome.tabs.remove(tabId);
      await loadTabs();
    });
  });
}

// Update tab count stats
function updateStats() {
  const tabCount = document.getElementById('tabCount');
  tabCount.textContent = `${allTabs.length} tab${allTabs.length !== 1 ? 's' : ''}`;
}

// Setup event listeners
function setupEventListeners() {
  // Search functionality
  const searchInput = document.getElementById('searchInput');
  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    if (query === '') {
      filteredTabs = [...allTabs];
    } else {
      filteredTabs = allTabs.filter(tab => 
        tab.title.toLowerCase().includes(query) || 
        tab.url.toLowerCase().includes(query)
      );
    }
    renderTabs(filteredTabs);
  });

  // Close duplicates button
  document.getElementById('closeDuplicates').addEventListener('click', async () => {
    const seenUrls = new Set();
    const duplicates = allTabs.filter(tab => {
      if (seenUrls.has(tab.url)) {
        return true;
      }
      seenUrls.add(tab.url);
      return false;
    });

    if (duplicates.length > 0) {
      const tabIds = duplicates.map(tab => tab.id);
      await chrome.tabs.remove(tabIds);
      await loadTabs();
    } else {
      alert('No duplicate tabs found!');
    }
  });

  // Close tabs to right button
  document.getElementById('closeRight').addEventListener('click', async () => {
    const activeTab = allTabs.find(tab => tab.active);
    if (!activeTab) {
      alert('No active tab found!');
      return;
    }

    const activeIndex = allTabs.indexOf(activeTab);
    const tabsToClose = allTabs.slice(activeIndex + 1);

    if (tabsToClose.length > 0) {
      const tabIds = tabsToClose.map(tab => tab.id);
      await chrome.tabs.remove(tabIds);
      await loadTabs();
    } else {
      alert('No tabs to the right!');
    }
  });

  // Group by domain button
  document.getElementById('groupTabs').addEventListener('click', async () => {
    const domainGroups = {};
    
    allTabs.forEach(tab => {
      try {
        const url = new URL(tab.url);
        const domain = url.hostname.replace('www.', '');
        
        if (!domainGroups[domain]) {
          domainGroups[domain] = [];
        }
        domainGroups[domain].push(tab.id);
      } catch (e) {
        // Skip invalid URLs
      }
    });

    // Create groups for domains with multiple tabs
    let groupedCount = 0;
    for (const [domain, tabIds] of Object.entries(domainGroups)) {
      if (tabIds.length > 1) {
        try {
          const groupId = await chrome.tabs.group({ tabIds: tabIds[0] });
          await chrome.tabGroups.update(groupId, { 
            title: domain.substring(0, 15),
            color: 'blue'
          });
          
          // Move remaining tabs to the group
          for (let i = 1; i < tabIds.length; i++) {
            await chrome.tabs.move(tabIds[i], { index: -1, groupId });
          }
          groupedCount++;
        } catch (e) {
          console.error('Error creating group:', e);
        }
      }
    }

    if (groupedCount > 0) {
      alert(`Created ${groupedCount} tab groups!`);
    } else {
      alert('No domains with multiple tabs to group!');
    }
    
    await loadTabs();
  });

  // Refresh button
  document.getElementById('refreshTabs').addEventListener('click', async () => {
    await loadTabs();
  });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}
