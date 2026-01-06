extern "C" {
#include <stdio.h>
#include <pigpio.h>

#define US100_TRIGGER_PIN 23
#define US100_ECHO_PIN    24
#define TIMER_INTERVAL_US 10000

static volatile int last_distance = -1;

int getDistance()
{
    gpioWrite(US100_TRIGGER_PIN, 1);
    gpioDelay(10);
    gpioWrite(US100_TRIGGER_PIN, 0);

    uint32_t start_wait = gpioTick();
    while (gpioRead(US100_ECHO_PIN) == 0) {
        if (gpioTick() - start_wait > 30000) return -1;
    }
    uint32_t start = gpioTick();

    while (gpioRead(US100_ECHO_PIN) == 1) {
        if (gpioTick() - start > 30000) return -1;
    }
    uint32_t end = gpioTick();

    return (end - start) / 5.8;
}

void timerHandler(void)
{
    last_distance = getDistance();
}

int start_sensor()
{
    if (gpioInitialise() < 0) return -1;

    gpioSetMode(US100_TRIGGER_PIN, PI_OUTPUT);
    gpioSetMode(US100_ECHO_PIN, PI_INPUT);

    gpioSetTimerFunc(0, TIMER_INTERVAL_US, timerHandler);

    return 0;
}

int get_last_distance()
{
    return last_distance;
}

void stop_sensor()
{
    gpioTerminate();
}
}
