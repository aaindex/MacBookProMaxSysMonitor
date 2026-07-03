# Android App

This folder contains a native Android wrapper for the Mac Monitor dashboard.

The first Android version is intentionally small: it opens the existing Mac agent dashboard in a WebView at:

```text
http://127.0.0.1:8765
```

That address works on the phone when the Mac and phone are connected with USB debugging and this command is running on the Mac:

```bash
adb reverse tcp:8765 tcp:8765
```

## Build

Open this folder in Android Studio, or build from the command line when the Android SDK and Gradle are installed:

```bash
cd android-app
gradle assembleDebug
```

## Install

After building:

```bash
adb install -r app/build/outputs/apk/debug/app-debug.apk
```

Then start the Mac agent:

```bash
cd ../mac-agent
python3 mac_monitor_server.py
```

Forward the port:

```bash
adb reverse tcp:8765 tcp:8765
```

Open the `Mac Monitor` app on the phone.

## Current Limitations

- The app requires USB debugging and `adb reverse`.
- The Mac agent must be running before the app can show live data.
- The dashboard is still rendered by the existing web UI.
