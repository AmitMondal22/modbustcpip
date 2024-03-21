from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pyModbusTCP.server import ModbusServer, DataBank

# Create FastAPI instance
app = FastAPI()


# Set up CORS
origins = [
    "http://localhost",
    "http://localhost:8000",
    "http://192.168.29.10:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create a Modbus server instance
server = ModbusServer("127.0.0.1", 1024, no_block=True)  # Assuming port 502

# Start the Modbus server
def start_modbus_server():
    server.start()
    print("Modbus TCP server started")

# Stop the Modbus server
def stop_modbus_server():
    server.stop()
    print("Modbus TCP server stopped")

# Function to read coil status
def read_coil_status(coil_address):
    coil_status = DataBank.get_bits(coil_address, 1)
    return coil_status[0] if coil_status else None

# Route to start the Modbus server
@app.get("/start_modbus_server")
async def start_server_route():
    start_modbus_server()
    return {"message": "Modbus TCP server starting..."}

# Route to stop the Modbus server
@app.get("/stop_modbus_server")
async def stop_server_route():
    stop_modbus_server()
    return {"message": "Modbus TCP server stopping..."}

# Route to read coil status
@app.get("/read_coil_status/{coil_address}")
async def read_coil_status_route(coil_address: int):
    coil_status = read_coil_status(coil_address)
    if coil_status is not None:
        return {"coil_address": coil_address, "coil_status": coil_status}
    else:
        return {"error": "Failed to read coil status"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)