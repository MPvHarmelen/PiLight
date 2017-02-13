from RPi import GPIO

DELAY = 0.000001
SIZE = (16, 32)
PINS = {
    'rgb1': (17, 18, 22,),
    'rgb2': (23, 24, 25,),
    'row': (7, 8, 9, 10),
    'clock': 3,
    'latch': 4,
    'oe': 2,
}


class LEDMatrix(object):
    def __init__(self, size):
        self.size = size

    def reset_colors(self, fill=None):
        """Reset the internal memory of the colours"""
        self.colors = [
            [fill for _ in range(self.size[0])]
            for _ in range(self.size[1])
        ]

    def get_color(self, row, column):
        """Get the (r, g, b) boolean values at (row, column)"""
        return self.colors[row][column]

    def set_color(self, row, column, color):
        """Set the (r, g, b) boolean values at (row, column)"""
        self.colors[row][column] = color


class GPIOLEDMatrix(LEDMatrix):
    """
    The LED matrix has a memory per row, with a 3 bit value per LED.
    The state of the LEDs can be set to the state of the memory by calling
    `latch`.
    `set_row` selects which row to control

    """
    TUP_KEYS = ['rgb1', 'rgb2', 'row']
    PIN_KEYS = ['clock', 'latch', 'oe']

    def __init__(self, pins, delay, *args, **kwargs):
        super(GPIOLEDMatrix, self).__init__(*args, **kwargs)
        self.pins = pins
        self.delay = delay
        self.init_pins()
        self.reset_colors((False, False, False,))

    def init_pins(self):
        """Initialise the GPIO pins to be used for LED matrix control"""
        # assume all pins are initialised with 0 values
        self.row = 0
        self.oe = 0
        self.color = (False, False, False)

        GPIO.setmode(GPIO.BCM)

        for tup_key in self.TUP_KEYS:
            for pin in self.pins[tup_key]:
                GPIO.setup(pin, GPIO.OUT)
        for pin_key in self.PIN_KEYS:
            GPIO.setup(self.pins[pin_key], GPIO.OUT)

    def cleanup(self):
        GPIO.cleanup()

    def verify_color(self, color):
        """Raise an error if this is not a legal colour"""
        # verify colour tuple
        if not isinstance(color, tuple) or len(color) != 3:
            raise ValueError("`color` must be a tuple of length 3")
        for b in color:
            if not isinstance(b, bool):
                raise ValueError("`color may only contain booleans")

    def latch(self):
        """
        Set the state of the LEDs to the values in the underlying row memory.
        """
        GPIO.output(self.pins['latch'], 1)
        GPIO.output(self.pins['latch'], 0)

    def clock(self):
        """
        Move the memory underlying the LEDs one LED

        This fills the first entry with the current colour (set by `set_color`)
        and discards the value in the last entry. All other values are shifted.
        """
        GPIO.output(self.pins['clock'], 1)
        GPIO.output(self.pins['clock'], 0)

    @staticmethod
    def bits_from_int(x, length=4):
        return tuple(x & (2 ** p) for p in range(length))

    def set_row(self, row):
        """
        Select which row to control.
        """
        self.row = row
        for pin, value in zip(self.pins['row'], self.bits_from_int(row)):
            GPIO.output(pin, value)

    def set_color(self, x, y, color):
        self.verify_color(color)
        super(GPIOLEDMatrix, self).set_color(x, y, color)

    def set_output_color(self, color, pins='rgb1'):
        self.color = color
        for pin, value in zip(self.pins[pins], color):
            GPIO.output(pin, value)

    def set_oe(self, oe):
        """
        Turn off all LEDs of all rows. True turns the LEDs off.

        The state of the LEDs and the content of the memory are kept. This
        means `set_oe(True)` (disabling the LEDs) followed by `set_oe(True)`
        (enabling the LEDs) effectively does nothing.
        """
        self.oe = oe
        GPIO.output(self.pins['oe'], oe)

    def draw(self):
        """Redraw the whole led board"""
        # Set the memories of all the rows
        for row, colors in enumerate(self.colors):
            self.set_row(row)
            # time.sleep(delay)
            for col, color in enumerate(colors):
                self.set_output_color(self.get_color(row, col))
                self.clock()
            time.sleep(self.delay)   # Why was this delay here in the first place?

        # Latch the memories to the LEDs
        self.set_oe(True)
        for _ in self.colors:
            self.set_row(row)
            self.latch()
        self.set_oe(False)


if __name__ == '__main__':
    # very light testing
    import time
    board = GPIOLEDMatrix(PINS, DELAY, SIZE)
    board.draw()
    board.set_color(0, 0, (True,) * 3)
    time.sleep(15)
    board.cleanup()
