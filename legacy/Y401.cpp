
extern "C" {
#include <stdio.h>
#include <pigpio.h>

// Pin configuration (BCM numbers)
#define US100_TRIGGER_PIN 23
#define US100_ECHO_PIN    24

// Timer interval (10 ms = 10,000 us)
#define TIMER_INTERVAL_US 10000

// Measure distance using pigpio pulse detection
int getDistance()
{
    // Trigger pulse
    gpioWrite(US100_TRIGGER_PIN, 1);
    gpioDelay(10);                 // 10 µs high
    gpioWrite(US100_TRIGGER_PIN, 0);

    // Wait for echo start
    while (gpioRead(US100_ECHO_PIN) == 0);
    uint32_t start = gpioTick();

    // Wait for echo end
    while (gpioRead(US100_ECHO_PIN) == 1);
    uint32_t end = gpioTick();

    // Pulse length in microseconds
    uint32_t duration = end - start;

    // Convert µs → mm (speed of sound)
    int distance = duration / 5.8;     // ~0.172 mm/µs → 1/0.172 = 5.81

    return distance;
}

// Timer callback (runs every 10 ms)
void timerHandler(void)
{
    printf("TIMER!\n");
    int dist = getDistance();
    printf("Distance: %d mm\n", dist);
}

int main()
{
    if (gpioInitialise() < 0)
    {
        printf("pigpio init failed\n");
        return 1;
    }
  
    printf("pigpio initialized\n");

    // Configure pins
    gpioSetMode(US100_TRIGGER_PIN, PI_OUTPUT);
    gpioSetMode(US100_ECHO_PIN, PI_INPUT);

    // Create repeating timer (10,000 µs = 10 ms)
    gpioSetTimerFunc(0, TIMER_INTERVAL_US, timerHandler);

    // Main loop (pigpio needs the program to stay alive)
    while (1)
    {
        time_sleep(1);
    }

    gpioTerminate();
    return 0;
}
}
