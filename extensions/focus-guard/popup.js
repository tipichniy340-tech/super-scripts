// Focus Guard - Popup Logic
document.addEventListener('DOMContentLoaded', () => {
  // Timer elements
  const timerDisplay = document.getElementById('timer-display');
  const startBtn = document.getElementById('start-btn');
  const pauseBtn = document.getElementById('pause-btn');
  const resetBtn = document.getElementById('reset-btn');
  const pomodoroMode = document.getElementById('pomodoro-mode');
  const shortBreak = document.getElementById('short-break');

  // Blocklist elements
  const siteInput = document.getElementById('site-input');
  const addSiteBtn = document.getElementById('add-site-btn');
  const blocklist = document.getElementById('blocklist');
  const blockToggle = document.getElementById('block-toggle');

  // Stats elements
  const focusTimeEl = document.getElementById('focus-time');
  const sessionsCountEl = document.getElementById('sessions-count');
  const blockedCountEl = document.getElementById('blocked-count');
  const resetStatsBtn = document.getElementById('reset-stats-btn');

  let timerInterval = null;
  let timeLeft = 25 * 60; // 25 minutes in seconds
  let isRunning = false;

  // Load settings from storage
  chrome.storage.sync.get(['blockList', 'isBlockingEnabled', 'stats'], (result) => {
    const sites = result.blockList || [];
    const isEnabled = result.isBlockingEnabled || false;
    const stats = result.stats || { focusTime: 0, sessions: 0, blocked: 0 };

    renderBlocklist(sites);
    blockToggle.checked = isEnabled;
    updateStatsUI(stats);
  });

  // Timer functions
  function updateTimerDisplay() {
    const minutes = Math.floor(timeLeft / 60);
    const seconds = timeLeft % 60;
    timerDisplay.textContent = `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  }

  function startTimer() {
    if (!isRunning) {
      isRunning = true;
      timerInterval = setInterval(() => {
        timeLeft--;
        updateTimerDisplay();

        if (timeLeft <= 0) {
          clearInterval(timerInterval);
          isRunning = false;
          timerFinished();
        }
      }, 1000);
    }
  }

  function pauseTimer() {
    if (isRunning) {
      clearInterval(timerInterval);
      isRunning = false;
    }
  }

  function resetTimer() {
    pauseTimer();
    timeLeft = pomodoroMode.checked ? 25 * 60 : 5 * 60;
    updateTimerDisplay();
  }

  function timerFinished() {
    // Play notification sound or show notification
    chrome.notifications.create({
      type: 'basic',
      iconUrl: 'icons/icon128.png',
      title: 'Focus Guard',
      message: pomodoroMode.checked ? 'Сессия завершена! Время отдохнуть.' : 'Перерыв окончен! Пора работать.'
    });

    // Update stats
    chrome.storage.sync.get(['stats'], (result) => {
      const stats = result.stats || { focusTime: 0, sessions: 0, blocked: 0 };
      if (pomodoroMode.checked) {
        stats.sessions += 1;
        stats.focusTime += 25;
      }
      chrome.storage.sync.set({ stats });
      updateStatsUI(stats);
    });

    timeLeft = pomodoroMode.checked ? 5 * 60 : 25 * 60;
    updateTimerDisplay();
  }

  // Mode toggle
  pomodoroMode.addEventListener('change', () => {
    if (pomodoroMode.checked) {
      shortBreak.checked = false;
      timeLeft = 25 * 60;
    }
    updateTimerDisplay();
  });

  shortBreak.addEventListener('change', () => {
    if (shortBreak.checked) {
      pomodoroMode.checked = false;
      timeLeft = 5 * 60;
    }
    updateTimerDisplay();
  });

  // Button listeners
  startBtn.addEventListener('click', startTimer);
  pauseBtn.addEventListener('click', pauseTimer);
  resetBtn.addEventListener('click', resetTimer);

  // Blocklist functions
  function renderBlocklist(sites) {
    blocklist.innerHTML = '';
    sites.forEach((site, index) => {
      const li = document.createElement('li');
      li.innerHTML = `
        <span>${site}</span>
        <span class="remove-site" data-index="${index}">×</span>
      `;
      blocklist.appendChild(li);
    });

    // Add remove listeners
    document.querySelectorAll('.remove-site').forEach(btn => {
      btn.addEventListener('click', (e) => {
        const index = parseInt(e.target.dataset.index);
        removeSite(index);
      });
    });
  }

  function addSite() {
    const site = siteInput.value.trim().toLowerCase();
    if (site && !site.includes(' ')) {
      chrome.storage.sync.get(['blockList'], (result) => {
        const sites = result.blockList || [];
        if (!sites.includes(site)) {
          sites.push(site);
          chrome.storage.sync.set({ blockList: sites });
          renderBlocklist(sites);
          siteInput.value = '';
        }
      });
    }
  }

  function removeSite(index) {
    chrome.storage.sync.get(['blockList'], (result) => {
      const sites = result.blockList || [];
      sites.splice(index, 1);
      chrome.storage.sync.set({ blockList: sites });
      renderBlocklist(sites);
    });
  }

  addSiteBtn.addEventListener('click', addSite);
  siteInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') addSite();
  });

  // Global block toggle
  blockToggle.addEventListener('change', () => {
    chrome.storage.sync.set({ isBlockingEnabled: blockToggle.checked });
    const statusText = blockToggle.nextElementSibling.nextElementSibling;
    statusText.innerHTML = blockToggle.checked 
      ? 'Блокировка <strong>включена</strong>' 
      : 'Блокировка <strong>выключена</strong>';
  });

  // Stats functions
  function updateStatsUI(stats) {
    focusTimeEl.textContent = stats.focusTime || 0;
    sessionsCountEl.textContent = stats.sessions || 0;
    blockedCountEl.textContent = stats.blocked || 0;
  }

  resetStatsBtn.addEventListener('click', () => {
    const newStats = { focusTime: 0, sessions: 0, blocked: 0 };
    chrome.storage.sync.set({ stats: newStats });
    updateStatsUI(newStats);
  });

  // Listen for blocked attempts from background
  chrome.runtime.onMessage.addListener((message) => {
    if (message.type === 'SITE_BLOCKED') {
      chrome.storage.sync.get(['stats'], (result) => {
        const stats = result.stats || { focusTime: 0, sessions: 0, blocked: 0 };
        stats.blocked += 1;
        chrome.storage.sync.set({ stats });
        updateStatsUI(stats);
      });
    }
  });

  // Initialize display
  updateTimerDisplay();
});
