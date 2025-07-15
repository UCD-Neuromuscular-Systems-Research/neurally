const electron = require('electron');

electron.contextBridge.exposeInMainWorld('electron', {
  logSomething: (callback) => {
    electron.ipcRenderer.on('audio', (_, data) => {
      callback(data);
    });
    console.log('something');
  },
  invokeSomething: () => electron.ipcRenderer.invoke('invokeSomething'),
});
