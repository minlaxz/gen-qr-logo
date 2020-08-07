from tkinter import *
root = Tk()
root.geometry("630x470")
root.title("Shane laxz")
root.configure(background='grey')
root.resizable(False,False)

try:
	from sys import executable,exit
	from subprocess import check_call
	from progress.bar import Bar
	bar = Bar('Processing', max=4)
	try:
		import win32print ,win32ui
		import PIL.ImageTk , PIL.Image , PIL.ImageWin
		import pyqrcode
		import os
	except ImportError as e:
		print(e)
		check_call([executable, '-m', 'pip', 'install','-r', req.txt])
except ImportError as e:
	print(e)
	print('You need to run \'pip3 install subprocess sys\'')
	exit()

def makeqr(e,p,n,t):
	e1.delete(0, 'end')
	e2.delete(0, 'end')
	e3.delete(0, 'end')
	e4.delete(0, 'end')
	#if t == 'icloud':

	q = pyqrcode.create('email:{0}, password:{1}, name:{2}, type:{3}'.format(e,p,n,t))
	q.png('.\qrs\{0}.png'.format(n),scale=6)
	print('OK ...')
	file_name = '.\qrs\{0}.png'.format(n)
	makeqrlogo(file_name,n)
	#return ('.\qrs\{0}.png'.format(n))


def makeqrlogo(file_name,n):
	qrim = PIL.Image.open(file_name)
	qrim = qrim.convert("RGBA")
	box = (125,125,205,205)
	qrim.crop(box)	
	logo = PIL.Image.open('logo.png')
	logo = logo.resize((box[2] - box[0], box[3] - box[1]))
	qrim.paste(logo,box)
	#qrim.show()
	qrim.save('.\doneqrs\{0}.png'.format(n))
	makeprint('.\doneqrs\{0}.png'.format(n))
    #return im

def makeprint(loc):
	printer_name = win32print.GetDefaultPrinter ()
	hDC = win32ui.CreateDC ()
	hDC.CreatePrinterDC (printer_name)
	printable_area = hDC.GetDeviceCaps (0), hDC.GetDeviceCaps (0) 
	printer_size = hDC.GetDeviceCaps (0), hDC.GetDeviceCaps (0)   
	printer_margins = hDC.GetDeviceCaps (4), hDC.GetDeviceCaps (6)
	file_name = PIL.Image.open (loc)
	ratios = [1.0 * printable_area[0] / file_name.size[0], 1.0 * printable_area[1] / file_name.size[1]]
	scale = min (ratios)
	hDC.StartDoc (loc)
	hDC.StartPage ()
	dib = PIL.ImageWin.Dib (file_name)
	scaled_width, scaled_height = [int (scale * i) for i in file_name.size]
	x1 = int ((printer_size[0] - scaled_width) / 2)
	y1 = int ((printer_size[1] - scaled_height) / 2)
	x2 = x1 + scaled_width
	y2 = y1 + scaled_height
	dib.draw (hDC.GetHandleOutput (), (x1, y1, x2, y2))
	hDC.EndPage ()
	hDC.EndDoc ()
	hDC.DeleteDC ()

def showimg():
	email = e1.get()
	password = e2.get()
	name = e3.get()
	acctype = e4.get()
	if not email or not password or not name or not acctype:
		print('error')
	else:
		print('Creating QR ...')
		makeqr(email,password,name,acctype)

def destory():
	root.destroy()

e1 = Entry(root, width=25)
e2 = Entry(root, width=25 , show="*")
e3 = Entry(root, width=25)
e4 = Entry(root, width=25)
e1.pack()
e2.pack()
e3.pack()
e4.pack()
e1.place(x=100, y=2)
e2.place(x=100, y=27)
e3.place(x=420, y=2)
e4.place(x=420, y=27)

l1 = Label(root, text="Email ==>", bg='grey')
l2 = Label(root, text="Password ==>", bg='grey')
l3 = Label(root, text="Name ==>", bg='grey')
l4 = Label(root, text="AccType ==>", bg='grey')
l1.pack()
l2.pack()
l3.pack()
l4.pack()
l1.place(x=22, y=2)
l2.place(x=2, y=27)
l3.place(x=335, y=2)
l4.place(x=320, y=27)
saveBtn = Button(root, text='Proceed', bg='grey', fg='black', command=showimg)
quitBtn = Button(root, text='Adios', bg='grey', fg='red', command=destory)
quitBtn.pack()
saveBtn.pack()
saveBtn.place(x=85, y=70)
quitBtn.place(x=10, y=70)

img = PIL.ImageTk.PhotoImage(PIL.Image.open('.\qrs\min.png'))
panel = Label(root,image = img)
#panel.pack()
panel.pack(side = "bottom", fill = "both", expand = "yes")
panel.place(x=200,y=180)

mainloop()


#os.startfile(filename, "print")