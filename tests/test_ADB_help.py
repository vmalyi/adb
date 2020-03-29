import inspect
import os
import re
import sys
import tempfile
import unittest

adb_android = os.path.realpath(
    os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], '../adb_android')))
if adb_android not in sys.path:
    sys.path.insert(0, adb_android)
import adb_android as adb
import var as v
#from sure import expect



a=adb.adb_help()
print(a)
