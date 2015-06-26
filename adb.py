import os
import tempfile
import pdb
from subprocess import check_output, CalledProcessError

ADB_COMMAND_PREFIX = 'adb'
ADB_COMMAND_SHELL = 'shell'
ADB_COMMAND_PULL = 'pull'
ADB_COMMAND_PUSH = 'push'
ADB_COMMAND_RM = 'rm -r'
ADB_COMMAND_CHMOD = 'chmod -R 777'
ADB_COMMAND_UNINSTALL = 'uninstall'
ADB_COMMAND_INSTALL = 'install'
ADB_COMMAND_FORWARD = 'forward'
ADB_COMMAND_DEVICES = 'devices'

def push(src, dest):
    """Pushes files and folders to device."""
    if (src is not None) and (dest is not None):
        adb_full_cmd = [ ADB_COMMAND_PREFIX, ADB_COMMAND_PUSH, src, dest ]
        return exec_command(adb_full_cmd)
    else:
        return False

def pull(src, dest):
    """Pulls files and folders to device."""
    if (src is not None) and (dest is not None):
        adb_full_cmd = [ ADB_COMMAND_PREFIX, ADB_COMMAND_PULL, src, dest ]
        return exec_command(adb_full_cmd)
    else:
        return False

def devices():
    """Provides list of available devices"""
    #todo: return device IDs
    adb_full_cmd = [ ADB_COMMAND_PREFIX, ADB_COMMAND_DEVICES ]
    return exec_command(adb_full_cmd)

def shell(subcommand):
    """Executes subcommand in adb shell

    accepts string as "subcommand" argument
    example: "adb shell cat filename.txt"

    """
    adb_full_cmd = [ ADB_COMMAND_PREFIX, ADB_COMMAND_SHELL, subcommand ]
    return exec_command(adb_full_cmd)

def exec_command(adb_full_cmd):
    """Executes adb command and handles result code.

    Based on adb command execution result returns
    True (0) or False (!=0).

    """
    if adb_full_cmd is not None:
        try:
            t = tempfile.TemporaryFile()
            output = check_output(adb_full_cmd, stderr=t)
            result = 0, output
            print('*** executing ' + '"' + ' '.join(adb_full_cmd) + '"' \
            + ' command')
        except CalledProcessError as e:
            t.seek(0)
            result = e.returncode, t.read()
        print(result[1])
        return result
    else:
        return False
