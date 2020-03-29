adb_android
==========

Enables android adb in your python script.

### Project status

[![Build Status](https://travis-ci.org/vmalyi/adb_android.svg?branch=master)](https://travis-ci.org/vmalyi/adb_android)
[![Analytics](https://ga-beacon.appspot.com/UA-70264103-1/vmalyi/adb_android/README)](https://github.com/igrigorik/ga-beacon)

### Purpose

This python package is a wrapper for standard android adb implementation. It allows you to execute android adb commands in your python script.

### What's supported?

Currently following adb commands are **supported**:
* adb push
* adb pull
* adb shell
* adb devices
* adb install
* adb uninstall
* adb get-serialno
* adb start-server
* adb kill-server
* adb get-state
* adb sync
* adb version
* adb bugreport
* adb help

Currently following adb commands are **not supported**:

* adb forward
* adb wait-for-device
* adb logcat
* adb jdwp
* ~~adb help~~
* adb -d
* adb -e
* adb -s

### How to install?

Install with help of pip:
```
pip install adb_android
```
### How to use?
```
from adb_android import adb_android

adb_android.push('/tmp/file.txt', '/data/media/0')
adb_android.pull('/data/media/0/file.txt', '/tmp/')
adb_android.shell('ls')
adb_android.devices()
adb_android.bugreport("report.log")
adb_android.install('/usr/local/app.apk')
adb_android.uninstall('com.example.android.valid')
adb_android.getserialno()

...
```

### How to contribute?

* Implement adb commands which are currently not supported by the module (see above)
* Increase unit test coverage for already supported commands
* Bring your own ideas!
