#include <wiringPi.h>
#include <stdio.h>
#include <unistd.h>

// Pin configuration (adjust as necessary)
#define US100_TRIGGER_PIN 0  // WiringPi pin number for the trigger
#define US100_ECHO_PIN 1     // WiringPi pin number for the echo

// Global variables
unsigned long lastMillis = 0;
unsigned long interval = 10000;  // Timer interval in microseconds (10ms)

// Function to handle distance measurement (using US100)
int getDistance() {
    digitalWrite(US100_TRIGGER_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(US100_TRIGGER_PIN, LOW);

    unsigned long duration = pulseIn(US100_ECHO_PIN, HIGH);
    int distance = duration / 58;  // Convert time to distance in mm
    return distance;
}

// Timer handler function to simulate ISR behavior
void timerHandler() {
    unsigned long currentMillis = millis();

    if (currentMillis - lastMillis >= interval) {
        lastMillis = currentMillis;

        // Run ISR for distance measurement
        int dist = getDistance();
        printf("Distance: %d mm\n", dist);
    }
}

int main() {
    // Initialize WiringPi
    if (wiringPiSetup() == -1) {
        printf("WiringPi setup failed\n");
        return -1;
    }

    // Set up pins
    pinMode(US100_TRIGGER_PIN, OUTPUT);
    pinMode(US100_ECHO_PIN, INPUT);

    // Set up a timer to call timerHandler() every 10ms
    while (1) {
        timerHandler();
        delay(1);  // 1ms delay to avoid busy-waiting and overloading the CPU
    }

    return 0;
}
