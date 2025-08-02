const electron = require('electron');

electron.contextBridge.exposeInMainWorld('electron', {
  logSomething: (callback) => {
    electron.ipcRenderer.on('audio', (_, data) => {
      callback(data);
    });
    console.log('something');
  },
  downloadResultsCSV: (csvContent, defaultPath) =>
    electron.ipcRenderer.invoke('downloadResultsCSV', {
      csvContent,
      defaultPath,
    }),
  downloadResultsImage: (imagePath, defaultPath) =>
    electron.ipcRenderer.invoke('downloadResultsImage', {
      imagePath,
      defaultPath,
    }),
  getImageDataUrl: (imagePath) =>
    electron.ipcRenderer.invoke('getImageDataUrl', imagePath),
  fileUpload: () => electron.ipcRenderer.invoke('openFileDialog'),
  processSingleFileHD: (testType, filePath) =>
    electron.ipcRenderer.invoke('processSingleFileHD', testType, filePath),
  processMultipleFilesHD: (testType, filePaths) =>
    electron.ipcRenderer.invoke('processMultipleFilesHD', testType, filePaths),
  invokeSomething: () => electron.ipcRenderer.invoke('invokeSomething'),
});
