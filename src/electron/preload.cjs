const electron = require('electron');

electron.contextBridge.exposeInMainWorld('electron', {
  logSomething: (callback) => {
    electron.ipcRenderer.on('audio', (_, data) => {
      callback(data);
    });
    console.log('something');
  },
  fileUpload: () => electron.ipcRenderer.invoke('openFileDialog'),
  processAudio: (filePath) =>
    electron.ipcRenderer.invoke('processAudio', filePath),
  invokeSomething: () => electron.ipcRenderer.invoke('invokeSomething'),
});
