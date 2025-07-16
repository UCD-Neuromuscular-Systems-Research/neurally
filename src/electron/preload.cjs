const electron = require('electron');

electron.contextBridge.exposeInMainWorld('electron', {
  logSomething: (callback) => {
    electron.ipcRenderer.on('audio', (_, data) => {
      callback(data);
    });
    console.log('something');
  },
  fileUpload: () => electron.ipcRenderer.invoke('openFileDialog'),
  invokeSomething: () => electron.ipcRenderer.invoke('invokeSomething'),
});
