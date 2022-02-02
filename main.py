from clock import Clock  # imports the clock class
import lcddriver
import os

lcd = lcddriver.lcd()
lcd.lcd_clear()
program = 0  # sets program to 0 for infinite loop creation
display = lcddriver.lcd()


def main():
    print(Clock.time())
    lcd.lcd_clear()
    lcd.lcd_display_string(Clock.time() + " " + Clock.date(), 1)
    os.system("sudo airmon-ng start wlan0")
    os.system("kismet -c wlan0mon")


if __name__ == '__main__':
    main()
