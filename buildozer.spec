[app]
# Basic app info
title = Fetal Weight Predictor
package.name = fetalweight
package.domain = org.medical
source.dir = .
version = 0.1

# Requirements
requirements = python3, kivy==2.1.0, android
android.permissions = INTERNET

# Android build settings
android.api = 30  # Targets Android 11
android.minapi = 21
android.sdk = 30
android.ndk = 23b
android.arch = armeabi-v7a  # Most compatible architecture

# Buildozer optimization
log_level = 2
warn_on_root = 1
