"""
a simple script for demonstrating serialdevice modules

"""
__author__ = 'jpindar'
import sys
import time
import logging
import serialdevice

ID_QUERY1 = "*IDN?\n"
ID_QUERY2 = "ID?\r"
PORT_NUMBER = 5

log_filename = "serialdevice_demo.log"
logger = logging.getLogger(__name__)
logging.basicConfig(filename=log_filename, filemode='a', format='%(levelname)-8s:%(asctime)s %(name)s: %(message)s')
logger.setLevel(logging.INFO)
logger.info("Serialdevice demo")

print(serialdevice.get_ports())

dut = serialdevice.SerialDevice()
print("opening port")
logger.info("opening port")
try:
    dut.open_port([PORT_NUMBER])
except Exception as e:
    pass  # catching exceptions here just to create a breakpoint for debugger

# You generally don't need to test this, but you can if you want to
if not dut.is_open():
    print("port is not open")

print("writing ID query")
dut.write(ID_QUERY1)
# time.sleep(read_delay)
print("reading response")

response = dut.read()

if response == '':
    print("no response")
else:
    print(response)


dut.close_port()









