from RPi import GPIO

PINS = {
    'rgb1': (17, 18, 22,),
    'rgb2': (23, 24, 25,),
    'row': (7, 8, 9),
    'clock': 3,
    'latch': 4,
    'oe': 2,
}


class LEDMatrix(object):
    def __init__(self, size):
        self.size = size

    def reset_colors(self):
        """Reset the internal memory of the colours"""
        self.colors = [
            [(False, False, False,) for _ in range(self.size[0])]
            for _ in range(self.size[1])
        ]

    def get_color(self, x, y):
        """Get the rgb boolean values at (x, y)"""
        return self.colors[y][x]

    def set_color(self, x, y, color):
        # verify color tuple
        if not isinstance(color, tuple) or len(color) != 3:
            raise ValueError("`color` must be a tuple of length 3")
        for b in color:
            if not isinstance(b, bool):
                raise ValueError("`color may only contain booleans")

        self.colors[y][x] = color


class GPIOLEDMatrix(LEDMatrix):
    TUP_KEYS = ['rgb1', 'rgb2', 'row']
    PIN_KEYS = ['clock', 'latch', 'oe']

    def __init__(self, pins, *args, **kwargs):
        super(GPIOLEDMatrix, self).__init__(*args, **kwargs)
        self.pins = pins
        self.init_pins()

    def init_pins(self):
        """Initialise the GPIO pins to be used for LED matrix control"""
        GPIO.cleanup()
        GPIO.setmode(GPIO.BCM)

        for tup_key in self.TUP_KEYS:
            for pin in self.pins[tup_key]:
                GPIO.setup(pin, GPIO.OUT)
        for pin_key in self.PIN_KEYS:
            GPIO.setup(self.pins[pin_key], GPIO.OUT)

    def clock(self, ):
        GPIO.output(self.pins['clock'], 1)
        GPIO.output(self.pins['clock'], 0)

    def latch(self, ):
        GPIO.output(self.pins['latch'], 1)
        GPIO.output(self.pins['latch'], 0)

    def bits_from_int(self, x):
        a_bit = x & 1
        b_bit = x & 2
        c_bit = x & 4
        return (a_bit, b_bit, c_bit)

    def set_row(self, row):
        for pin, value in zip(self.pins['row'], self.bits_from_int(row)):
            GPIO.output(pin, value)

    def draw_color(self, color, pins='rgb1'):
        for pin, value in zip(self.pins[pins], color):
            GPIO.output(pin, value)

    def set_oe(self, oe):
        """Disable all LEDs"""
        GPIO.output(self.pins['oe'], oe)

    def draw(self):
        "THIS CODE IS BROKEN"
        for row in range(8):
            self.set_oe(True)
            set_color_top(0)
            set_row(row)
            # time.sleep(delay)
            for col in range(32):
                set_color_top(screen[row][col])
                set_color_bottom(screen[row+8][col])
                clock()
            # GPIO.output(oe_pin, 0)
            latch()
            GPIO.output(oe_pin, 0)
            time.sleep(delay)
