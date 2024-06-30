#include <Adafruit_Sensor.h>
#include <DHT.h>
#include <DHT_U.h>

#define DHTPIN 2    // Pin connected to the DHT11 sensor
#define FAN_PIN_1 3 // Pin connected to the first fan
#define FAN_PIN_2 4 // Pin connected to the second fan
#define FAN_PIN_3 5 // Pin connected to the third fan
#define FAN_PIN_4 6 // Pin connected to the fourth fan
#define FAN_PIN_5 7 // Pin connected to the fifth fan
#define RED_LED_PIN 8
#define GREEN_LED_PIN 9
#define WHITE_LED_PIN 10

DHT_Unified dht(DHTPIN, DHT11);

bool fan1Status;
bool fan2Status;
bool fan3Status;
bool fan4Status;
bool fan5Status;
bool manualControl;
bool manualFanStatus;
float temperature;

void setup() {
  pinMode(FAN_PIN_1, OUTPUT);
  pinMode(FAN_PIN_2, OUTPUT);
  pinMode(FAN_PIN_3, OUTPUT);
  pinMode(FAN_PIN_4, OUTPUT);
  pinMode(FAN_PIN_5, OUTPUT);
  pinMode(RED_LED_PIN, OUTPUT);
  pinMode(GREEN_LED_PIN, OUTPUT);
  pinMode(WHITE_LED_PIN, OUTPUT);
  Serial.begin(9600);
  dht.begin();

  digitalWrite(RED_LED_PIN, HIGH);
  digitalWrite(GREEN_LED_PIN, LOW);   // Turn off the green LED initially
  digitalWrite(WHITE_LED_PIN, LOW);   // Turn off the white LED initially
}

void loop() {
  if (manualControl) {
    digitalWrite(FAN_PIN_1, manualFanStatus);
    digitalWrite(FAN_PIN_2, manualFanStatus);
    digitalWrite(FAN_PIN_3, manualFanStatus);
    digitalWrite(FAN_PIN_4, manualFanStatus);
    digitalWrite(FAN_PIN_5, manualFanStatus);
    digitalWrite(GREEN_LED_PIN, LOW);   
    digitalWrite(WHITE_LED_PIN, HIGH);

    fan1Status = manualFanStatus;
    fan2Status = manualFanStatus;
    fan3Status = manualFanStatus;
    fan4Status = manualFanStatus;
    fan5Status = manualFanStatus;

      sensors_event_t event;
      dht.temperature().getEvent(&event);
      float temperature = event.temperature;

      Serial.print("Temperature: ");
      Serial.print(temperature);
      Serial.println("°C");

      Serial.print(digitalRead(FAN_PIN_1));
      Serial.print(",");
      Serial.print(digitalRead(FAN_PIN_2));
      Serial.print(",");
      Serial.print(digitalRead(FAN_PIN_3));
      Serial.print(",");
      Serial.print(digitalRead(FAN_PIN_4));
      Serial.print(",");
      Serial.println(digitalRead(FAN_PIN_5));
      
  } else {
    sensors_event_t event;
    dht.temperature().getEvent(&event);
    if (!isnan(event.temperature)) {
      float temperature = event.temperature;

      if (temperature < 30) {
        digitalWrite(FAN_PIN_1, LOW);
        digitalWrite(FAN_PIN_2, LOW);
        digitalWrite(FAN_PIN_3, LOW);
        digitalWrite(FAN_PIN_4, LOW);
        digitalWrite(FAN_PIN_5, LOW);
        digitalWrite(GREEN_LED_PIN, HIGH);   
        digitalWrite(WHITE_LED_PIN, LOW);


        fan1Status = HIGH;
        fan2Status = HIGH;
        fan3Status = HIGH;
        fan4Status = HIGH;
        fan5Status = HIGH;

      } else if (temperature > 30 && temperature < 35) {
        digitalWrite(FAN_PIN_1, LOW);
        digitalWrite(FAN_PIN_2, LOW);
        digitalWrite(FAN_PIN_3, HIGH);
        digitalWrite(FAN_PIN_4, LOW);
        digitalWrite(FAN_PIN_5, LOW);
        digitalWrite(GREEN_LED_PIN, HIGH);   
        digitalWrite(WHITE_LED_PIN, LOW);

        fan1Status = HIGH;
        fan2Status = HIGH;
        fan3Status = LOW;
        fan4Status = HIGH;
        fan5Status = HIGH;

      } else if (temperature >= 35 && temperature < 40) {
        digitalWrite(FAN_PIN_1, HIGH);
        digitalWrite(FAN_PIN_2, LOW);
        digitalWrite(FAN_PIN_3, HIGH);
        digitalWrite(FAN_PIN_4, LOW);
        digitalWrite(FAN_PIN_5, HIGH);
        digitalWrite(GREEN_LED_PIN, HIGH);   
        digitalWrite(WHITE_LED_PIN, LOW);
        
        fan1Status = LOW;
        fan2Status = HIGH;
        fan3Status = LOW;
        fan4Status = HIGH;
        fan5Status = LOW;

      } else {
        digitalWrite(FAN_PIN_1, HIGH);
        digitalWrite(FAN_PIN_2, HIGH);
        digitalWrite(FAN_PIN_3, HIGH);
        digitalWrite(FAN_PIN_4, HIGH);
        digitalWrite(FAN_PIN_5, HIGH);
        digitalWrite(GREEN_LED_PIN, HIGH);   
        digitalWrite(WHITE_LED_PIN, LOW);
        
        fan1Status = LOW;
        fan2Status = LOW;
        fan3Status = LOW;
        fan4Status = LOW;
        fan5Status = LOW;
        
      }

      Serial.print("Temperature: ");
      Serial.print(temperature);
      Serial.println("°C");

      Serial.print(digitalRead(fan1Status));
      Serial.print(",");
      Serial.print(digitalRead(fan2Status));
      Serial.print(",");
      Serial.print(digitalRead(fan3Status));
      Serial.print(",");
      Serial.print(digitalRead(fan4Status));
      Serial.print(",");
      Serial.println(digitalRead(fan5Status));
    }
  }
  delay(2000);
}

void serialEvent() {
  while (Serial.available()) {
    char command = Serial.read();

    if (command == 'T') {
      // Switch to temperature sensing mode
      manualControl = false;
    } else if (command == '1') {
      // Turn on fans (manual control mode)
      manualControl = true;
      manualFanStatus = 1;
    } else if (command == '0') {
      // Turn off fans (manual control mode)
      manualControl = true;
      manualFanStatus = 0;
    }
  }
}
