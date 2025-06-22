// frontend/main.js
const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

function createWindow() {
  const win = new BrowserWindow({
    width: 800,
    height: 700,
    webPreferences: {
      preload: path.join(__dirname, 'preload.js'),
    }
  });

  win.loadFile('index.html');
}

app.whenReady().then(() => {
  createWindow();

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) createWindow();
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});

// Face Recognition handler
let recognitionProcess = null;

ipcMain.on('start-recognition', () => {
  if (recognitionProcess) {
    console.log('Recognition already running.');
    return;
  }

  recognitionProcess = spawn('python', [
    path.join(__dirname, '../backend/face_recognition/recognize_face.py')
  ]);

  recognitionProcess.stdout.on('data', (data) => {
    console.log(`[RECOGNITION] ${data}`);
  });

  recognitionProcess.stderr.on('data', (data) => {
    console.error(`[RECOGNITION ERROR] ${data}`);
  });

  recognitionProcess.on('close', (code) => {
    console.log(`Face recognition script exited with code ${code}`);
    recognitionProcess = null;
  });
});

ipcMain.on('stop-recognition', () => {
  if (recognitionProcess) {
    recognitionProcess.kill();
    console.log('[INFO] Recognition process stopped.');
  } else {
    console.log('[INFO] No recognition process running.');
  }
});

// Face Collection handler
ipcMain.on('start-collection', (event, name) => {
  const pythonProcess = spawn('python', [
    path.join(__dirname, '../backend/face_recognition/collect_face.py'),
    name
  ]);

  pythonProcess.stdout.on('data', (data) => {
    console.log(`[COLLECT] ${data}`);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`[COLLECT ERROR] ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Face collection script exited with code ${code}`);
  });
});
