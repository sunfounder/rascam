# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
import numbers
import time
import numpy as np
from PIL import Image
# import spidev
import RPi.GPIO as GPIO
import Adafruit_GPIO.SPI as SPI

__version__ = '0.0.2'

BG_SPI_CS_BACK = 0
BG_SPI_CS_FRONT = 1

SPI_CLOCK_HZ = 40000000

ST7789_NOP = 0x00
ST7789_SWRESET = 0x01
ST7789_RDDID = 0x04
ST7789_RDDST = 0x09

ST7789_SLPIN = 0x10
ST7789_SLPOUT = 0x11
ST7789_PTLON = 0x12
ST7789_NORON = 0x13

# ILI9341_RDMODE = 0x0A
# ILI9341_RDMADCTL = 0x0B
# ILI9341_RDPIXFMT = 0x0C
# ILI9341_RDIMGFMT = 0x0A
# ILI9341_RDSELFDIAG = 0x0F

ST7789_INVOFF = 0x20
ST7789_INVON = 0x21
# ILI9341_GAMMASET = 0x26
ST7789_DISPOFF = 0x28
ST7789_DISPON = 0x29

ST7789_CASET = 0x2A
ST7789_RASET = 0x2B
ST7789_RAMWR = 0x2C
ST7789_RAMRD = 0x2E

ST7789_PTLAR = 0x30
ST7789_MADCTL = 0x36
ST7789_COLMOD = 0x3A

ST7789_FRMCTR1 = 0xB1
ST7789_FRMCTR2 = 0xB2
ST7789_FRMCTR3 = 0xB3
ST7789_INVCTR = 0xB4
# ILI9341_DFUNCTR = 0xB6
ST7789_DISSET5 = 0xB6

ST7789_GCTRL = 0xB7
ST7789_GTADJ = 0xB8
ST7789_VCOMS = 0xBB

ST7789_LCMCTRL = 0xC0
ST7789_IDSET = 0xC1
ST7789_VDVVRHEN = 0xC2
ST7789_VRHS = 0xC3
ST7789_VDVS = 0xC4
ST7789_VMCTR1 = 0xC5
ST7789_FRCTRL2 = 0xC6
ST7789_CABCCTRL = 0xC7

ST7789_RDID1 = 0xDA
ST7789_RDID2 = 0xDB
ST7789_RDID3 = 0xDC
ST7789_RDID4 = 0xDD

ST7789_GMCTRP1 = 0xE0
ST7789_GMCTRN1 = 0xE1

ST7789_PWCTR6 = 0xFC


class ST7789(object):
    """Representation of an ST7789 TFT LCD."""

    def __init__(self, port, cs, dc, backlight=None, rst=None, width=320,
                 height=240, rotation=90, invert=True, spi_speed_hz=4000000):
        """Create an instance of the display using SPI communication.
        Must provide the GPIO pin number for the D/C pin and the SPI driver.
        Can optionally provide the GPIO pin number for the reset pin as the rst parameter.
        :param port: SPI port number
        :param cs: SPI chip-select number (0 or 1 for BCM
        :param backlight: Pin for controlling backlight
        :param rst: Reset pin for ST7789
        :param width: Width of display connected to ST7789
        :param height: Height of display connected to ST7789
        :param rotation: Rotation of display connected to ST7789
        :param invert: Invert display
        :param spi_speed_hz: SPI speed (in Hz)
        """

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)

        # self._spi = spidev.SpiDev(port, cs)
        self._spi = SPI.SpiDev(0, 0, max_speed_hz=spi_speed_hz)
        self._spi.mode = 0
        self._spi.lsbfirst = False
        # self._spi.max_speed_hz = spi_speed_hz

        self._dc = dc
        self._rst = rst
        self._width = width
        self._height = height
        self._rotation = rotation
        self._invert = invert

        self._offset_left = 0
        self._offset_top = 0

        # Set DC as output.
        GPIO.setup(dc, GPIO.OUT)

        # Setup backlight as output (if provided).
        self._backlight = backlight
        if backlight is not None:
            GPIO.setup(backlight, GPIO.OUT)
            GPIO.output(backlight, GPIO.LOW)
            time.sleep(0.1)
            GPIO.output(backlight, GPIO.HIGH)

        # Setup reset as output (if provided).
        if rst is not None:
            GPIO.setup(rst, GPIO.OUT)

        self.reset()
        self._init()

    def send(self, data, is_data=True, chunk_size=4096):
        """Write a byte or array of bytes to the display. Is_data parameter
        controls if byte should be interpreted as display data (True) or command
        data (False).  Chunk_size is an optional size of bytes to write in a
        single SPI transaction, with a default of 4096.
        """
        # Set DC low for command, high for data.
        GPIO.output(self._dc, is_data)

        # Convert scalar argument to list so either can be passed as parameter.
        if isinstance(data, numbers.Number):
            data = [data & 0xFF]
        # Write data a chunk at a time.
        # data = [i for i in range(4096)]
        for start in range(0, len(data), chunk_size):
            # print("ss")
            end = min(start + chunk_size, len(data))
            # time.sleep(0.001)
            # print(len(data),start,end)
            # self._spi.xfer(data[start:end])
            self._spi.write(data[start:end])

    def set_backlight(self, value):
        """Set the backlight on/off."""
        if self._backlight is not None:
            GPIO.output(self._backlight, value)

    @property
    def width(self):
        return self._width if self._rotation == 0 or self._rotation == 180 else self._height

    @property
    def height(self):
        return self._height if self._rotation == 0 or self._rotation == 180 else self._width

    def command(self, data):
        """Write a byte or array of bytes to the display as command data."""
        self.send(data, False)

    def data(self, data):
        """Write a byte or array of bytes to the display as display data."""
        self.send(data, True)

    def reset(self):
        """Reset the display, if reset pin is connected."""
        if self._rst is not None:
            GPIO.output(self._rst, 1)
            time.sleep(0.500)
            GPIO.output(self._rst, 0)
            time.sleep(0.500)
            GPIO.output(self._rst, 1)
            time.sleep(0.500)

    def _init(self):
        # Initialize the display.

        self.command(ST7789_SWRESET)    # Software reset
        time.sleep(0.150)               # delay 150 ms

        self.command(ST7789_MADCTL)
        self.data(0x70)

        self.command(ST7789_FRMCTR2)    # Frame rate ctrl - idle mode
        self.data(0x0C)
        self.data(0x0C)
        self.data(0x00)
        self.data(0x33)
        self.data(0x33)

        self.command(ST7789_COLMOD)
        self.data(0x05)

        self.command(ST7789_GCTRL)
        self.data(0x14)

        self.command(ST7789_VCOMS)
        self.data(0x37)

        self.command(ST7789_LCMCTRL)    # Power control
        self.data(0x2C)

        self.command(ST7789_VDVVRHEN)   # Power control
        self.data(0x01)

        self.command(ST7789_VRHS)       # Power control
        self.data(0x12)

        self.command(ST7789_VDVS)       # Power control
        self.data(0x20)

        self.command(0xD0)
        self.data(0xA4)
        self.data(0xA1)

        self.command(ST7789_FRCTRL2)
        self.data(0x0F)

        self.command(ST7789_GMCTRP1)    # Set Gamma
        self.data(0xD0)
        self.data(0x04)
        self.data(0x0D)
        self.data(0x11)
        self.data(0x13)
        self.data(0x2B)
        self.data(0x3F)
        self.data(0x54)
        self.data(0x4C)
        self.data(0x18)
        self.data(0x0D)
        self.data(0x0B)
        self.data(0x1F)
        self.data(0x23)

        self.command(ST7789_GMCTRN1)    # Set Gamma
        self.data(0xD0)
        self.data(0x04)
        self.data(0x0C)
        self.data(0x11)
        self.data(0x13)
        self.data(0x2C)
        self.data(0x3F)
        self.data(0x44)
        self.data(0x51)
        self.data(0x2F)
        self.data(0x1F)
        self.data(0x1F)
        self.data(0x20)
        self.data(0x23)

        if self._invert:
            self.command(ST7789_INVON)   # Invert display
        else:
            self.command(ST7789_INVOFF)  # Don't invert display

        self.command(ST7789_SLPOUT)

        self.command(ST7789_DISPON)     # Display on
        time.sleep(0.100)               # 100 ms

    def begin(self):
        """Set up the display
        Deprecated. Included in __init__.
        """
        pass

    def set_window(self, x0=0, y0=0, x1=None, y1=None):
        """Set the pixel address window for proceeding drawing commands. x0 and
        x1 should define the minimum and maximum x pixel bounds.  y0 and y1
        should define the minimum and maximum y pixel bound.  If no parameters
        are specified the default will be to update the entire display from 0,0
        to width-1,height-1.
        """
        if x1 is None:
            x1 = self._width - 1

        if y1 is None:
            y1 = self._height - 1

        y0 += self._offset_top
        y1 += self._offset_top

        x0 += self._offset_left
        x1 += self._offset_left

        self.command(ST7789_CASET)       # Column addr set
        self.data(x0 >> 8)
        self.data(x0 & 0xFF)             # XSTART
        self.data(x1 >> 8)
        self.data(x1 & 0xFF)             # XEND
        self.command(ST7789_RASET)       # Row addr set
        self.data(y0 >> 8)
        self.data(y0 & 0xFF)             # YSTART
        self.data(y1 >> 8)
        self.data(y1 & 0xFF)             # YEND
        self.command(ST7789_RAMWR)       # write to RAM

    def display(self, image):
        """Write the provided image to the hardware.
        :param image: Should be RGB format and the same dimensions as the display hardware.
        """
        # Set address bounds to entire display.
        self.set_window()
        # print("window")
        # Convert image to array of 18bit 666 RGB data bytes.
        # Unfortunate that this copy has to occur, but the SPI byte writing
        # function needs to take an array of bytes and PIL doesn't natively
        # store images in 18-bit 666 RGB format.
        pixelbytes = list(self.image_to_data(image, self._rotation))
        # print("image data")
        # Write data to hardware.
        # print(len(pixelbytes))
        # for i in range(0, len(pixelbytes), 4096):
        #     self.data(pixelbytes[i:i + 4096])
        self.data(pixelbytes)
        # print("for")

    def image_to_data(self, image, rotation=0):
        """Generator function to convert a PIL image to 16-bit 565 RGB bytes."""
        # NumPy is much faster at doing this. NumPy code provided by:
        # Keith (https://www.blogger.com/profile/02555547344016007163)
        # pb = np.rot90(np.array(image.convert('RGB')), rotation // 90).astype('uint8')
        # image = Image.fromarray(image)
        # pb = np.rot90(np.array(image.convert('RGB')), rotation // 90).astype('uint8')
        pb = np.rot90(image, rotation // 90).astype('uint16')
        # pb = np.array(image.convert('RGB')).astype('uint8')
        # print('pb:',pb.shape)
        result = np.zeros((self._height, self._width, 2), dtype=np.uint8)
        # print('result:',result[..., [0]].shape)
        a = np.bitwise_and(pb[..., [0]], 0xF8)
        b = np.right_shift(pb[..., [1]], 5)
        # print('a:',a.shape)
        # print('b:',b.shape)
        result[..., [0]] = np.add(a, b)
        result[..., [1]] = np.add(np.bitwise_and(np.left_shift(pb[..., [1]], 3), 0xE0), np.right_shift(pb[..., [2]], 3))
        return result.flatten().tolist()



# ST7789 IPS LCD (240x240) driver
# import numbers
# import time
# import numpy as np

# from PIL import Image
# from PIL import ImageDraw

# import Adafruit_GPIO as GPIO
# import Adafruit_GPIO.SPI as SPI
# # import spidev
# # import RPi.GPIO as GPIO
# SPI_CLOCK_HZ = 40000000 # 40 MHz

# # Constants for interacting with display registers.
# ST7789_TFTWIDTH    = 320
# ST7789_TFTHEIGHT   = 240

# ST7789_NOP         = 0x00
# ST7789_SWRESET     = 0x01
# ST7789_RDDID       = 0x04
# ST7789_RDDST       = 0x09
# ST7789_RDDPM       = 0x0A
# ST7789_RDDMADCTL   = 0x0B
# ST7789_RDDCOLMOD   = 0x0C
# ST7789_RDDIM       = 0x0D
# ST7789_RDDSM       = 0x0E
# ST7789_RDDSDR      = 0x0F

# ST7789_SLPIN       = 0x10
# ST7789_SLPOUT      = 0x11
# ST7789_PTLON       = 0x12
# ST7789_NORON       = 0x13

# ST7789_INVOFF      = 0x20
# ST7789_INVON       = 0x21
# ST7789_GAMSET      = 0x26
# ST7789_DISPOFF     = 0x28
# ST7789_DISPON      = 0x29
# ST7789_CASET       = 0x2A
# ST7789_RASET       = 0x2B
# ST7789_RAMWR       = 0x2C
# ST7789_RAMRD       = 0x2E

# ST7789_PTLAR       = 0x30
# ST7789_VSCRDEF     = 0x33
# ST7789_TEOFF       = 0x34
# ST7789_TEON        = 0x35
# ST7789_MADCTL      = 0x36
# ST7789_VSCRSADD    = 0x37
# ST7789_IDMOFF      = 0x38
# ST7789_IDMON       = 0x39
# ST7789_COLMOD      = 0x3A
# ST7789_RAMWRC      = 0x3C
# ST7789_RAMRDC      = 0x3E

# ST7789_TESCAN      = 0x44
# ST7789_RDTESCAN    = 0x45

# ST7789_WRDISBV     = 0x51
# ST7789_RDDISBV     = 0x52
# ST7789_WRCTRLD     = 0x53
# ST7789_RDCTRLD     = 0x54
# ST7789_WRCACE      = 0x55
# ST7789_RDCABC      = 0x56
# ST7789_WRCABCMB    = 0x5E
# ST7789_RDCABCMB    = 0x5F

# ST7789_RDABCSDR    = 0x68

# ST7789_RDID1       = 0xDA
# ST7789_RDID2       = 0xDB
# ST7789_RDID3       = 0xDC

# ST7789_RAMCTRL     = 0xB0
# ST7789_RGBCTRL     = 0xB1
# ST7789_PORCTRL     = 0xB2
# ST7789_FRCTRL1     = 0xB3

# ST7789_GCTRL       = 0xB7
# ST7789_DGMEN       = 0xBA
# ST7789_VCOMS       = 0xBB

# ST7789_LCMCTRL     = 0xC0
# ST7789_IDSET       = 0xC1
# ST7789_VDVVRHEN    = 0xC2

# ST7789_VRHS        = 0xC3
# ST7789_VDVSET      = 0xC4
# ST7789_VCMOFSET    = 0xC5
# ST7789_FRCTR2      = 0xC6
# ST7789_CABCCTRL    = 0xC7
# ST7789_REGSEL1     = 0xC8
# ST7789_REGSEL2     = 0xCA
# ST7789_PWMFRSEL    = 0xCC

# ST7789_PWCTRL1     = 0xD0
# ST7789_VAPVANEN    = 0xD2
# ST7789_CMD2EN      = 0xDF5A6902
# ST7789_PVGAMCTRL   = 0xE0
# ST7789_NVGAMCTRL   = 0xE1
# ST7789_DGMLUTR     = 0xE2
# ST7789_DGMLUTB     = 0xE3
# ST7789_GATECTRL    = 0xE4
# ST7789_PWCTRL2     = 0xE8
# ST7789_EQCTRL      = 0xE9
# ST7789_PROMCTRL    = 0xEC
# ST7789_PROMEN      = 0xFA
# ST7789_NVMSET      = 0xFC
# ST7789_PROMACT     = 0xFE

# # Colours for convenience
# ST7789_BLACK       = 0x0000 # 0b 00000 000000 00000
# ST7789_BLUE        = 0x001F # 0b 00000 000000 11111
# ST7789_GREEN       = 0x07E0 # 0b 00000 111111 00000
# ST7789_RED         = 0xF800 # 0b 11111 000000 00000
# ST7789_CYAN        = 0x07FF # 0b 00000 111111 11111
# ST7789_MAGENTA     = 0xF81F # 0b 11111 000000 11111
# ST7789_YELLOW      = 0xFFE0 # 0b 11111 111111 00000
# ST7789_WHITE       = 0xFFFF # 0b 11111 111111 11111


# def color565(r, g, b):
#     """Convert red, green, blue components to a 16-bit 565 RGB value. Components
#     should be values 0 to 255.
#     """
#     return ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)

# def image_to_data(image):
#     """Generator function to convert a PIL image to 16-bit 565 RGB bytes."""
#     # NumPy is much faster at doing this. NumPy code provided by:
#     # Keith (https://www.blogger.com/profile/02555547344016007163)
#     # pb = np.array(image.convert('RGB')).astype('uint16')
#     pb = np.rot90(image, rotation // 90).astype('uint8')
#     color = ((pb[:,:,0] & 0xF8) << 8) | ((pb[:,:,1] & 0xFC) << 3) | (pb[:,:,2] >> 3)
#     return np.dstack(((color >> 8) & 0xFF, color & 0xFF)).flatten().tolist()

# class ST7789(object):
#     """Representation of an ST7789 IPS LCD."""

#     def __init__(self, spi, mode=3, rst=27, dc=25, led=24,gpio=None, width=ST7789_TFTWIDTH,
#         height=ST7789_TFTHEIGHT):
#         """Create an instance of the display using SPI communication.  Must
#         provide the GPIO pin number for the D/C pin and the SPI driver.  Can
#         optionally provide the GPIO pin number for the reset pin as the rst
#         parameter.
#         """
#         self._spi = spi
#         self._rst = rst
#         self._dc = dc
#         self._led = led
#         self._gpio = gpio
#         self.width = width
#         self.height = height
#         if self._gpio is None:
#             self._gpio = GPIO.get_platform_gpio()
#         # Set DC as output.
#         self._gpio.setup(dc, GPIO.OUT)
#         # Setup reset as output (if provided).
#         if rst is not None:
#             self._gpio.setup(rst, GPIO.OUT)
#         # Turn on the backlight LED
#         self._gpio.setup(led, GPIO.OUT)
#         self._gpio.setup(led, GPIO.HIGH)
#         # Set SPI to mode 0, MSB first.
#         spi.set_mode(mode)
#         spi.set_bit_order(SPI.MSBFIRST)
#         spi.set_clock_hz(SPI_CLOCK_HZ)
#         # Create an image buffer.
#         self.buffer = Image.new('RGB', (width, height))

#     def send(self, data, is_data=True, chunk_size=4096):
#         """Write a byte or array of bytes to the display. Is_data parameter
#         controls if byte should be interpreted as display data (True) or command
#         data (False).  Chunk_size is an optional size of bytes to write in a
#         single SPI transaction, with a default of 4096.
#         """
#         # Set DC low for command, high for data.
#         self._gpio.output(self._dc, is_data)
#         # Convert scalar argument to list so either can be passed as parameter.
#         if isinstance(data, numbers.Number):
#             data = [data & 0xFF]
#         # Write data a chunk at a time.
#         for start in range(0, len(data), chunk_size):
#             end = min(start+chunk_size, len(data))
#             self._spi.write(data[start:end])

#     def command(self, data):
#         """Write a byte or array of bytes to the display as command data."""
#         self.send(data, False)

#     def data(self, data):
#         """Write a byte or array of bytes to the display as display data."""
#         self.send(data, True)

#     def reset(self):
#         """Reset the display, if reset pin is connected."""
#         if self._rst is not None:
#             self._gpio.set_high(self._rst)
#             time.sleep(0.100)
#             self._gpio.set_low(self._rst)
#             time.sleep(0.100)
#             self._gpio.set_high(self._rst)
#             time.sleep(0.100)

#     def _init(self):
#         # Initialize the display.  Broken out as a separate function so it can
#         # be overridden by other displays in the future.

#         time.sleep(0.010)
#         self.command(0x11)
#         time.sleep(0.150)

#         self.command(0x36)
#         self.data(0x00)

#         self.command(0x3A)
#         self.data(0x05)

#         self.command(0xB2)
#         self.data(0x0C)
#         self.data(0x0C)

#         self.command(0xB7)
#         self.data(0x35)

#         self.command(0xBB)
#         self.data(0x1A)

#         self.command(0xC0)
#         self.data(0x2C)

#         self.command(0xC2)
#         self.data(0x01)

#         self.command(0xC3)
#         self.data(0x0B)

#         self.command(0xC4)
#         self.data(0x20)

#         self.command(0xC6)
#         self.data(0x0F)

#         self.command(0xD0)
#         self.data(0xA4)
#         self.data(0xA1)

#         self.command(0x21)

#         self.command(0xE0)
#         self.data(0x00)
#         self.data(0x19)
#         self.data(0x1E)
#         self.data(0x0A)
#         self.data(0x09)
#         self.data(0x15)
#         self.data(0x3D)
#         self.data(0x44)
#         self.data(0x51)
#         self.data(0x12)
#         self.data(0x03)
#         self.data(0x00)
#         self.data(0x3F)
#         self.data(0x3F)

#         self.command(0xE1)
#         self.data(0x00)
#         self.data(0x18)
#         self.data(0x1E)
#         self.data(0x0A)
#         self.data(0x09)
#         self.data(0x25)
#         self.data(0x3F)
#         self.data(0x43)
#         self.data(0x52)
#         self.data(0x33)
#         self.data(0x03)
#         self.data(0x00)
#         self.data(0x3F)
#         self.data(0x3F)
#         self.command(0x29)

#         time.sleep(0.100) # 100 ms

#     def begin(self):
#         """Initialize the display.  Should be called once before other calls that
#         interact with the display are called.
#         """
#         self.reset()
#         self._init()

#     def set_window(self, x0=0, y0=0, x1=None, y1=None):
#         """Set the pixel address window for proceeding drawing commands. x0 and
#         x1 should define the minimum and maximum x pixel bounds.  y0 and y1
#         should define the minimum and maximum y pixel bound.  If no parameters
#         are specified the default will be to update the entire display from 0,0
#         to width-1,height-1.
#         """
#         if x1 is None:
#             x1 = self.width-1
#         if y1 is None:
#             y1 = self.height-1
#         self.command(ST7789_CASET)       # Column addr set
#         self.data(x0 >> 8)
#         self.data(x0)                    # XSTART
#         self.data(x1 >> 8)
#         self.data(x1)                    # XEND
#         self.command(ST7789_RASET)       # Row addr set
#         self.data(y0 >> 8)
#         self.data(y0)                    # YSTART
#         self.data(y1 >> 8)
#         self.data(y1)                    # YEND
#         self.command(ST7789_RAMWR)       # write to RAM

#     #def display(self, image=None):
#     def display(self, image=None, x0=0, y0=0, x1=None, y1=None):
#         """Write the display buffer or provided image to the hardware.  If no
#         image parameter is provided the display buffer will be written to the
#         hardware.  If an image is provided, it should be RGB format and the
#         same dimensions as the display hardware.
#         """
#         # By default write the internal buffer to the display.
#         if image is None:
#             image = self.buffer
#         # Set address bounds to entire display.
#         #self.set_window()
#         if x1 is None:
#             x1 = self.width-1
#         if y1 is None:
#             y1 = self.height-1
#         self.set_window(x0, y0, x1, y1)
#         #image.thumbnail((x1-x0+1, y1-y0+1), Image.ANTIALIAS)
#         # Convert image to array of 16bit 565 RGB data bytes.
#         # Unfortunate that this copy has to occur, but the SPI byte writing
#         # function needs to take an array of bytes and PIL doesn't natively
#         # store images in 16-bit 565 RGB format.
#         pixelbytes = list(image_to_data(image))
#         # Write data to hardware.
#         self.data(pixelbytes)

#     def clear(self, color=(0,0,0)):
#         """Clear the image buffer to the specified RGB color (default black)."""
#         width, height = self.buffer.size
#         self.buffer.putdata([color]*(width*height))

#     def draw(self):
#         """Return a PIL ImageDraw instance for 2D drawing on the image buffer."""
#         return ImageDraw.Draw(self.buffer)