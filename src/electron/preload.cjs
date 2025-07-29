const electron = require('electron');

electron.contextBridge.exposeInMainWorld('electron', {
  logSomething: (callback) => {
    electron.ipcRenderer.on('audio', (_, data) => {
      callback(data);
    });
    console.log('something');
  },
  getImageDataUrl: (imagePath) =>
    electron.ipcRenderer.invoke('getImageDataUrl', imagePath),
  fileUpload: () => electron.ipcRenderer.invoke('openFileDialog'),
  processAudio: (filePath) =>
    electron.ipcRenderer.invoke('processAudio', filePath),
  processSingleFileHD: (testType, filePath) =>
    electron.ipcRenderer.invoke('processSingleFileHD', testType, filePath),
  invokeSomething: () => electron.ipcRenderer.invoke('invokeSomething'),
});
