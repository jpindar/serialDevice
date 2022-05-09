# pylint: disable=unused-argument,line-too-long
"""
File: serialdevice_pyserial.py

Unlike some libraries, pySerial works with comports up to at least COM99. Nice.

One reason there are several similar ways to read from the port is that I was getting some
unexpected variations in speed when calling pySerial's routines. You'd think the built-in
routines would be faster but they weren't always.

TODO: test what happens if any of these are called on a port that's not open
(such as one whose USB cable has been disconnected)

baud rates of 19200, 115200, and 230400 work
baud rate of 460800 doesn't work reliably

"""
__author__ = 'jpindar@jpindar.com'
import logging
import time
import serial
import serial.tools.list_ports
from typing import List, Dict, Optional, Any, Union

read_delay = 0.2
baud_rate = 19200

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_ports() -> List[Union[int, str]]:
    """
    ask pySerial for a list of com ports
    """
    possible_ports: List[serial.ListPortInfo] = serial.tools.list_ports.comports()
    ports: List[Union[int, str]] = []
    for i in possible_ports:
        s = str(i.device) + ' ' + str(i.description) + ' ' + str(i.hwid)
        logger.info(s)
        s = i.device   # something like 'COM4'
        ports.append(int(s[3:]))  # from position 3 to the end, to handle multi-digit port numbers
    logger.info("ports reported by pySerial:" + str(ports))
    if (ports is None) or (ports == []):
        return ['']  # because we are most likely going to display this
    return ports


class SerialDevice:
    """
    An object that represents a generic serial device
    """

    def __init__(self):
        """
        Constructor for serial device, no parameters
        This constructor just creates the object, doesn't give it a serial port
        """
        self.comPort = None
        self.port_num = None

    def open_port(self, connection_info: List) -> None:
        """
        opens a serial port
        connection_info[0] should be an integer, 0 meaning COM1, etc
        returns True if it succeeded, False if there was an error
        :param connection_info: a list, 0th element is an integer
        :return: boolean
        """
        self.close_port()
        self.port_num = connection_info[0]
        port_name = "COM" + str(self.port_num)
        logger.info("opening serial port " + port_name)
        try:
            self.comPort = serial.Serial(port=port_name,
                                         baudrate=baud_rate,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,
                                         bytesize=serial.EIGHTBITS,
                                         timeout=2,
                                         write_timeout=2)
        except ValueError as e:
            logger.warning("SerialDevice.openPort: Serial port setting out of range\r\n")
            logger.warning(e.__class__)
            # logger.warn(e.__doc__)
            raise e
        except (serial.SerialException, serial.SerialTimeoutException) as e:
            logger.warning("SerialDevice.openPort: Can't open that serial port\r\n")
            logger.warning(e.__class__)
            logger.warning(e.__doc__)
            raise e
        except Exception as e:
            logger.warning("SerialDevice.openPort: Can't open that serial port\r\n")
            logger.warning(e.__class__)
            logger.warning(e.__doc__)
            raise e
        else:
            logger.info("SerialDevice.openPort: opened a " + str(self.comPort.__class__))

    def is_open(self) -> bool:
        """
        This is really just checking if open_port() succeeded
        """
        if not hasattr(self, 'comPort'):
            logger.warning("is_open(): com port does not exist")
            return False
        if self.comPort is None:
            logger.warning("is_open(): com port does not exist")
            return False
        if not self.comPort.isOpen():
            logger.warning("is_open(): comPort.isOpen() is false")
            return False
        return True

    def close_port(self) -> None:
        if not hasattr(self, 'comPort'):
            return
        if not hasattr(self.comPort, 'close'):
            return
        try:
            self.comPort.close()
        except Exception as e:
            logger.warning(e.__class__)
            raise e

    def write(self, msg: str) -> None:
        """
        send a string
        don't need to check if port is open, comport.write() does that

        :param msg: the string to send
        :return: none
        """
        # self.comPort.reset_input_buffer()
        # self.comPort.reset_output_buffer()
        if not self.is_open():  # this only checks the higher level software, not the actual port
            logger.warning("can't write to the serial port because it is not open")
            # TODO raise an appropriate exception here
            return
        # logger.info("SerialDevice.write: writing " + str(msg) + " to serial port")
        try:
            self.comPort.write(msg.encode(encoding='UTF-8'))
        # if the port was never opened it would cause an attribute error
        # but that would be detected by the self.is_open
        except serial.PortNotOpenError as e:
            logger.warning("SerialDevice.write: can't write to the serial port\r\n")
            logger.warning(e.__class__)
            logger.warning(e.__doc__)
            raise e
        except serial.SerialException as e:
            # this is the error  you get if the USB cable for a virtual com port has disconnected
            logger.warning("SerialDevice.write: can't write to the serial port\r\n")
            logger.warning(e.__class__)
            logger.warning(e.__doc__)
            raise e
        except Exception as e:  # catching all exceptions is OK as long as we re-raise them
            logger.error(e.__class__)
            raise e

    def read(self) -> Optional[str]:
        """
        reads a response from the serial port
        TODO: investigate possible timing issues: is self.comPort.readline() slow ?
        """
        r_bytes = None
        # delay was 0.2 for old, slow BBUQ device
        # time.sleep(read_delay)  # read can fail if no delay here, 0.2 works
        if not self.is_open():  # this only checks the higher level software, not the actual port
            logger.warning("can't read from the serial port because it is not open")
            # TODO raise an appropriate exception here - IOError?
            return None
        r_bytes: bytearray = bytearray()
        try:
            # print(time.time())
            # r_bytes = self.comPort.readline()
            # r_bytes = self.comPort.read_until(serial.CR, 100)
            # r_bytes = self._read_until(serial.CR, 1000)
            r_bytes = self._readline()
            # print(time.time())
        except serial.PortNotOpenError as e:
            logger.warning(e.__class__)
            logger.warning(e.__doc__)
            logger.warning(e.strerror)
            logger.warning(e.__cause__)
            # raise e
            return None
        except serial.SerialException as e:
            # this is the error  you get if the USB cable for a virtual com port has disconnected
            logger.warning("SerialDevice.read: error raised by serial port read")
            logger.warning(e.__class__)
            logger.warning(e.__doc__)
            logger.warning(e.strerror)
            logger.warning(e.__cause__)
            # raise e
            return None
        except (IOError, AttributeError) as e:
            logger.warning("SerialDevice.read: didn't get a response from serial port " + str(self.port_num))
            logger.warning("exception: " + str(e.__class__))
            logger.warning(e.__doc__)
            # logger.warning(e.strerror)  # attributeError has no strerror
            logger.warning(e.__cause__)
            return None
        else:
            r_str: str = r_bytes.decode(encoding='UTF-8')
            return r_str.strip('\r\n')

    def _read_until(self, terminator=serial.LF, max_size=1000):
        """
        Read until a termination sequence is found, the size
        is exceeded or until timeout occurs.
        This is copied from serialutil.py, part of pySerial
        But it runs faster here?
        """
        length_of_termination = len(terminator)
        line: bytearray = bytearray()
        count = 0
        c: bytes = bytes()
        while True:
            c = self.comPort.read(1)
            if c:
                line += c
                count += 1
                if line[-length_of_termination:] == terminator:
                    break
                if max_size is not None and count >= max_size:
                    break
            else:
                break
        return line

    def _readline(self, terminator='\r', max_size=1000) -> bytearray:
        """
        implemented this myself because PySerial's readline() is extremely slow
        :param terminator: read until you receive this termination character(s)
        :return: bytes (because that's what the original .readline() returns)
        #  the default value of max_size is a completely arbitrary number
        """
        c = None
        length_of_termination = len(terminator)
        line: bytearray = bytearray()
        count = 0
        c: bytes = bytes()
        try:
            while self.comPort.inWaiting() > 0:
                # c = self.comPort.read(self.comPort.inWaiting())   # would this be faster?
                c = self.comPort.read(1)
                if c:
                    line += c
                    count += 1
                    if line[-length_of_termination:] == terminator:
                        break
                    if count > max_size:
                        break
                else:
                    break
        except Exception as e:
            logger.error("in _readline")
            logger.error(e.__class__)
            raise e  # let .read() handle it

        return line
