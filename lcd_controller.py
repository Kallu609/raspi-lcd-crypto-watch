from Adafruit_CharLCD import Adafruit_CharLCD


class LCDController(Adafruit_CharLCD):
    def __init__(self):
        self.pin_rs = 25
        self.pin_en = 24
        self.pin_d4 = 23
        self.pin_d5 = 18
        self.pin_d6 = 15
        self.pin_d7 = 14

        self.lcd_columns = 16
        self.lcd_rows    = 2

        init_args = (self.pin_rs, self.pin_en, self.pin_d4, self.pin_d5, self.pin_d6, self.pin_d7, self.lcd_columns, self.lcd_rows, )
        super(LCDController, self).__init__(*init_args)