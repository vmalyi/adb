import tempfile
from subprocess import check_output, CalledProcessError, call
import subprocess

import var as v

def _isDeviceAvailable():
    """
    Private Function to check if device is available;
    To be used by only functions inside module
    :return: True or False
    """
    result = getserialno()
    if result[1].strip() == "unknown":
        return False
    else:
        return True


def version():
    """
    Display the version of adb
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_VERSION]
    return _exec_command(adb_full_cmd)


def wait_for_device(timeout=10):
    """
    Blocks execution until the device is online - that is, until the instance state is device.
    :param timeout: timeout value for the function to exit automatically, default value is 10.
    :return: result of _exec_command_with_timer() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_WAITFORDEVICE]
    return _exec_command_with_timer(adb_full_cmd, timeout=timeout)


def bugreport(dest_file="default.log"):
    """
    Prints dumpsys, dumpstate, and logcat data to the screen, for the purposes of bug reporting
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_BUGREPORT]
    try:
        dest_file_handler = open(dest_file, "w")
    except IOError:
        print "IOError: Failed to create a log file"
    
    # We have to check if device is available or not before executing this command
    # as adb bugreport will wait-for-device infinitely and does not come out of 
    # loop
    # Execute only if device is available only
    if _isDeviceAvailable():
        result = _exec_command_to_file(adb_full_cmd, dest_file_handler)
        return (result, "Success: Bug report saved to: " + dest_file)
    else:
        return (0, "Device Not Found")


def push(src, dest):
    """
    Push object from host to target
    :param src: string path to source object on host
    :param dest: string destination path on target
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_PUSH, src, dest]
    return _exec_command(adb_full_cmd)


def pull(src, dest):
    """
    Pull object from target to host
    :param src: string path of object on target
    :param dest: string destination path on host
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_PULL, src, dest]
    return _exec_command(adb_full_cmd)


def devices(opts=[]):
    """
    Get list of all available devices including emulators
    :param opts: list command options (e.g. ["-r", "-a"])
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_DEVICES, _convert_opts(opts)]
    return _exec_command(adb_full_cmd)


def shell(cmd):
    """
    Execute shell command on target
    :param cmd: string shell command to execute
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_SHELL, cmd]
    return _exec_command(adb_full_cmd)


def install(apk, opts=[]):
    """
    Install *.apk on target
    :param apk: string path to apk on host to install
    :param opts: list command options (e.g. ["-r", "-a"])
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_INSTALL, _convert_opts(opts), apk]
    return _exec_command(adb_full_cmd)


def uninstall(app, opts=[]):
    """
    Uninstall app from target
    :param app: app name to uninstall from target (e.g. "com.example.android.valid")
    :param opts: list command options (e.g. ["-r", "-a"])
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_UNINSTALL, _convert_opts(opts), app]
    return _exec_command(adb_full_cmd)


def getserialno():
    """
    Get serial number for all available target devices
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_GETSERIALNO]
    return _exec_command(adb_full_cmd)


def sync():
    """
    Copy host->device only if changed
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_SHELL ,v.ADB_COMMAND_SYNC]
    return _exec_command(adb_full_cmd)


def start_server():
    """
    Startd adb server daemon on host
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_START_SERVER]
    return _exec_command(adb_full_cmd)


def kill_server():
    """
    Kill adb server daemon on host
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_KILL_SERVER]
    return _exec_command(adb_full_cmd)


def get_state():
    """
    Get state of device connected per adb
    :return: result of _exec_command() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_GET_STATE]
    return _exec_command(adb_full_cmd)


def _convert_opts(opts):
    """
    Convert list with command options to single string value
    with 'space' delimeter
    :param opts: list with space-delimeted values
    :return: string with space-delimeted values
    """
    return ' '.join(opts)


def _exec_command(adb_cmd):
    """
    Format adb command and execute it in shell
    :param adb_cmd: list adb command to execute
    :return: string '0' and shell command output if successful, otherwise
    raise CalledProcessError exception and return error code
    """
    t = tempfile.TemporaryFile()
    final_adb_cmd = []
    for e in adb_cmd:
        if e != '':  # avoid items with empty string...
            final_adb_cmd.append(e)  # ... so that final command doesn't
            # contain extra spaces
    print('\n*** Executing ' + ' '.join(adb_cmd) + ' ' + 'command')

    try:
        output = check_output(final_adb_cmd, stderr=t)
    except CalledProcessError as e:
        t.seek(0)
        result = e.returncode, t.read()
    else:
        result = 0, output
        print('\n' + result[1])

    return result


def _exec_command_with_timer(adb_cmd, cwd=None, shell=False, kill_tree=True, timeout=20, env=None):
    """
    Format adb command and execute it in shell, after the default timeout of
    20 seconds it automatically kills the process and comes out of function
    :param adb_cmd: list adb command to execute
    :param cwd: Current working directory, default value is set to None
    :param shell: spawns a sub-shell for the command to run, default value is set
                  to None
    :param kill_tree: kills all the subprocess launched by command, default
                      value is set to True
    :param timeout: Time set to come out of the function, default value is set to 20
    :param env: Environment, default set to None
    :return: integer 0 and shell command output, shell command error if successful,
             integer 1 and shell command output, shell command error if timeout occurs,
             otherwise raise CalledProcessError exception and return error code
    """
    from threading import Timer
    print('\n*** Executing ' + ' '.join(adb_cmd) + ' ' + 'command')
    try:
        p = subprocess.Popen(adb_cmd, shell=shell, cwd=cwd, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, env=env)
        if timeout != -1:
            timer = Timer(timeout, p.kill)
            timer.start()
        stdout, stderr = p.communicate()
        if timeout != -1:
            timer.cancel()
        result = p.returncode, stdout,stderr
    except CalledProcessError as e:
        result = p.returncode, stdout, stderr
    
    return result


def _exec_command_to_file(adb_cmd, dest_file_handler):
    """
    Format adb command and execute it in shell and redirects to a file
    :param adb_cmd: list adb command to execute
    :param dest_file_handler: file handler to which output will be redirected
    :return: string '0' and writes shell command output to file if successful, otherwise
    raise CalledProcessError exception and return error code
    """
    t = tempfile.TemporaryFile()
    final_adb_cmd = []
    for e in adb_cmd:
        if e != '':  # avoid items with empty string...
            final_adb_cmd.append(e)  # ... so that final command doesn't
            # contain extra spaces
    print('\n*** Executing ' + ' '.join(adb_cmd) + ' ' + 'command')

    try:
        output = call(final_adb_cmd, stdout=dest_file_handler, stderr=t)
    except CalledProcessError as e:
        t.seek(0)
        result = e.returncode, t.read()
    else:
        result = output
        dest_file_handler.close()

    return result