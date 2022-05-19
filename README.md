# serialDevice

Some code for controlling devices via a serial port. 

This uses pySerial, which can be found at https://pypi.python.org/pypi/pyserial and https://github.com/pyserial/pyserial


Files:

* serialdevice.py - a module representing a generic serial device

* serialdevice_demo.py - an example of using serialdevice by itself

* serialdevice_tests.py  -  tests for serialdevice

* multimeter.py  -  a module using serialdevice to represent a Fluke 8845A digital multimeter

* multimeter_demo.py - an example of using multimeter

At this time, multmeter only uses a few of the 8845A's many functions, but more will be added later.
