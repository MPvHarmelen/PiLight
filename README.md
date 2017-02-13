# PiLight
-----

This controller uses code inspired from [this tutorial](https://learn.adafruit.com/connecting-a-16x32-rgb-led-matrix-panel-to-a-raspberry-pi).
More detailed explanation [here](http://www.rayslogic.com/propeller/programming/AdafruitRGB/AdafruitRGB.htm)

Only one row of LEDS can be on simultaneously.

## Pin meanings

Pins can only have a `high` or `low` value. On a 32x32 board two rows are
controlled simultaneously. On a 16x32 board only the top row is used (we assume
the second row is ignored.)

Board pin  | description        | Pi pin           | baby languages
---------- | ------------------ | ---------------- | --------------
R1         | Red 1st bank       | GPIO 17          | red LED on top row
G1         | Green 1st bank     | GPIO 18          | green LED on top row
B1         | Blue 1st bank      | GPIO 22          | blue LED on top row
R2         | Red 2nd bank       | GPIO 23          | red LED on bottom row
G2         | Green 2nd bank     | GPIO 24          | green LED on bottom row
B2         | Blue 2nd bank      | GPIO 25          | blue LED on bottom row
A, B, C, D | Row address        | GPIO 7, 8, 9, 10 | a 4-bit row address
OE-        | neg. Output enable | GPIO 2           | whether the boards is on at all
CLK        | Serial clock       | GPIO 3           | select next LED
STR        | Strobe row data    | GPIO 4           | make LEDs show current row data

is | this | a
--- | --- | ---
working | table? |

## Protocol
rectangle (xpos, ypos, xsize, ysize)
on/off

## TODO
 - [ ] Move ping configuration to configuration file
