from camera import camera_main
from Ultrasensor import sensor
import asyncio
import httpx
import time
import json
from datetime import datetime

SERVER_IP = "194.5.157.250"
SERVER_PORT = "13869"
BASE_URL = f"http://{SERVER_IP}:{SERVER_PORT}/api"
SLEEP_TIME = 1

camera_queue = asyncio.Queue(maxsize=1)   # <-- Shared queue for camera results

async def main():
    async with httpx.AsyncClient() as client:
        
        # Start camera task in background
        asyncio.create_task(camera_main(camera_queue))
        camera_data = None
        
        while True:
            # Ultrasound (runs instantly)
            #sensor_data = await sensor()
            try:
                # Read latest camera detection (non-blocking)
                camera_data = camera_queue.get_nowait()
            except asyncio.QueueEmpty:
                pass
                
            print(f"People detected: {camera_data}")
            
            print(
                f"[{time.strftime('%H:%M:%S')}] "
                #f"Sensor distance: {sensor_data}, "
                f"People detected: {camera_data}"
            )
            """
            # --- SEND ULTRASOUND ----
            try:
                response = await client.post(
                    f"{BASE_URL}/ultrasound",
                    json={"distance": sensor_data, "trackTime": time.time()},
                    timeout=5
                )
                print("Ultrasound sent:", response.status_code)
            except Exception as e:
                print("Error sending ultrasound:", e)
			"""
            # --- SEND CAMERA ----
            try:
                response = await client.post(
                    f"{BASE_URL}/camera/new",
                    json={"number": camera_data, "trackTime": datetime.now().isoformat()},
                    timeout=5
                )
                print("Camera sent:", response.status_code)
            except Exception as e:
                print("Error sending camera:", e)
			
            await asyncio.sleep(SLEEP_TIME)
            
if __name__ == "__main__":
    asyncio.run(main())
