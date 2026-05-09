// QR Generator Pro - Background Script

chrome.runtime.onInstalled.addListener(() => {
  // Создаем контекстное меню
  chrome.contextMenus.create({
    id: "generateQR",
    title: "Создать QR-код для \"%s\"",
    contexts: ["selection", "link", "page"]
  });
});

// Обработка клика по контекстному меню
chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === "generateQR") {
    let text = info.selectionText || info.linkUrl || info.pageUrl;
    
    // Отправляем сообщение popup
    chrome.runtime.sendMessage({
      action: "generateQR",
      text: text
    }).catch(() => {
      // Если popup закрыт, открываем его и передаем данные через storage
      chrome.storage.local.set({ pendingQR: text }, () => {
        chrome.action.openPopup();
      });
    });
  }
});

// Обработка сообщения от popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "getActiveTabUrl") {
    chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      if (tabs[0]) {
        sendResponse({ url: tabs[0].url });
      }
    });
    return true; // Для асинхронного ответа
  }
});
