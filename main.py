from clock import Clock  # imports the clock class
from scan import Scan   # imports the scan class
import lcddriver

lcd = lcddriver.lcd()
lcd.lcd_clear()
program = 0  # sets program to 0 for infinite loop creation
display = lcddriver.lcd()


def main():
    print(Clock.time())
    lcd.lcd_clear()
    lcd.lcd_display_string(Clock.time() + " " + Clock.date(), 1)
    Scan.setup()



if __name__ == '__main__':
    main()
