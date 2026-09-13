# Housie AI Desktop (Windows, macOS, Linux)

Housie AI Desktop runs natively on Windows, macOS, and Linux using Electron.

## Prerequisites
- Node.js 18+ and npm

## Development
```bash
cd electron
npm install
npm start
```

## Build Installers
To build standalone packages for your current operating system:
```bash
# Windows (.exe installer + portable)
npm run dist:win

# macOS (.dmg + .zip for Apple Silicon & Intel)
npm run dist:mac

# Linux (.AppImage + .deb)
npm run dist:linux

# All platforms (on CI)
npm run dist:all
```

Output binaries will be placed in the `electron/dist/` directory.
