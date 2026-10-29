# ===== MPU6050 DRIVER CODE (included here) =====
from machine import Pin, I2C
from time import sleep, ticks_ms

class MPU6050:
    def __init__(self, i2c, addr=0x68):
        self.i2c = i2c
        self.addr = addr
        # Wake up the MPU6050
        self.i2c.writeto_mem(self.addr, 0x6B, bytes([0]))

    def read_raw_data(self, reg):
        data = self.i2c.readfrom_mem(self.addr, reg, 2)
        value = (data[0] << 8) | data[1]
        if value > 32768:
            value -= 65536
        return value

    def get_gyro_data(self):
        gx = self.read_raw_data(0x43) / 131.0
        gy = self.read_raw_data(0x45) / 131.0
        gz = self.read_raw_data(0x47) / 131.0
        return {'x': gx, 'y': gy, 'z': gz}


# ===== MAIN PROGRAM STARTS HERE =====
# LED pins
redLED = Pin(18, Pin.OUT)
greenLED = Pin(19, Pin.OUT)

# I2C setup for ESP32
i2c = I2C(0, scl=Pin(22), sda=Pin(21))
mpu = MPU6050(i2c)

# Thresholds and timing
drowsyThresholdX = 20.0
drowsyThresholdZ = 20.0
stillDelay = 20000  # 20 seconds in ms

# State variables
stillStartTime = 0
isDrowsy = False
lastCountdown = 0

print("Initializing MPU6050...")
sleep(1)
print("System ready. Monitoring driver activity...")

while True:
    gyro = mpu.get_gyro_data()
    rotX = gyro['x']
    rotZ = gyro['z']

    isStill = (abs(rotX) < drowsyThresholdX and abs(rotZ) < drowsyThresholdZ)
    now = ticks_ms()

    if isStill:
        if stillStartTime == 0:
            stillStartTime = now
            print("Driver is sitting still... starting 20s countdown.")
            lastCountdown = 20

        elapsed = now - stillStartTime
        remaining = int((stillDelay - elapsed) / 1000)

        if remaining < lastCountdown and remaining > 0:
            print(f"Driver still... {remaining}s remaining before drowsiness alert.")
            lastCountdown = remaining

        if elapsed >= stillDelay:
            if not isDrowsy:
                print("⚠️  DRIVING ALERT: Drowsiness detected!")
            redLED.value(1)
            greenLED.value(0)
            isDrowsy = True

    else:
        if stillStartTime != 0:
            print("Movement detected — driver is awake.")
        stillStartTime = 0
        isDrowsy = False
        redLED.value(0)
        greenLED.value(1)

    sleep(0.5)
