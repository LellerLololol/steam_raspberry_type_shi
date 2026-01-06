#include "US100.h"
#include "TimerInterrupt_Generic.h"
#include "ISR_Timer_Generic.h"

MBED_RPI_PICO_Timer ITimer(0);///for pico
ISR_Timer ISR_timer;

static const unsigned long HARDWARE_TIMER_INTERVAL_US = 10000UL;///for pico

void timerHandler(uint alarm_num){

  TIMER_ISR_START(alarm_num);///for pico

  ISR_timer.run();

  TIMER_ISR_END(alarm_num);///for pico
}

void setup() {

  Serial.begin(9600);

  us100.setup();

  if (ITimer.attachInterruptInterval(HARDWARE_TIMER_INTERVAL_US, timerHandler))///for pico
  {
    Serial.print(F("Starting  ITimer, millis() = ")); 
    Serial.println(millis());
  }
  else{
    Serial.println(F("Can't set ITimer. Select another frequency or a timer"));
  }

  ISR_timer.setInterval(US100::TIMER_INTERVAL_MS, US100::ISR_timerHandler, &us100);

}


void loop_cycle() {

  int dist = us100.getDistance();
  Serial.print("Distance: ");
  Serial.print(dist);
  Serial.println("mm");

  delay(100);

}
