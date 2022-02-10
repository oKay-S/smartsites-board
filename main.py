import re
import time

import hashlib
import pcapy
import subprocess
import websockets
import asyncio

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

HOST = 'smartsites.kieransoutter.com'  # The server's hostname or IP address
PORT = 443  # The port used by the server

mac_match = re.compile("[A-Za-z0-9]{2}:[A-Za-z0-9]{2}:[A-Za-z0-9]{2}:[A-Za-z0-9]{2}:[A-Za-z0-9]{2}:[A-Za-z0-9]{2}",
                       flags=re.I)

async def socket(msg):
    async with websockets.connect("wss://smartsites.kieransoutter.com") as websocket:
        print("socket opened")
        await websocket.send("bkjsafey834tw." + msg)
        await websocket.recv()
        print("socket closed")

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
        print("5 minutes pass!")
        length = len(packets)
        lengthstr = str(length)
        lcd.lcd_display_string("Devices: " + lengthstr, 2)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(socket(lengthstr))

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
            try:
                msg = "0"
                loop = asyncio.get_event_loop()
                loop.run_until_complete(socket(msg))
                lcd.lcd_clear()
                lcd.lcd_display_string("Socket", 1)
                lcd.lcd_display_string("Tested", 2)
                try:
                    p.loop(-1, addpackets)
                except:
                    lcd.lcd_clear()
                    lcd.lcd_display_string("Loop", 1)
                    lcd.lcd_display_string("failed", 2)
            except Exception as err:
                lcd.lcd_clear()
                lcd.lcd_display_string("Socket", 1)
                lcd.lcd_display_string("failed", 2)
                print(err)
        except:
            lcd.lcd_clear()
            lcd.lcd_display_string("Scanning", 1)
            lcd.lcd_display_string("failed", 2)
    except:
        lcd.lcd_clear()
        lcd.lcd_display_string("Scanner", 1)
        lcd.lcd_display_string("failed ", 2)


if __name__ == '__main__':
    main()
