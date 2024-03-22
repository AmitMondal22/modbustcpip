from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform

# Create an instance of ModbusServer
server = ModbusServer("127.0.0.1", 502, no_block=True)

try:
    print("Start server...")
    server.start()
    print("Server is online")
    state = [0]
    while True:
        server.data_bank.set_input_registers(0, [int(uniform(20, 100))])
        if state != server.data_bank.get_input_registers(1):
            state = server.data_bank.get_input_registers(1)
            print("Value of Register 1 has changed to " + str(state))
        sleep(0.5)

except Exception as e:
    print("Error:", e)

finally:
    print("Shutdown server ...")
    server.stop()
    print("Server is offline")
