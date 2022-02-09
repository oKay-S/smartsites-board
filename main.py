import re
import time

import hashlib
import pcapy
import subprocess

from scan import Scan  # imports the scan class
import lcddriver

scan = Scan()

lcd = lcddriver.lcd()
lcd.lcd_clear()
program = 0  # sets program to 0 for infinite loop creation
display = lcddriver.lcd()
packets = []
router_list = []
lastprinttime = time.time()

mac_match = re.compile("[A-Za-z0-9]{2}:[A-Za-z0-9]{2}:[A-Za-z0-9]{2}:[A-Za-z0-9]{2}:[A-Za-z0-9]{2}:[A-Za-z0-9]{2}",
                       flags=re.I)


def addpackets(header, data):
    global lastprinttime
    global packets
    global router_list

    packet = scan.packet_handler(header, data)

    try:
        routers = subprocess.check_output("sudo iwlist wlan0 scan | grep 'Address'", shell=True)
        routers_str = str(routers)
        routers_str_upper = routers_str.upper()  # although currently the command returns in uppercase, it may not in future iterations of the command
        routers_regexed = mac_match.findall(routers_str_upper)
        for i in routers_regexed:
            routers_hashed = hashlib.sha512(i.encode("utf-8")).hexdigest()
            if routers_hashed not in router_list:
                router_list.append(routers_hashed)
    except:
        print("scan failed")

    if packet is not None:
        for address in packet:
            if address not in packets:
                if address not in router_list:
                    packets.append(address)
                    lcd.lcd_display_string("                     ",
                                           1)  # Horrible way of doing this however there is no driver support for clearing just one line
                    lcd.lcd_display_string("Device Found", 1)
                else:
                    lcd.lcd_display_string("                     ",
                                           1)  # see previous comment
                    lcd.lcd_display_string("Router Found", 1)

    else:
        lcd.lcd_display_string("                     ",
                               1)  # see previous comment
        lcd.lcd_display_string("Improper Packet", 1)

    if (lastprinttime + 300) < time.time():
        lastprinttime = time.time()
        lcd.lcd_clear()
        print("a minute passes!")
        length = len(packets)
        lengthstr = str(length)
        lcd.lcd_display_string("Number of", 1)
        lcd.lcd_display_string("Devices: " + lengthstr, 2)
        time.sleep(1)

        print(packets)
        packets = []


def main():
    lcd.lcd_clear()
    lcd.lcd_display_string("System", 1)
    lcd.lcd_display_string("ok ", 2)
    time.sleep(1)
    try:
        p = pcapy.open_live("wlan1mon", 2000, 0, 1000)
        lcd.lcd_clear()
        lcd.lcd_display_string("Scanner", 1)
        lcd.lcd_display_string("ok", 2)
        time.sleep(1)
        try:
            lcd.lcd_clear()
            lcd.lcd_display_string("Scanning", 1)
            lcd.lcd_display_string("Active", 2)
            p.loop(-1, addpackets)
        except:
            lcd.lcd_clear()
            lcd.lcd_display_string("Scanning", 1)
            lcd.lcd_display_string("failed", 2)
    except:
        lcd.lcd_clear()
        lcd.lcd_display_string("Scanner", 1)
        lcd.lcd_display_string("Failed ", 2)


if __name__ == '__main__':
    main()
