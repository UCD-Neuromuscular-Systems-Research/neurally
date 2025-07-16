import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import path from 'path';
import { isDev } from './util.js';
import { getPreloadPath } from './pathResolver.js';
import { getStaticData, sendDataToBackend } from './backendData.js';
import { spawn } from 'child_process';

const processAudio = (filePath) => {
  const pythonExe =
    process.platform === 'win32'
      ? path.join(app.getAppPath(), 'src/python/venv/Scripts/python.exe')
      : path.join(app.getAppPath(), 'src/python/venv/bin/python');
  const scriptPath = path.join(app.getAppPath(), 'src/python/process_audio.py');
  return new Promise((resolve, reject) => {
    const child = spawn(pythonExe, [scriptPath, filePath]);
    let output = '';
    let error = '';
    child.stdout.on('data', (data) => {
      output += data.toString();
    });

    child.stderr.on('data', (data) => {
      error += data.toString();
    });

    child.on('close', (code) => {
      if (code === 0) {
        resolve(output.trim());
      } else {
        reject(error || output);
      }
    });
  });
};

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

  ipcMain.handle('processAudio', (event, filePath) => {
    console.log(event);
    processAudio(filePath)
      .then((result) => console.log('Python output:', result))
      .catch((err) => console.error('Python error:', err));
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
