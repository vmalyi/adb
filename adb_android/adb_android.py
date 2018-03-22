import tempfile
import re
from subprocess import check_output, CalledProcessError, call
from adb_android import var as v


def __convert_flags(flags):
    """
    Convert list with command options to single string value
    with 'space' delimeter
    :param flags: list with space-delimeted values
    :return: string with space-delimeted values
     """
    if flags is None:
        return ''
    return ' '.join(flags)


def __get_devices():
    """
    Returns the name[s] of all ADB connected devices
    :return: True or False
    """
    retVal = []
    error, devices_output = devices(quiet=True)
    for line in devices_output.splitlines():
        result = re.match("([^ ]+)[ \t]+device$", line)
        if result is not None:
            retVal.append(result.groups()[0])
    return retVal


def __prompt_if_multiple_devices():
    devices = __get_devices()
    if len(devices) == 0:
        print("There are no connected devices. Not executing command")
        return devices
    if len(devices) == 1:
        return devices

    print("There is more than 1 device connected. Select device numbers seperated by space to execute or enter nothing to run on all")
    for i in range(0, len(devices)):
        print('{}: {}'.format(i, devices[i]))
    input_raw = input("Enter target[s] to run command\n")

    # If the user did not enter any numbers, return all devices
    if not input_raw.strip():
        return devices

    # Add only the devices the user selected to the return value
    indexes = input_raw.split()
    retVal = []
    for i in indexes:
        retVal.append(devices[int(i)])
    return retVal


def __get_devices_from_list(indexes):
    devices = __get_devices()
    # If an empty list is given, return all devices
    if indexes is None or len(indexes) == 0:
        return devices
    retVal = []
    # Validate there are more devices than given indexes
    if len(indexes) > len(devices):
        # TODO: Throw an exceptions
        return retVal
    # Get the devices of the given indexes
    for i in range(0, len(indexes)):
        # TODO: verify index is valid within devices
        retVal.append(devices[indexes[i]])
    return retVal


def version():
    """
    Display the version of adb
    :return: result of __exec_command() execution
    """
    adb_full_cmd = v.ADB_COMMAND_VERSION
    return __exec_command(adb_full_cmd)


def os_version(device_indexes=None):
    """
    Display the version of the OS of target
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_OS_VERSION
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def connect(ip, port):
    """
    Connect ADB to the target from IP and port number
    :return: result of __exec_command() execution
    """
    adb_full_cmd = v.ADB_COMMAND_CONNECT.format(ip, port)
    return __exec_command(adb_full_cmd)


def bugreport(dest_file="default.log"):
    """
    Prints dumpsys, dumpstate, and logcat data to the screen, for the purposes of bug reporting
    :return: result of __exec_command_on_device_to_file() execution
    """
    adb_full_cmd = [v.ADB_COMMAND_PREFIX, v.ADB_COMMAND_BUGREPORT]
    try:
        dest_file_handler = open(dest_file, "w")
    except IOError:
        print("IOError: Failed to create a log file")

    # We have to check if device is available or not before executing this command
    # as adb bugreport will wait-for-device infinitely and does not come out of 
    # loop
    # Execute only if device is available only
    __exec_command_on_device_to_file(adb_full_cmd, dest_file_handler)
    return (1, "Success: Bug report saved to: " + dest_file)


def push(src, dest, device_indexes=None):
    """
    Push object from host to target
    :param src: string path to source object on host
    :param dest: string destination path on target
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_PUSH.format(src, dest)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def pull(src, dest, device_indexes=None):
    """
    Pull object from target to host
    :param src: string path of object on target
    :param dest: string destination path on host
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_PULL.format(src, dest)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def rm(path, device_indexes=None):
    """
    Remove the given file or directory on target[s]
    :param src: string path of object on target
    :param dest: string destination path on host
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_RM.format(path)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def devices(quiet=False):
    """
    Get list of all available devices including emulators
    :param flags: list command options (e.g. ["-r", "-a"])
    :return: result of __exec_command() execution
    """
    adb_full_cmd = v.ADB_COMMAND_DEVICES.format()
    return __exec_command(adb_full_cmd, quiet=quiet)


def launch(application_name, main_activity, flags=None, device_indexes=None):
    """
    Launch app identified by the package name and main activity on target
    :param cmd: string shell command to execute
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_LAUNCH.format(__convert_flags(flags), application_name, main_activity)
    return __exec_command_on_device(adb_full_cmd, device_indexes)

def install(apk_path, flags=None, device_indexes=None):
    """
    Install *.apk on target
    :param apk: string path to apk on host to install
    :param flags: list command options (e.g. ["-r", "-a"])
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_INSTALL.format(__convert_flags(flags), apk_path)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def uninstall(application_name, device_indexes=None):
    """
    Uninstall app from target
    :param app: app name to uninstall from target (e.g. "com.example.android.valid")
    :param flags: list command options (e.g. ["-r", "-a"])
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_UNINSTALL.format(application_name)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def close(application_name, device_indexes=None):
    """
    Uninstall app from target
    :param app: app name to uninstall from target (e.g. "com.example.android.valid")
    :param flags: list command options (e.g. ["-r", "-a"])
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_CLOSE.format(application_name)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def clear(application_name, device_indexes=None):
    """
    Wipe all cache and user data associated to that app on target[s]
    :param app: app name to uninstall from target (e.g. "com.example.android.valid")
    :param flags: list command options (e.g. ["-r", "-a"])
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_CLEAR.format(application_name)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def getserialno(device_indexes=None):
    """
    Get serial number for all available target devices
    :return: result of __exec_command() execution
    """
    adb_full_cmd = v.ADB_COMMAND_GETSERIALNO
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def wait_for_device():
    """
    Block execution until the device is online
    :return: result of __exec_command() execution
    """
    adb_full_cmd = v.ADB_COMMAND_WAITFORDEVICE
    return __exec_command(adb_full_cmd)


def start_server():
    """
    Startd adb server daemon on host
    :return: result of __exec_command() execution
    """
    adb_full_cmd = v.ADB_COMMAND_START_SERVER
    return __exec_command(adb_full_cmd)


def kill_server():
    """
    Kill adb server daemon on host
    :return: result of __exec_command() execution
    """
    adb_full_cmd = v.ADB_COMMAND_KILL_SERVER
    return __exec_command(adb_full_cmd)


def get_state(device_indexes=None):
    """
    Get state of device connected per adb
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_GET_STATE
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def packages(device_indexes=None):
    """
    Get the list of packages on target[s]
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_PACKAGES
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def apps(device_indexes=None):
    """
    Get the list of installed applications on target[s]
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_APPS
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def run_tests(application_name, flags=None, device_indexes=None):
    """
    Run the instrumented tests of the given app with given flags on target[s]
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_TESTS.format(__convert_flags(flags), application_name)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def input_text(text, device_indexes=None):
    """
    Simulate user text input on target[s]
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_INPUT_TEXT.format(text)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def input_swipe(x1, y1, x2, y2, duration, device_indexes=None):
    """
    Simulate user swipe at given co-ordinates to co-ordinates for duration
    on target[s]
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_SWIPE.format(x1, y1, x2, y2, duration)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def input_keyevent(event, device_indexes=None):
    """
    Simulate event from given event code on target[s]
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_KEYEVENT.format(event)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def input_tap(x, y, device_indexes=None):
    """
    Simulate user tap at given co-ordinates on target[s]
    :return: result of __exec_command_on_device() execution
    """
    adb_full_cmd = v.ADB_COMMAND_TAP.format(x, y)
    return __exec_command_on_device(adb_full_cmd, device_indexes)


def __exec_adb_command(adb_cmd, quiet=False):
    """
    Execute the given ADB command in shell and print the output if
    not set to quiet.
    :param adb_cmd: string adb command to execute
    :return: string '0' and shell command output if successful, otherwise
    raise CalledProcessError exception and return error code
    """
    if not quiet:
        print('Running command: {}'.format(adb_cmd))

    t = tempfile.TemporaryFile()
    try:
        output = check_output(adb_cmd, stderr=t).decode("utf-8")
    except CalledProcessError as e:
        t.seek(0)
        result = e.returncode, t.read() + e.output
        if not quiet:
            print(result[1].decode('unicode_escape'))
    else:
        # There is a bug in adb.exe where output from `install`, `push` and
        # `pull` will write output to stderr even in the success cases.
        # To work-around this, if stdout is empty, we instead return what
        # is written to stderr as the success output.
        if not output:
            t.seek(0)
            result = 0, t.read().decode('unicode_escape')
        else:
            result = 0, output
        if not quiet:
            print(result[1])

    return result


def __exec_adb_command_to_file(adb_cmd, dest_file_handler):
    """
    Execute the given ADB command in shell and redirects to a file
    :param adb_cmd: string adb command to execute
    :return: string '0' and shell command output if successful, otherwise
    raise CalledProcessError exception and return error code
    """
    print('Running command: {} to file'.format(adb_cmd))

    t = tempfile.TemporaryFile()
    try:
        output = call(adb_cmd, stdout=dest_file_handler, stderr=t)
    except CalledProcessError as e:
        t.seek(0)
        result = e.returncode, t.read()
    else:
        result = output
        dest_file_handler.close()

    return result


def __exec_command_on_device(adb_cmd, device_indexes=None):
    """
    Run the given ADB command on the connected device. If there are multiple connected
    devices, prompt the user for input unless the devices to execute on have been given
    :param adb_cmd: string adb command to execute
    :return: list of string '0' and shell command output if successful, otherwise
    raise CalledProcessError exception and return error code
    """
    if device_indexes is None:
        devices = __prompt_if_multiple_devices()
    else:
        devices = __get_devices_from_list(device_indexes)
    result = []
    for device in devices:
        result.append(__exec_adb_command('{} -s {} {}'.format(v.ADB_COMMAND_PREFIX, device, adb_cmd)))
    return result


def __exec_command(adb_cmd, quiet=False):
    """
    Run the given ADB command which does not require a connected device
    :param adb_cmd: string adb command to execute
    :return: string '0' and shell command output if successful, otherwise
    raise CalledProcessError exception and return error code
    """
    return __exec_adb_command('{} {}'.format(v.ADB_COMMAND_PREFIX, adb_cmd), quiet)


def __exec_command_on_device_to_file(adb_cmd, dest_file_handler):
    """
    Format adb command and execute it in shell and redirects to a file
    :param adb_cmd: string adb command to execute
    :param dest_file_handler: file handler to which output will be redirected
    :return: string '0' and writes shell command output to file if successful, otherwise
    raise CalledProcessError exception and return error code
    """
    devices = __prompt_if_multiple_devices()
    result = []
    for device in devices:
        result.append(__exec_adb_command_to_file('{} -s {} {}'.format(v.ADB_COMMAND_PREFIX, device, adb_cmd), dest_file_handler))
    return result

def __exec_command_to_file(adb_cmd, dest_file_handler):
    """
    Run the given ADB command which does not require a connected device and
    redirect output to a file
    :param adb_cmd: string adb command to execute
    :param dest_file_handler: file handler to which output will be redirected
    :return: string '0' and writes shell command output to file if successful, otherwise
    raise CalledProcessError exception and return error code
    """
    return __exec_adb_command_to_file('{} {}'.format(v.ADB_COMMAND_PREFIX, adb_cmd), dest_file_handler)
