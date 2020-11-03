import explorerhat
import sqlite3
import time
from config import DATABASE_LOGIN, WATERING_TIME, DRYNESS_THRESHOLD

def read_water():
    TEMPLATE = '''INSERT INTO schedule(date, voltage) VALUES(datetime('now'), ?)'''
    voltage = explorerhat.analog.one.read()

    with sqlite3.connect(DATABASE_LOGIN) as connection:
        cursor = connection.cursor()
        cursor.execute(TEMPLATE, (voltage,))

    return voltage

def water_plant(water_time : int = 10):
    explorerhat.light[0].on()
    explorerhat.motor.one.forwards(100)
    
    time.sleep(water_time)
    
    explorerhat.motor.one.stop()
    explorerhat.light[0].off()

    TEMPLATE = '''INSERT INTO watered_schedule VALUES(datetime('now'))'''
    with sqlite3.connect(DATABASE_LOGIN) as connection:
        cursor = connection.cursor()
        cursor.execute(TEMPLATE)

if __name__ == '__main__':
    voltage = read_water()

    print("Voltage: {}".format(voltage))

    if voltage < DRYNESS_THRESHOLD:
        if voltage < 0.01:
            print("ERROR: Sensor not working")
        else:
            print("Watering Plant")
            water_plant(WATERING_TIME)
