from machine import Pin, SPI
import time
import framebuf

class dogm128(framebuf.FrameBuffer):
    # init with my personal defaults
    def __init__(self, spi=SPI(1, 10_000_000, sck=Pin(10), mosi=Pin(11)),
                 a0=Pin(12, Pin.OUT), cs=Pin(13, Pin.OUT)):
        self.spi =  spi
        self.cs = cs
        self.a0 = a0
        self._init_seq()
        self.data = bytearray(128*8)
        super().__init__(self.data, 128, 64, framebuf.MONO_VLSB)
        self.printfb()


    def sendcmd(self, cmd):
        self.cs(0)
        self.a0(0)
        b = bytearray(1)
        b[0] = cmd
        self.spi.write(b)
        self.cs(1)
        time.sleep(0.001)


    def senddata(self, data):
        self.cs(0)
        self.a0(1)
        self.spi.write(data)
        self.cs(1)


    def _init_seq(self):
        self.sendcmd(0x40)
        self.sendcmd(0xa1)
        self.sendcmd(0xc0)
        self.sendcmd(0xa6)
        self.sendcmd(0xa2)
        self.sendcmd(0x2f)
        self.sendcmd(0xfb)
        self.sendcmd(0x00)
        self.sendcmd(0x27)
        self.sendcmd(0x81)
        self.sendcmd(0x16)
        self.sendcmd(0x00)
        self.sendcmd(0xaf)


    def jumpline(self, line):
        self.sendcmd(0xb0 + line)  # line 0
        self.sendcmd(0x00)  # pos low 0
        self.sendcmd(0x10)  # pos high 0

    def cleanfb(self):
        self.data = bytearray(128*8)
        self.printfb()

    def printfb(self):
        for i in range(0, 8):
            self.jumpline(i)
            self.senddata(self.data[i * 128 : i * 128 + 128])
