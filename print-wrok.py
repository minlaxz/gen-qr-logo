import win32print
import win32ui
from PIL import Image, ImageWin
printer_name = win32print.GetDefaultPrinter ()
file_name = "./qrs/min.png"
hDC = win32ui.CreateDC ()
hDC.CreatePrinterDC (printer_name)
#printable_area = hDC.GetDeviceCaps (8), hDC.GetDeviceCaps (10) # HORZRES / VERTRES = printable area
#printer_size = hDC.GetDeviceCaps (110), hDC.GetDeviceCaps (111) # PHYSICAL WIDTH/HEIGHT = total area
#printer_margins = hDC.GetDeviceCaps (112), hDC.GetDeviceCaps (113) # PHYSICALOFFSETX/Y = left / top margin
printable_area = hDC.GetDeviceCaps (0), hDC.GetDeviceCaps (0) 
printer_size = hDC.GetDeviceCaps (0), hDC.GetDeviceCaps (0)   
printer_margins = hDC.GetDeviceCaps (4), hDC.GetDeviceCaps (6)

bmp = Image.open (file_name)
if bmp.size[0] > bmp.size[1]:     #270width 270height
  bmp = bmp.rotate (90)

ratios = [1.0 * printable_area[0] / bmp.size[0], 1.0 * printable_area[1] / bmp.size[1]]
scale = min (ratios)

#
# Start the print job, and draw the bitmap to
#  the printer device at the scaled size.
#
hDC.StartDoc (file_name)
hDC.StartPage ()

dib = ImageWin.Dib (bmp)
scaled_width, scaled_height = [int (scale * i) for i in bmp.size]
x1 = int ((printer_size[0] - scaled_width) / 2)
y1 = int ((printer_size[1] - scaled_height) / 2)
x2 = x1 + scaled_width
y2 = y1 + scaled_height
dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))

hDC.EndPage ()
hDC.EndDoc ()
hDC.DeleteDC ()