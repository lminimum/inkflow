import { app, shell, BrowserWindow, ipcMain } from 'electron'
import { join } from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
import icon from '../../resources/icon.png?asset'
import { spawn, ChildProcess } from 'child_process'
import path from 'path'

let backendProcess: ChildProcess | null = null

function getBackendPath(): string | null {
  const isDev = is.dev
  if (isDev) {
    // In development, we might run the backend manually or not at all.
    // Returning null will prevent the app from trying to start it.
    return null
  }

  // In production, the executable is packaged into the app's resources.
  // Note the '.exe' extension for Windows. Adjust for other platforms if needed.
  const platform = process.platform
  const extension = platform === 'win32' ? '.exe' : ''

  // The 'to' field in extraResources in electron-builder.yml is 'backend'
  return path.join(process.resourcesPath, 'backend', `ink-backend${extension}`)
}

function createWindow(): void {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 1100,
    height: 675,
    show: false,
    autoHideMenuBar: true,
    frame: false,
    ...(process.platform !== 'darwin' ? { icon } : {}),
    webPreferences: {
      preload: join(__dirname, '../preload/index.js'),
      sandbox: false
    }
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  // HMR for renderer base on electron-vite cli.
  // Load the remote URL for development or the local html file for production.
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(join(__dirname, '../renderer/index.html'))
  }
}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  // Start the backend process
  const backendPath = getBackendPath()
  if (backendPath) {
    console.log(`Starting backend from: ${backendPath}`)
    backendProcess = spawn(backendPath, [], {
      stdio: 'ignore', // You can change this to 'inherit' to see backend logs
      detached: false
    })

    backendProcess.on('error', (err) => {
      console.error('Failed to start backend process:', err)
    })

    backendProcess.on('close', (code) => {
      console.log(`Backend process exited with code ${code}`)
    })
  }

  // Set app user model id for windows
  electronApp.setAppUserModelId('com.electron')

  // Default open or close DevTools by F12 in development
  // and ignore CommandOrControl + R in production.
  // see https://github.com/alex8088/electron-toolkit/tree/master/packages/utils
  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  // IPC test
  ipcMain.on('ping', () => console.log('pong'))

  ipcMain.on('window-minimize', () => {
    const win = BrowserWindow.getFocusedWindow()
    if (win) win.minimize()
  })

  ipcMain.on('window-maximize', () => {
    const win = BrowserWindow.getFocusedWindow()
    if (win) {
      if (win.isMaximized()) {
        win.unmaximize()
      } else {
        win.maximize()
      }
    }
  })

  ipcMain.on('window-close', () => {
    const win = BrowserWindow.getFocusedWindow()
    if (win) win.close()
  })

  createWindow()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('will-quit', () => {
  if (backendProcess) {
    console.log('Killing backend process...')
    backendProcess.kill()
    backendProcess = null
  }
})

// In this file you can include the rest of your app's specific main process
// code. You can also put them in separate files and require them here.
