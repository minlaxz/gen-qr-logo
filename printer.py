from escpos.connections import getUSBPrinter


printer = getUSBPrinter()(idVendor=0x04B8,
                          idProduct=0x007B,
                          inputEndPoint=0x82,
                          outputEndPoint=0x01) # Create the printer object with the connection params

printer.text("Hello World")
printer.lf()
