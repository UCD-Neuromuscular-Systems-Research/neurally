import path from 'node:path';
import { app } from 'electron';
import { isDev } from './util.js';

export function getPreloadPath() {
  if (isDev()) {
    return path.join(app.getAppPath(), 'src', 'electron', 'preload.cjs');
  }
  return path.join(process.resourcesPath, 'src', 'electron', 'preload.cjs');
}
