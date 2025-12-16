/*
 * ultra_driver.cpp
 * A simple, non-blocking C++ driver for HC-SR04 sensor using pigpio.
 * Compile with: g++ -shared -o ultra_driver.so -fPIC ultra_driver.cpp -lpigpio
 * -lrt
 */

#include <pigpio.h>
#include <stdio.h>
#include <unistd.h>

// Prevent name mangling for ctypes
extern "C" {

/**
 * Initialize pigpio library.
 * Returns 0 on success, error code (<0) on failure.
 * Returns 1 if already initialized.
 */
int ultra_init() {
  int cfg = gpioCfgGetInternals();
  // If pigpio is already initialized/running, gpioInitialise returns regular
  // PID or error But we can check if it's already initialised to avoid re-init
  // issues
  if (cfg & PI_CFG_NOSIGHANDLER) {
    // Logic to detect if we are already safe?
    // Usually gpioInitialise handles re-calls gracefully, returning existing
    // version/handle.
  }

  int result = gpioInitialise();
  if (result < 0) {
    return result;
  }
  return 0;
}

/**
 * Measure distance in millimeters.
 *
 * @param trigger_pin GPIO pin for Trigger (output)
 * @param echo_pin    GPIO pin for Echo (input)
 * @return Distance in mm, or -1 if timeout/error.
 */
int ultra_measure(int trigger_pin, int echo_pin) {
  if (trigger_pin < 0 || echo_pin < 0)
    return -2; // Invalid pins

  // Ensure mode is set (safe to call repeatedly)
  gpioSetMode(trigger_pin, PI_OUTPUT);
  gpioSetMode(echo_pin, PI_INPUT);

  // Ensure trigger is low first
  gpioWrite(trigger_pin, 0);
  // Short delay to settle? (2 micros is tiny)
  gpioDelay(2);

  // 1. Send Trigger Pulse (10 us)
  gpioWrite(trigger_pin, 1);
  gpioDelay(10);
  gpioWrite(trigger_pin, 0);

  // 2. Wait for Echo High (Start of pulse)
  // Timeout: 30ms (enough for ~5 meters)
  // 30ms = 30000 us
  uint32_t start_wait = gpioTick();
  while (gpioRead(echo_pin) == 0) {
    if (gpioTick() - start_wait > 30000) {
      return -1; // Timeout waiting for echo start
    }
  }
  uint32_t pulse_start = gpioTick();

  // 3. Wait for Echo Low (End of pulse)
  // Same timeout
  while (gpioRead(echo_pin) == 1) {
    if (gpioTick() - pulse_start > 30000) {
      return -1; // Timeout waiting for echo to end (too far)
    }
  }
  uint32_t pulse_end = gpioTick();

  // 4. Calculate Duration
  uint32_t duration_us = pulse_end - pulse_start;

  // 5. Convert to distance
  // Speed of sound ~343m/s = 343000mm/s
  // Distance = (Time * Speed) / 2
  // mm = (us * 1e-6 * 343000) / 2
  // mm = (us * 0.343) / 2 = us * 0.1715
  // Integer math: (us * 343) / 2000

  int distance_mm = (duration_us * 343) / 2000;

  return distance_mm;
}

/**
 * Terminate pigpio (optional, usually kept alive).
 */
void ultra_terminate() { gpioTerminate(); }
}
