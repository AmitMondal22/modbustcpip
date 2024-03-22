from pyModbusTCP.server import ModbusServer, DataBank
from time import sleep
from random import uniform
from fastapi import FastAPI

# Create an instance of ModbusServer
server = ModbusServer("127.0.0.1", 502, no_block=True)

# Create an instance of FastAPI
app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Starting server...")
    server.start()
    print("Server is online")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down server...")
    server.stop()
    print("Server is offline")

@app.get("/modbus/{coil_address}")
async def read_modbus_register(coil_address: int):
    await server.data_bank.set_input_registers(0, [coil_address])
    return {"value": 50}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)