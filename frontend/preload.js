const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  startRecognition: () => ipcRenderer.send('start-recognition'),
  stopRecognition: () => ipcRenderer.send('stop-recognition'),
  startCollection: (name) => ipcRenderer.send('start-collection', name)
});
