import itertools
import re
import winreg

import serial


def get_serial_ports():
    """ Uses the Win32 registry to return a
        list of serial (COM) ports
        existing on this computer.
    """
    path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
    key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    ports_list = []

    for i in itertools.count():
        try:
            val = winreg.EnumValue(key, i)

            # determine if port is available
            fullname = full_port_name(str(val[1]))
            ser = serial.Serial(fullname, 38400)
            ser.close()

            ports_list.append((str(val[1]), "Available"))
        except serial.SerialException:
            ports_list.append((str(val[1]), "Unavailable"))
        except EnvironmentError:
            break

    return ports_list


def full_port_name(portname):
    """ Given a port-name (of the form COM7,
        COM12, CNCA0, etc.) returns a full
        name suitable for opening with the
        Serial class.
    """
    m = re.match(r'^COM(\d+)$', portname)
    if m and int(m.group(1)) < 10:
        return portname
    return '\\\\.\\' + portname
