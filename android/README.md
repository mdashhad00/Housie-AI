# Housie AI for Android

Housie AI supports Android in two ways:
1. **Instant Progressive Web App (PWA / WebAPK)**: Open https://housie-ai.vercel.app in Chrome on Android and tap **"Install App"** or **"Add to Home Screen"**. It installs as a real standalone Android application with its own icon, splash screen, and full-screen window!
2. **Native Android APK**: Built using Capacitor or Bubblewrap CLI.

## How to Build the APK via Bubblewrap (Official Google WebAPK Tool)
```bash
# 1. Install bubblewrap CLI
npm install -g @bubblewrap/cli

# 2. Initialize project from manifest
bubblewrap init --manifest=https://housie-ai.vercel.app/manifest.json

# 3. Build signed APK
bubblewrap build
```

## How to Build via Capacitor
```bash
npm install @capacitor/core @capacitor/cli @capacitor/android
npx cap init "Housie AI" com.housieai.app --web-dir public
npx cap add android
npx cap open android
# In Android Studio: Build -> Build Bundle(s) / APK(s) -> Build APK(s)
```

The compiled APK will be at `android/app/build/outputs/apk/release/app-release.apk`.
