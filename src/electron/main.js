import { app, BrowserWindow, ipcMain, dialog } from 'electron';
import path from 'path';
import fs from 'node:fs';
import process from 'node:process';
import { isDev } from './util.js';
import { getPreloadPath } from './pathResolver.js';
import { getStaticData, sendDataToBackend } from './backendData.js';
import { spawn } from 'child_process';

const PYTHON_PATHS = {
  win32: path.join('src', 'scripts', 'venv', 'Scripts', 'python.exe'),
  default: path.join('src', 'scripts', 'venv', 'bin', 'python'),
};

const getBasePath = () =>
  process.env.NODE_ENV === 'development'
    ? app.getAppPath()
    : process.resourcesPath;

const getExecutablePath = () => {
  const base = getBasePath();

  if (process.platform === 'win32') {
    // Use compiled executable on Windows
    return path.join(base, 'dist-python', 'neurally-python.exe');
  } else {
    // Use Python script on other platforms
    const pythonPath = PYTHON_PATHS[process.platform] || PYTHON_PATHS.default;
    return path.join(base, pythonPath);
  }
};

const getMainScriptPath = () => {
  const base = getBasePath();

  if (process.platform === 'win32') {
    // No script path needed for Windows executable
    return null;
  } else {
    return path.join(base, 'src', 'scripts', 'main.py');
  }
};

const createPythonProcess = (executable, scriptPath, args, env = {}) => {
  return new Promise((resolve, reject) => {
    // Check if executable exists
    if (!fs.existsSync(executable)) {
      reject({
        message: 'Processing component not found',
        details: `Executable not found: ${executable}`,
        code: -1
      });
      return;
    }

    const processEnv = { ...process.env, ...env };

    if (app.isPackaged) {
      processEnv.NEURALLY_NO_LOG = '1';
    }

    // For Windows executable, don't pass scriptPath
    const spawnArgs = scriptPath ? [scriptPath, ...args] : args;
    const child = spawn(executable, spawnArgs, { env: processEnv });

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
        // Provide more specific error messages based on common issues
        let errorMessage = 'Internal processing error';
        
        if (error.includes('No module named')) {
          errorMessage = 'Module configuration error';
        } else if (error.includes('File not found') || error.includes('No such file')) {
          errorMessage = 'File access error';
        } else if (error.includes('Permission denied')) {
          errorMessage = 'Permission error';
        }
        
        reject({
          message: errorMessage,
          details: error || output,
          code: code
        });
      }
    });
  });
};

const executeHD = async (testType, filePaths, isMultiple = false) => {
  const executable = getExecutablePath();
  const scriptPath = getMainScriptPath();

  const args = isMultiple
    ? [testType, '--multiple', filePaths.join('|')]
    : [testType, filePaths];

  return createPythonProcess(executable, scriptPath, args);
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

  ipcMain.handle('processHD', async (event, testType, filePaths) => {
    try {
      const isMultiple = Array.isArray(filePaths);
      const result = await executeHD(testType, filePaths, isMultiple);
      return result;
    } catch (error) {
      console.log('Python error: ', error);
      // Return a user-friendly error message instead of throwing technical details
      return {
        status: 'error',
        message: 'Internal error occurred during processing. Please try again.',
        details: app.isPackaged ? null : error.toString() // Only show details in development
      };
    }
  });

  ipcMain.handle('openFileDialog', async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog({
      properties: ['openFile', 'multiSelections'],
      filters: [
        {
          name: 'Audio Files',
          extensions: ['wav', 'mp3', 'm4a', 'WAV', 'MP3', 'M4A'],
        },
        { name: 'WAV Files', extensions: ['wav', 'WAV'] },
        { name: 'MP3 Files', extensions: ['mp3', 'MP3'] },
        { name: 'M4A Files', extensions: ['m4a', 'M4A'] },
        { name: 'All Files', extensions: ['*'] },
      ],
    });

    if (canceled) {
      return null;
    }

    return filePaths;
  });

  ipcMain.handle('cleanupOutputDirectory', async () => {
    cleanupOutputDirectory();
    return { success: true };
  });
};

const cleanupOutputDirectory = () => {
  try {
    const base = getBasePath();
    const outputPath = path.join(base, 'src', 'scripts', 'output');

    if (fs.existsSync(outputPath)) {
      fs.rmSync(outputPath, { recursive: true, force: true });
    }
  } catch (error) {
    console.error('Error cleaning up output directory:', error);
  }
};

app.whenReady().then(() => {
  createMainWindow();
});

// Cleanup on app exit
app.on('before-quit', () => {
  cleanupOutputDirectory();
});

app.on('window-all-closed', () => {
  cleanupOutputDirectory();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    createMainWindow();
  }
});
