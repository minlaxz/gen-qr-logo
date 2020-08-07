from escpos.printer import Usb
#from escpos.connections import getUSBPrinter
p = Usb(0x04B8,0x007B)
#p = Usb(0x1a2b,0x1a2b,0,0x81,0x02)
#p = Usb(0x04b8, 0x0202, 0, profile="TM-T88III")
p.text("Hello World")
#p.image("logo.gif")
#p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
p.cut()


import usb.core
import usb.util

# find our device
dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)
p = usb.core.find(0x04B8,0x007B)
# was it found?
if dev is None:
    raise ValueError('Device not found')