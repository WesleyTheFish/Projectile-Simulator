import board
import digitalio
import time
import adafruit_gps
from adafruit_servokit import ServoKit
import feathers2
import adafruit_bno055
import busio


i2c = board.I2C()

# initilize Servos
kit = ServoKit(channels=8)
servo5 = kit.servo[0]

# initilize IMU
sensor = adafruit_bno055.BNO055_I2C(i2c)



servo_angle =0
count = 0
mod = 0

def setup_gps():
    """ Initialize GPS """

    uart = busio.UART(board.TX, board.RX, baudrate=9600, timeout=10)
    gps = adafruit_gps.GPS(uart, debug=False)

    # Turn on the basic GGA and RMC info (what you typically want)
    gps.send_command(b"PMTK314,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0")
    # Turn on just minimum info (RMC only, location):
    # gps.send_command(b'PMTK314,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
    # Turn off everything:
    # gps.send_command(b'PMTK314,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0')
    # Turn on everything (not all of it is parsed!)
    # gps.send_command(b'PMTK314,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0')

    # Set update rate to once a second (1hz) which is what you typically want.
    gps.send_command(b"PMTK220,200")
    # Or decrease to once every two seconds by doubling the millisecond value.
    # Be sure to also increase your UART timeout above!
    # gps.send_command(b'PMTK220,2000')
    # You can also speed up the rate, but don't go too fast or else you can lose
    # data during parsing.  This would be twice a second (2hz, 500ms delay):
    # gps.send_command(b'PMTK220,500')

    return gps

def gps_loop(gps, debug=False):
    count = 0
    # Main loop runs forever printing the location, etc. every second.
    last_print = time.monotonic()
    while True:
        # Make sure to call gps.update() every loop iteration and at least twice
        # as fast as data comes from the GPS unit (usually every second).
        # This returns a bool that's true if it parsed new data (you can ignore it
        # though if you don't care and instead look at the has_fix property).
        gps.update()
        # Every second print out current location details if there's a fix.
        current = time.monotonic()
        if current - last_print >= 1:
            count+=1
            last_print = current
            if not gps.has_fix:
                # Try again if we don't have a fix yet.
                print("Waiting for fix...")
                continue
            # We have a fix! (gps.has_fix is true)
            # Print out details about the fix like location, date, etc.
            if debug:
                print("=" * 40)  # Print a separator line.
                print(
                    "Fix timestamp: {}/{}/{} {:02}:{:02}:{:02}".format(
                        gps.timestamp_utc.tm_mon,
                        gps.timestamp_utc.tm_mday,
                        gps.timestamp_utc.tm_year,
                        gps.timestamp_utc.tm_hour,
                        gps.timestamp_utc.tm_min,
                        gps.timestamp_utc.tm_sec,
                    )
                )

                print(
                    "Precise Latitude: {:2.}{:2.4f} degrees".format(
                        gps.latitude_degrees, gps.latitude_minutes
                    )
                )
                print(
                    "Precise Longitude: {:2.}{:2.4f} degrees".format(
                        gps.longitude_degrees, gps.longitude_minutes
                    )
                )
                print("Fix quality: {}".format(gps.fix_quality))
                # Some attributes beyond latitude, longitude and timestamp are optional
                # and might not be present.  Check if they're None before trying to use!
                if gps.satellites is not None:
                    print("# satellites: {}".format(gps.satellites))
                if gps.altitude_m is not None:
                    print("Altitude: {} meters".format(gps.altitude_m))
                if gps.speed_knots is not None:
                    print("Speed: {} knots".format(gps.speed_knots))
                if gps.track_angle_deg is not None:
                    print("Track angle: {} degrees".format(gps.track_angle_deg))
                if gps.horizontal_dilution is not None:
                    print("Horizontal dilution: {}".format(gps.horizontal_dilution))
                if gps.height_geoid is not None:
                    print("Height geoid: {} meters".format(gps.height_geoid))

            print(f"Lat/Long:  {gps.latitude_degrees:.6f} {gps.longitude:.6f}  Alt={gps.altitude_m} {count}")
            print("Precise Latitude: {:2.}{:2.4f} degrees".format(gps.latitude_degrees, gps.latitude_minutes))

def find_offset():
    a_sum = [0,0,0]
    for _ in range(1000):
        a_sum = [a+s for s,a in zip(a_sum, sensor.linear_acceleration)]
        print(a_sum)

    offset = [v/1000.0 for v in a_sum]
    return offset

def imu_call():
    pos = [0,0,0]
    vel = [0,0,0]
    acc = [0,0,0]
    time_step = 0.1

    # IMU control
    ts = .1
    while 1:
        t1 = time.time()
        acc = [a - e for a,e in zip(sensor.linear_acceleration, [-0.110923, 0.00671985, -0.377355])]
        for i in range(3):
            vel[i] += acc[i] * time_step
            pos[i] += vel[i] * time_step
        print(f"{pos[0]:+0.3f} {pos[1]:+0.3f} {pos[2]:+0.3f} {acc[0]:+0.3f} {acc[1]:+0.3f} {acc[2]:+0.3f}")
        time.sleep(time_step)
        ts = time.time()-t1


def servo_call():
    #Servo control
    mod = count % 360
    if(mod<180):
        servo_angle = mod
    else:
        servo_angle=180-(mod % 180)
    kit.servo[4].angle = servo_angle
    count +=1
    feathers2.led_set(count%2)

#print(find_offset())
#imu_call()
gps = setup_gps()
gps_loop(gps)
