from escpos.connections import getNetworkPrinter


printer = getNetworkPrinter()(host='192.168.0.1', port=9100)


printer.qr('My name is Min Latt')
printer.lf()