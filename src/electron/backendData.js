export function sendDataToBackend(mainWindow) {
  mainWindow.webContents.send('audio', {
    name: 'Backend data',
    place: 'Dublin',
    day: 'Tuesday',
  });
}

export function getStaticData() {
  return 'Static';
}
