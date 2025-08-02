import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import path from 'path';
import fs from 'node:fs';
import process from 'node:process';
import { isDev } from './util.js';
import { getPreloadPath } from './pathResolver.js';
import { getStaticData, sendDataToBackend } from './backendData.js';
import { spawn } from 'child_process';

const processSingleFileHD = (testType, filePath) => {
  const base =
    process.env.NODE_ENV === 'development'
      ? app.getAppPath()
      : process.resourcesPath;

  const pythonExe =
    process.platform === 'win32'
      ? path.join(base, 'src', 'scripts', 'venv', 'Scripts', 'python.exe')
      : path.join(base, 'src', 'scripts', 'venv', 'bin', 'python');

  const scriptPath = path.join(base, 'src', 'scripts', 'main.py');

  return new Promise((resolve, reject) => {
    const env = { ...process.env };

    if (app.isPackaged) {
      // Disable logging in production
      env.NEURALLY_NO_LOG = '1';
    }

    const child = spawn(pythonExe, [scriptPath, testType, filePath], { env });
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

const processMultipleFilesHD = async (testType, filePaths) => {
  const base =
    process.env.NODE_ENV === 'development'
      ? app.getAppPath()
      : process.resourcesPath;

  const pythonExe =
    process.platform === 'win32'
      ? path.join(base, 'src', 'scripts', 'venv', 'Scripts', 'python.exe')
      : path.join(base, 'src', 'scripts', 'venv', 'bin', 'python');

  const scriptPath = path.join(base, 'src', 'scripts', 'main.py');

  return new Promise((resolve, reject) => {
    const env = { ...process.env };

    if (app.isPackaged) {
      env.NEURALLY_NO_LOG = '1';
    }

    // Join file paths with a separator that Python can split
    const filePathsString = filePaths.join('|');

    const child = spawn(
      pythonExe,
      [scriptPath, testType, '--multiple', filePathsString],
      { env }
    );
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

// TODO: Make this normal size once, the app is properly styled responsively
const createMainWindow = () => {
  const mainWindow = new BrowserWindow({
    width: 1280,
    height: 800,
    // fullscreen: true,
    resizable: false,
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

  ipcMain.handle(
    'downloadResultsCSV',
    async (event, { csvContent, defaultPath }) => {
      const win = BrowserWindow.getFocusedWindow();
      const { filePath, canceled } = await dialog.showSaveDialog(win, {
        title: 'Save Results as CSV',
        defaultPath: defaultPath || 'results.csv',
        filters: [{ name: 'CSV Files', extensions: ['csv'] }],
      });
      if (canceled || !filePath) return { success: false };
      try {
        fs.writeFileSync(filePath, csvContent, 'utf-8');
        return { success: true, filePath };
      } catch (err) {
        return { success: false, error: err.message };
      }
    }
  );

  ipcMain.handle(
    'downloadResultsImage',
    async (event, { imagePath, defaultPath }) => {
      const win = BrowserWindow.getFocusedWindow();
      const ext = path.extname(imagePath).toLowerCase();
      const { filePath, canceled } = await dialog.showSaveDialog(win, {
        title: 'Save Plot Image',
        defaultPath: defaultPath || `plot${ext}`,
        filters: [{ name: 'Image Files', extensions: [ext.replace('.', '')] }],
      });
      if (canceled || !filePath) return { success: false };
      try {
        fs.copyFileSync(imagePath, filePath);
        return { success: true, filePath };
      } catch (err) {
        return { success: false, error: err.message };
      }
    }
  );

  ipcMain.handle('getImageDataUrl', async (event, imagePath) => {
    try {
      const ext = path.extname(imagePath).toLowerCase();
      let mimeType = 'image/png';
      if (ext === '.jpg' || ext === '.jpeg') mimeType = 'image/jpeg';
      const imageBuffer = fs.readFileSync(imagePath);
      const base64 = imageBuffer.toString('base64');
      return `data:${mimeType};base64,${base64}`;
    } catch (error) {
      console.error('Error reading image: ', error);
      return null;
    }
  });

  ipcMain.handle('processSingleFileHD', async (event, testType, filePath) => {
    try {
      const result = await processSingleFileHD(testType, filePath);
      console.log(result, 'Result main');
      return result;
    } catch (error) {
      console.log('Python error: ', error);
      throw error;
    }
  });

  ipcMain.handle(
    'processMultipleFilesHD',
    async (event, testType, filePaths) => {
      try {
        const result = await processMultipleFilesHD(testType, filePaths);
        console.log(result, 'Multi-file result main');
        return result;
      } catch (error) {
        console.log('Python error: ', error);
        throw error;
      }
    }
  );

  ipcMain.handle('openFileDialog', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ['openFiles'],
      filters: [{ name: 'Audio files', extensions: ['wav'] }],
    });

    if (canceled) {
      return null;
    }

    return filePaths;
  });
};

app.whenReady().then(() => {
  createMainWindow();
});
