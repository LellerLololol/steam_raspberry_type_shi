import asyncio
import ctypes
import pathlib
import time
import statistics
import logging
from concurrent.futures import ThreadPoolExecutor

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AsyncUltraSensor:
    def __init__(self, trigger_pin=23, echo_pin=24, lib_path="ultra_driver.so"):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        self.lib_path = lib_path
        self._executor = ThreadPoolExecutor(max_workers=1)
        self._lib = None
        self._load_library()
        
    def _load_library(self):
        """Load the C++ shared library."""
        try:
            full_path = pathlib.Path(__file__).parent / self.lib_path
            logger.info(f"Loading library from: {full_path}")
            self._lib = ctypes.CDLL(str(full_path))
            
            # Setup return types and argument types
            self._lib.ultra_init.restype = ctypes.c_int
            self._lib.ultra_measure.argtypes = [ctypes.c_int, ctypes.c_int]
            self._lib.ultra_measure.restype = ctypes.c_int
            
            # Initialize GPIO
            res = self._lib.ultra_init()
            if res < 0:
                logger.error(f"Failed to initialize pigpio (error code {res})")
                raise RuntimeError("pigpio initialization failed. Are you running with sudo?")
            logger.info("pigpio initialized successfully.")
            
        except OSError as e:
            logger.error(f"Could not load library {self.lib_path}: {e}")
            logger.error("Did you run 'sh compile_driver.sh' first?")
            raise

    def d_measure_sync(self):
        """Blocking call to C++ function (runs in < 40ms typically)."""
        if not self._lib:
            return -1
        return self._lib.ultra_measure(self.trigger_pin, self.echo_pin)

    async def get_distance(self):
        """
        Get a single distance measurement asynchronously.
        Returns distance in cm, or None if error.
        """
        loop = asyncio.get_running_loop()
        # Run the C function in a separate thread to avoid blocking the asyncio event loop
        dist_mm = await loop.run_in_executor(self._executor, self.d_measure_sync)
        
        if dist_mm < 0:
            return None # Timeout or error
            
        return dist_mm / 10.0 # Convert mm to cm

    async def get_filtered_distance(self, samples=5):
        """
        Get the median of 'samples' measurements to filter noise (garbage info).
        """
        readings = []
        for _ in range(samples):
            d = await self.get_distance()
            if d is not None and 2.0 < d < 400.0: # Valid range 2cm - 400cm
                readings.append(d)
            # Small sleep between bursts to let echoes die down
            await asyncio.sleep(0.01) 
            
        if not readings:
            return None
            
        return statistics.median(readings)

async def main():
    """Test function"""
    try:
        sensor = AsyncUltraSensor(trigger_pin=23, echo_pin=24)
        print("Starting sensor loop... Press Ctrl+C to stop.")
        while True:
            dist = await sensor.get_filtered_distance(samples=3)
            if dist:
                print(f"Distance: {dist:.1f} cm")
            else:
                print("Distance: --")
            await asyncio.sleep(0.5)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nStopped.")
