from Flowerpot_Engine import *
from noaa_engine import get_noaa_data
from thingsboard_engine import *
import time


def main():

    print("Starting Flowerpot System...")

    # Loop forever
    i = 1
    while True:

        # Read sensor values
        soil = read_SoilMoisture()
        light = read_Light()
        waterLevel = read_WaterLevel()
        temp, hum = read_TempHum()

        # Get NOAA data
        noaa = get_noaa_data()

        # Data 
        data_out = {
            "Packet": i,
            "SoilMoisture": soil,
            "Light": light,
            "WaterLevel": 1 if waterLevel == "full" else 0,
            "Temperature": temp,
            "Humidity": hum,
            "NoaaTemp": noaa["temp"],
            "Precipitation": noaa["prec"],
            "SunPct": noaa["sunpct"]
        }

        print("data_out=", data_out)

        # Send data to ThingsBoard
        send_data(data_out)

        print('---------------------------')

        i = i + 1
        time.sleep(5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        disconnect_tb()
        GPIO.cleanup()
        print('\nBye...')
    except Exception as e:
        disconnect_tb()
        GPIO.cleanup()
        print(f"\nAn error occurred: {e}")