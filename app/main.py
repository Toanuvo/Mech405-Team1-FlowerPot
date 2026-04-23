import datetime
from Flowerpot_Engine import *
from noaa_engine import get_noaa_data
from thingsboard_engine import *
import time


def adjust_pot(humidity, lightpct, sunpct, soil_moisture, precipitation, temperature, has_water, rotation):
    pump_duration = 0.5
    if humidity < 60:
        pump_duration += 0.2
    if sunpct >= 50:
        pump_duration += 0.2
    if precipitation >= 40:
        pump_duration -= 0.2
    if temperature >= 75:
        pump_duration += 0.2
        
    now = datetime.datetime.now().time() # get current hour
    
    is_morning = datetime.time(7) < now <= datetime.time(8)
    is_evening = datetime.time(18) < now <= datetime.time(19)
    
    need_water = soil_moisture < 40 or not has_water
    
    print(f"pump duration: {pump_duration}")
    if (is_morning or is_evening) and need_water:
        pump_ON()
        time.sleep(pump_duration)
        pump_OFF()
        
        
    is_day = datetime.time(7) < now <= datetime.time(19)
    
    # sunny day so rotate plant during day
    if is_day and (sunpct >= 50 or (lightpct >= 20)):
        if is_morning:
            # move plant to one side
            while not read_RightLim():
                motor.rotate(1, 'CCW', 's', 'full')
            rotation = -90
         
        for i in range(15):
            if read_LeftLim():
                break
            motor.rotate(1, 'CW', 's', 'full')
            rotation += 1
            
        
        
    
    return pump_duration, rotation

def main():

    print("Starting Flowerpot System...")
    home_base()
    rotation = 0 # 0 = home, -CCW, +CW

    # Loop forever
    i = 1
    while True:

        # Read sensor values
        soil = read_SoilMoisture()
        light = read_Light()
        waterLevel = 1 if read_WaterLevel() == "full" else 0
        temp, hum = read_TempHum()

        # Get NOAA data
        dayTemp, prec, sunpct = get_noaa_data()
        
        pump_duration, rotation = adjust_pot(hum,light,sunpct, soil, prec, temp, waterLevel, rotation)

        # Data 
        data_out = {
            "Packet": i,
            "SoilMoisture": soil,
            "Light": light,
            "WaterLevel": waterLevel,
            "Temperature": temp,
            "Humidity": hum,
            "NoaaTemp": dayTemp,
            "Precipitation": prec,
            "SunPct": sunpct
        }

        print("data_out=", data_out)

        # Send data to ThingsBoard
        send_data(data_out)
        
        with open("log.csv", "+a") as csv:
            if csv.tell() == 0: # add csv header if file is empty
                csv.write("date,temp,humidity,rotation,soilMoisture,light,waterLevel,dayTemp,precipitation,sunpct,pumpDuration\n")
            csv.write(f"{datetime.datetime.now()},{temp},{hum},{rotation},{soil},{light},{waterLevel},{dayTemp},{prec},{sunpct},{pump_duration}\n")

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




    
