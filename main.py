import os
import time

import pcapy

from clock import Clock  # imports the clock class
from scan import Scan   # imports the scan class
import lcddriver

scan = Scan()

lcd = lcddriver.lcd()
lcd.lcd_clear()
program = 0  # sets program to 0 for infinite loop creation
display = lcddriver.lcd()
packets = []
lastprinttime = time.time()


def addpackets(header, data):

    global lastprinttime
    global packets

    packet = scan.packet_handler(header, data)
    if packet is not None:
        if packet not in packets:
            packets.append(packet)

    if (lastprinttime + 60) < time.time():
        lastprinttime = time.time()
        os.system("clear")
        print("a minute passes!")
        length = len(packets)
        print(str(length))
        print(packets)
        packets = []

def main():
    print(Clock.time())
    lcd.lcd_clear()
    lcd.lcd_display_string(Clock.time() + " " + Clock.date(), 1)
    p = pcapy.open_live("wlan1mon", 2000, 0, 1000)
    p.loop(-1, addpackets)





if __name__ == '__main__':
    main()
