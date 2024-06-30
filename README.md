# Automated-Fan-Controlling-System
Automated Fan Controlling using a Basic SCADA System is a project aimed at implementing a temperature-based fan control system with a graphical user interface (GUI) developed using Python for easy interaction and monitoring. The system utilizes an Arduino Mega microcontroller to collect temperature data from a DHT11 sensor and control the status of five fans based on the temperature readings. The system also includes a manual control mode, allowing users to manually turn the fans on or off. Additionally, the system incorporates LED indicators to provide visual feedback on the system's operating mode.

## Features
1. Automatic Temperature Control: The system automatically adjusts fan status based on temperature readings from the DHT11 sensor.
2. Manual Control Mode: Users can manually control the fans using the GUI.
3. Real-time Temperature Monitoring: The GUI displays real-time temperature data and a live graph showing temperature variations over time.
4. LED Indicators: Visual feedback with LED indicators showing the system's operating mode.

## Components
1. Arduino Mega: Microcontroller to process temperature data and control fan status.
2. DHT11 Sensor: Sensor to measure temperature.
3. Fans: Five fans controlled based on temperature readings.
4. LED Indicators:
   - Red LED: Indicates the system is running.
   - Green LED: Activated in temperature-controlled mode.
   - White LED: Activated in manual control mode.
5. Python GUI: Graphical User Interface for user interaction and monitoring.

## Hardware Setup

### Components
* Arduino Mega
* DHT11 Sensor
* Five fans
* Three LEDs (Red, Green, White)
* Breadboard and jumper wires

### Circuit Diagram
Instructions
* Connect the DHT11 sensor to the Arduino Mega as per the circuit diagram.
* Connect the LEDs to the Arduino Mega, ensuring they are properly wired to indicate the operating modes.
* Connect the fans to the Arduino Mega for temperature-based and manual control.

## Software Setup

### Arduino Code
The Arduino code (Arduino_Code.ino) is responsible for reading the temperature data from the DHT11 sensor and controlling the fans and LEDs.

### Python GUI
The Python GUI (Python_GUI.py) provides an interface for monitoring temperature and controlling the fans. It displays real-time temperature data and allows switching between automatic and manual control modes.

