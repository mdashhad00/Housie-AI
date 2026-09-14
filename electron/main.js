const { app, BrowserWindow, ipcMain, Notification, shell, session } = require('electron');
const path = require('path');

let mainWindow;

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1240,
    height: 840,
    minWidth: 800,
    minHeight: 600,
    title: 'Housie AI — Your Smart AI Companion',
    backgroundColor: '#0f172a',
    autoHideMenuBar: true,
    show: false,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
      nodeIntegration: false,
      contextIsolation: true,
      webSecurity: true,
      spellcheck: true
    }
  });

  // Automatically grant audio / microphone permissions for Whisper STT and speech synthesis
  session.defaultSession.setPermissionRequestHandler((webContents, permission, callback) => {
    const allowed = ['media', 'audioCapture', 'notifications'];
    if (allowed.includes(permission)) {
      callback(true);
    } else {
      callback(false);
    }
  });

  // Try loading live URL first if online, fallback to local index.html
  const liveUrl = 'https://housie-ai.vercel.app';
  const localFile = path.join(__dirname, '..', 'index.html');

  mainWindow.loadURL(liveUrl).catch(() => {
    mainWindow.loadFile(localFile);
  });

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
  });

  // Handle external links in native system browser
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    if (url.startsWith('http:') || url.startsWith('https:') || url.startsWith('mailto:') || url.startsWith('tel:')) {
      shell.openExternal(url);
      return { action: 'deny' };
    }
    return { action: 'allow' };
  });

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

// IPC Handlers
ipcMain.on('window-minimize', () => {
  if (mainWindow) mainWindow.minimize();
});

ipcMain.on('window-maximize', () => {
  if (mainWindow) {
    if (mainWindow.isMaximized()) mainWindow.unmaximize();
    else mainWindow.maximize();
  }
});

ipcMain.on('window-close', () => {
  if (mainWindow) mainWindow.close();
});

ipcMain.on('show-notification', (event, { title, body }) => {
  if (Notification.isSupported()) {
    new Notification({ title: title || 'Housie AI', body: body || '' }).show();
  }
});

// Computer Control IPC Handler
const { spawn } = require('child_process');
ipcMain.handle('execute-control-command', async (event, { message }) => {
  return new Promise((resolve) => {
    const pythonExe = process.platform === 'win32' ? 'python' : 'python3';
    const pyCode = `
import sys, json, os
sys.path.insert(0, r'${path.join(__dirname, '..').replace(/\\/g, '/')}')
from core.planner import Planner
from controller.factory import get_controller
plan = Planner.plan_from_text('''${message.replace(/'/g, "\\'")}''')
ctrl = get_controller()
results = [ctrl.execute_tool(s['tool'], s['args']) for s in plan]
print(json.dumps({'plan': plan, 'results': results, 'platform': ctrl.platform_name}))
`;
    const child = spawn(pythonExe, ['-c', pyCode]);
    let stdout = '';
    let stderr = '';
    child.stdout.on('data', (d) => { stdout += d.toString(); });
    child.stderr.on('data', (d) => { stderr += d.toString(); });
    child.on('close', (code) => {
      try {
        const parsed = JSON.parse(stdout.trim());
        resolve({ success: code === 0, ...parsed });
      } catch (e) {
        resolve({ success: false, error: stderr || stdout || 'Execution failed' });
      }
    });
  });
});

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
