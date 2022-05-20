"""
A minimal program to demonstrate the use of multimeter.py to communicate with a Fluke 8845A digital
multimeter via a serial port

Author: jpindar@jpindar.com

Requirements: multimeter.py
              serialdevice.py
              pySerial:  https://pypi.python.org/pypi/pyserial  https://github.com/pyserial/pyserial

"""
__author__ = 'jpindar@jpindar.com'
import sys
import logging
from serialdevice import get_ports
from multimeter import Multimeter


def main():
    """
    basic usage example
    There are checks here that are for testing that aren't needed in production code

    There is no exception handling here because it would be done differently depending on the context

    TODO: add the 'abort, retry, ignore' system I have used before
    """
    print("Serial ports detected: ")
    ports = get_ports()
    for n in ports:
       print(n)

    # here you could prompt the user to select a port, read if from a config file or whatever
    p = 5  # for COM5

    print("Connecting to Fluke DMM")
    dmm = Multimeter(p)
    print("Found the instrument at " + str(dmm.port_name))

    if dmm.is_open():
        print('The serial port is open')

    s = dmm.get_ID()
    if s == "":
        print("The device did not return an ID string")
        sys.exit()

    print("The device returned ID string:  " + s)
    if s == Multimeter.GOOD_ID_RESPONSE:
        print("OK")
    elif s == Multimeter.GOOD_ID_RESPONSE_45:
        print("The meter is in the wrong mode (Fluke 45 emulation).")
        sys.exit()
    else:
        print("ERROR")
        sys.exit()

    s = dmm.get_errors()
    if s != Multimeter.ERROR_CODE_OK:
        print(s)
    dmm.clear_errors()

    dmm.remote()
    print("measuring DC voltage...")
    v = dmm.get_DCVolts()

    if isinstance(v, float):
         print(f"{v} volts dc")
    else:
         print("Did not get a response from the multimeter")

    dmm.close_port()


if __name__ == '__main__':
    main()


