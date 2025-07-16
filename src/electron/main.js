import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import path from 'path';
import { isDev } from './util.js';
import { getPreloadPath } from './pathResolver.js';
import { getStaticData, sendDataToBackend } from './backendData.js';

const createMainWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      preload: getPreloadPath(),
    },
  });

  if (isDev()) {
    mainWindow.loadURL('http://localhost:5123');
  } else {
    mainWindow.loadFile(path.join(app.getAppPath() + '/dist-react/index.html'));
  }

  sendDataToBackend(mainWindow);

  ipcMain.handle('invokeSomething', () => {
    return getStaticData();
  });

  ipcMain.handle('openFileDialog', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ['openFile'],
      filters: [{ name: 'Audio files', extensions: ['wav'] }],
    });

    if (canceled) {
      return null;
    }

    return filePaths[0];
  });
};

app.whenReady().then(() => {
  createMainWindow();
});
