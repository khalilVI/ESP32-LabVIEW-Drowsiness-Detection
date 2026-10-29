# ESP32 & LabVIEW Drowsiness Detection

Driver drowsiness detection system integrating an ESP32 MicroPython simulation with a LabVIEW backend for MPU6050 gyroscope data processing.

## 🛠️ System Architecture
* **Embedded Hardware Simulation:** ESP32 via Wokwi (`diagram.json`, `wokwi-project.txt`)
* **Sensor Integration:** MPU6050 (Accelerometer & Gyroscope) via I2C
* **Microcontroller Logic:** MicroPython (`main.py`)
* **Data Processing & GUI:** LabVIEW (`sensor mdl.vi`)

## 🧠 LabVIEW Detection Logic
![LabVIEW Block Diagram](Screenshot%202025-11-06%20213640.png)
