// QR Generator Pro - Popup Script

document.addEventListener('DOMContentLoaded', () => {
  const qrText = document.getElementById('qr-text');
  const currentPageBtn = document.getElementById('current-page-btn');
  const generateBtn = document.getElementById('generate-btn');
  const qrSize = document.getElementById('qr-size');
  const qrColor = document.getElementById('qr-color');
  const qrBg = document.getElementById('qr-bg');
  const qrResult = document.getElementById('qr-result');
  const qrCanvas = document.getElementById('qr-canvas');
  const downloadBtn = document.getElementById('download-btn');
  const copyBtn = document.getElementById('copy-btn');
  const historyList = document.getElementById('history-list');
  const clearHistoryBtn = document.getElementById('clear-history-btn');

  let currentQRData = null;

  // Загрузка истории из storage
  loadHistory();

  // Кнопка "Текущая страница"
  currentPageBtn.addEventListener('click', async () => {
    try {
      const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
      if (tab && tab.url) {
        qrText.value = tab.url;
      }
    } catch (error) {
      console.error('Ошибка получения URL:', error);
    }
  });

  // Генерация QR-кода
  generateBtn.addEventListener('click', () => {
    const text = qrText.value.trim();
    if (!text) {
      alert('Введите текст или URL для генерации QR-кода');
      return;
    }

    const size = parseInt(qrSize.value);
    const color = qrColor.value;
    const bgColor = qrBg.value;

    generateQRCode(text, size, color, bgColor);
    saveToHistory(text);
  });

  // Генерация QR с использованием библиотеки
  function generateQRCode(text, size, color, bgColor) {
    QRCode.toCanvas(qrCanvas, text, {
      width: size,
      color: {
        dark: color,
        light: bgColor
      },
      margin: 2
    }, (error) => {
      if (error) {
        console.error('Ошибка генерации QR:', error);
        alert('Ошибка при создании QR-кода');
        return;
      }
      qrResult.classList.remove('hidden');
      currentQRData = text;
    });
  }

  // Скачивание QR-кода
  downloadBtn.addEventListener('click', () => {
    if (!currentQRData) return;

    const link = document.createElement('a');
    link.download = `qr-code-${Date.now()}.png`;
    link.href = qrCanvas.toDataURL('image/png');
    link.click();
  });

  // Копирование в буфер обмена
  copyBtn.addEventListener('click', async () => {
    if (!currentQRData) return;

    try {
      const blob = await new Promise(resolve => qrCanvas.toBlob(resolve, 'image/png'));
      await navigator.clipboard.write([
        new ClipboardItem({
          'image/png': blob
        })
      ]);
      alert('QR-код скопирован в буфер обмена!');
    } catch (error) {
      console.error('Ошибка копирования:', error);
      alert('Не удалось скопировать изображение');
    }
  });

  // Сохранение в историю
  function saveToHistory(text) {
    chrome.storage.local.get(['history'], (result) => {
      let history = result.history || [];
      
      // Удаляем дубликат если есть
      history = history.filter(item => item !== text);
      
      // Добавляем в начало
      history.unshift(text);
      
      // Ограничиваем до 10 записей
      if (history.length > 10) {
        history = history.slice(0, 10);
      }

      chrome.storage.local.set({ history }, () => {
        loadHistory();
      });
    });
  }

  // Загрузка истории
  function loadHistory() {
    chrome.storage.local.get(['history'], (result) => {
      const history = result.history || [];
      historyList.innerHTML = '';

      if (history.length === 0) {
        historyList.innerHTML = '<li style="cursor: default; color: #999;">История пуста</li>';
        return;
      }

      history.forEach((item, index) => {
        const li = document.createElement('li');
        li.textContent = item.length > 40 ? item.substring(0, 40) + '...' : item;
        li.title = item;
        li.addEventListener('click', () => {
          qrText.value = item;
          generateBtn.click();
        });
        historyList.appendChild(li);
      });
    });
  }

  // Очистка истории
  clearHistoryBtn.addEventListener('click', () => {
    if (confirm('Вы уверены, что хотите очистить историю?')) {
      chrome.storage.local.remove(['history'], () => {
        loadHistory();
      });
    }
  });

  // Контекстное меню - обработка сообщения
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'generateQR') {
      qrText.value = request.text;
      generateBtn.click();
    }
  });
});
