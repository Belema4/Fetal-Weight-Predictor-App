[app]
# Basic app information
title = Fetal Weight Predictor
package.name = fetalweight
package.domain = org.medical
source.dir = .
version = 1.0

# Python requirements
requirements = python3, kivy==2.1.0

# Android configuration
android.ndk_path = $HOME/.buildozer/android/platform/android-ndk-r23b
android.sdk_path = $HOME/.buildozer/android/platform/android-sdk
android.arch = armeabi-v7a
android.api = 30
android.minapi = 21
android.gradle_dependencies = 'com.android.tools.build:gradle:7.0.0'

# Permissions
android.permissions = INTERNET

# Build settings
log_level = 2
warn_on_root = 1
