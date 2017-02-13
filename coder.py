def encode(xpos, ypos, width, height, red=True, green=True, blue=True):
    """
    Given the position and color of the leds, encodes this information in an
    int of 3 bytes, which can be decoded using decode
    """

    # input validation first
    if not 0 <= xpos <= 31:
        raise ValueError('The x-position has to be between 0 and 31 inclusive'
                         'to fit the size of the board')
    elif not 0 <= ypos <= 15:
        raise ValueError('The y-position has to be between 0 and 15 inclusive'
                         'to fit the size of the board')
    elif width < 1:
        raise ValueError('The width value has to be higher than 0')
    elif height < 1:
        raise ValueError('The height value has to be higher than 0')
    elif width + xpos > 32:
        raise ValueError('The width and the x-position combined should not'
                         'go over the edge of the board')
    elif height + ypos > 16:
        raise ValueError('The height and the y-position combined should not'
                         'go over the edge of the board')

    signal = 0
    signal += xpos
    signal <<= 4
    signal += ypos
    signal <<= 5
    signal += width
    signal <<= 4
    signal += height
    signal <<= 3

    signal += 4 if red else 0
    signal += 2 if green else 0
    signal += 1 if blue else 0

    return signal
    
def decode(bytes):
    # color
    blue = True if bytes & 1 else False
    bytes >>= 1
    green = True if bytes & 1 else False
    bytes >>= 1
    red = True if bytes & 1 else False
    bytes >>= 1

    # height and width
    height = bytes & 2**4-1
    bytes >>= 4
    width = bytes & 2**5-1
    bytes >>= 5

    # position
    ypos = bytes & 2**4-1
    bytes >>= 4
    xpos = bytes & 2**5-1

    return xpos, ypos, width, height, red, green, blue

if __name__ == '__main__':
    a = encode(1, 2, 3, 4, blue=False)
    print(a)
    print(decode(a))