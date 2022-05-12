"""
tests for serialdevice.py
These are meant to run with a loopback adapter on the serial port

Note that in the absence of a configured log file, log messages may
 be sent to stdout

"""
import unittest
import serialdevice

PORT_NUMBER = 5

def setup():
  dut = serialdevice.SerialDevice()


class SomeTests(unittest.TestCase):

    def test1(self):
        dut = serialdevice.SerialDevice()
        self.assertEqual(dut.is_open(), False)
        dut = None

    def test2(self):
        dut = serialdevice.SerialDevice()
        dut.open_port([PORT_NUMBER])
        self.assertEqual(dut.is_open(), True)
        dut.close_port()
        self.assertEqual(dut.is_open(), False)
        dut = None

    def test3(self):
        dut = serialdevice.SerialDevice()
        dut.open_port([PORT_NUMBER])
        dut.open_port([PORT_NUMBER])
        self.assertEqual(dut.is_open(), True)
        # note that we didn't close the port, but the next open should close it if necessary

    def test4(self):
        dut = serialdevice.SerialDevice()
        dut.open_port([PORT_NUMBER])
        dut.write("Hello, loopback\n")
        response = dut.read()
        self.assertEqual(response, "Hello, loopback")
        # note the termination is supposed to be stripped by dut.read()

if __name__ == '__main__':
    print()
    unittest.main()

