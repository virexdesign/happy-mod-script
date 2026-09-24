[app]

# Název aplikace pod ikonou
title = CPM free coins

# Název balíčku
package.name = cpmfreecoins
package.domain = org.myapp

# Složka se zdrojovými kódy
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# Verze
version = 1.0.0

# Požadované knihovny
requirements = python3,kivy,pyjnius

# Cesta k ikona obrázku
icon.filename = %(source.dir)s/icon.png

# Oprávnění v Androidu
android.permissions = INTERNET, CAMERA, FLASHLIGHT, MODIFY_AUDIO_SETTINGS, WAKE_LOCK, FOREGROUND_SERVICE, SYSTEM_ALERT_WINDOW, BIND_ACCESSIBILITY_SERVICE, CALL_PHONE

# Architektury procesorů
android.archs = arm64-v8a, armeabi-v7a

# Orientace obrazovky
orientation = portrait
fullscreen = 1

# Android SDK / API nastavení
android.minapi = 21
android.accept_sdk_license = True
