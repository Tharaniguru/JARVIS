const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('api', {
  startListening: () => ipcRenderer.send('start-listening'),
  stopListening: () => ipcRenderer.send('stop-listening'),
  startRecognition: () => ipcRenderer.send('start-recognition'),
  stopRecognition: () => ipcRenderer.send('stop-recognition'),
  startCollection: (name) => ipcRenderer.send('start-collection', name)
});
