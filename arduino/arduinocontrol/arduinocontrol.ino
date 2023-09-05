#include <Servo.h>

// #define CALIBRATION_BOARD // uncomment this line if you are using the calibration pins
#define RPM_SENSOR // uncomment if you want to compile with the RPM_SENSOR
// #define ENABLE_BRAKES // uncomment if you want to use the brakes

// Servo
#define SERVO_PIN 6
#define SERVO_MIN 900
#define SERVO_MAX 2100
#define SERVO_NEUTRAL 1500
#define SERVO_DEADBAND 2
Servo servoSteering;

// Motor
#define ESC_PIN 5
#define ESC_MIN 1000
#define ESC_MAX 2000
#define ESC_NEUTRAL 1500
#define ESC_DEADBAND 100
Servo motorESC;

#ifdef RPM_SENSOR

// Sensor for RPM
#define SENSOR_INT_PIN 1
#define SENSOR_DIGITAL_PIN 3

#endif

#define BUFF_LENGTH 5
// variables used to read serial
byte dummyBuff[1] = {0};
// {start, steering, throttle, end}
byte buffData[BUFF_LENGTH] = {0, 0, 0, 0, 0};
bool reverseMode = false;

byte expected_start = 255;
byte expected_end = 0;

// variables to detect last received serial message (safety)
long last_received = 0;
int maxTimout = 500;

// variables to read PWM pulses
unsigned long timer_start = 0;
unsigned long last_interrupt_time = 0;
long motor_speed = 0;
long prev_motor_speed = 0;

void setup()
{
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);

  Serial.begin(115200);
  Serial.setTimeout(200);

  // servo init
  servoSteering.attach(SERVO_PIN, SERVO_MIN, SERVO_MAX);
  servoSteering.writeMicroseconds(SERVO_NEUTRAL);

  // motor init
  motorESC.attach(ESC_PIN, ESC_MIN, ESC_MAX);
  motorESC.writeMicroseconds(ESC_NEUTRAL);

#ifdef RPM_SENSOR
  // pinMode(SENSOR_INT_PIN, INPUT);
  attachInterrupt(SENSOR_INT_PIN, signalChange, CHANGE);
#endif

#ifdef CALIBRATION_BOARD
  // debugging board init
#define BUTTON_PIN 16
#define LED_PIN 15

  pinMode(BUTTON_PIN, INPUT);
  pinMode(LED_PIN, OUTPUT);

  // if the button is pressed within a second, enter calibration process
  for (int i = 0; i < 20; i++)
  {
    delay(50);
    if (digitalRead(BUTTON_PIN))
    {
      blinkLED(1);
      waitButtonReleased(); // calibrate ESC
      calibrationSteps();
      break;
    }
  }
  blinkLED(1);
#endif
}

void loop()
{

  // write rpm sensor data to the serial
  if (Serial && motor_speed != prev_motor_speed)
  {
    prev_motor_speed = motor_speed;
    Serial.println(prev_motor_speed);
  }

  if (Serial.available())
  {
    // read the data from the serial
    Serial.readBytes(buffData, BUFF_LENGTH);

    if (buffData[0] == expected_start && buffData[BUFF_LENGTH - 1] == expected_end) // check wether we are reading the right data buffer
    {
      last_received = millis();
      changeSteering();
      changeThrottle();
    }
    else
    {
      Serial.readBytes(dummyBuff, 1); // needed to adjust start and end of the message
    }
  }

  // if the arduino isn't receiving anything for a given amount of time, stop the motor and servo
  else if (millis() - last_received > maxTimout)
  {
    servoSteering.writeMicroseconds(SERVO_NEUTRAL);
    motorESC.writeMicroseconds(ESC_NEUTRAL);
  }
}

void changeSteering()
{
  float decoded_steering = buffData[1];

  int steering = SERVO_MAX - decoded_steering / 255 * (SERVO_MAX - SERVO_MIN);
  servoSteering.writeMicroseconds(steering);
}

void changeThrottle()
{
  float decoded_trottle = buffData[2];
  float decoded_brake = buffData[3];

  int throttle = ESC_MIN + decoded_trottle / 255 * (ESC_MAX - ESC_MIN);

#ifdef ENABLE_BRAKES
  int brake = ESC_NEUTRAL - decoded_brake / 255 * (ESC_NEUTRAL - ESC_MIN);

  if (brake != ESC_NEUTRAL)
  {
    // go back to brake mode
    if (reverseMode)
    {
      motorESC.writeMicroseconds(ESC_NEUTRAL);
    }
    else
    {
      motorESC.writeMicroseconds(brake);
    }
  }


  else
  {
    // positive throttle
    if (throttle >= ESC_NEUTRAL)
    {
      motorESC.writeMicroseconds(throttle);

      if (reverseMode)
      {
        reverseMode = false;
        digitalWrite(LED_BUILTIN, LOW);
      }
    }
    // reverse
    else if (reverseMode)
    {
      motorESC.writeMicroseconds(throttle);
    }
    // go into reverse mode
    else
    {
      motorESC.writeMicroseconds((ESC_NEUTRAL + ESC_MIN) / 2);
      delay(100);
      motorESC.writeMicroseconds(ESC_NEUTRAL);
      delay(100);
      motorESC.writeMicroseconds(throttle);
      reverseMode = true;
      digitalWrite(LED_BUILTIN, HIGH);
    }
  }
#endif

#ifndef ENABLE_BRAKES
  motorESC.writeMicroseconds(throttle);
#endif

}

#ifdef RPM_SENSOR
void signalChange() // this function will be called on state change of SENSOR_PIN
{
  last_interrupt_time = micros();
  if (digitalRead(SENSOR_DIGITAL_PIN) == HIGH)
  {
    timer_start = last_interrupt_time;
  }
  else
  {
    if (timer_start != 0)
    {
      motor_speed = last_interrupt_time - timer_start;
      timer_start = 0;
    }
  }
}
#endif

#ifdef CALIBRATION_BOARD
void calibrationSteps()
{
  // neutral pwm
  waitButtonClicked();
  blinkLED(1);
  motorESC.writeMicroseconds(ESC_NEUTRAL);

  // max pwm
  waitButtonClicked();
  blinkLED(2);
  motorESC.writeMicroseconds(ESC_MAX);

  // min pwm
  waitButtonClicked();
  blinkLED(3);
  motorESC.writeMicroseconds(ESC_MIN);

  delay(2900); // wait less than 3 seconds and set to neutral point to avoid motor to start at full power
  motorESC.writeMicroseconds(ESC_NEUTRAL);
}

void waitButtonClicked()
{
  waitButtonPressed();
  waitButtonReleased();
}

void waitButtonPressed()
{
  while (!digitalRead(BUT
  TON_PIN))
  { // wait for button to be pressed
    delay(50);
  }
}

void waitButtonReleased()
{
  while (digitalRead(BUTTON_PIN))
  { // wait for button to be released
    delay(50);
  }
}

void blinkLED(int rep)
{
  for (int i = 0; i < rep; i++)
  {
    digitalWrite(LED_PIN, HIGH);
    delay(250);
    digitalWrite(LED_PIN, LOW);
    delay(250);
  }
}
#endif
