import win32print ,win32ui
import PIL.ImageTk , PIL.Image , PIL.ImageWin
import pyqrcode
import datetime , re
from sys import exit
from os import system
from time import sleep
from firebase_admin import db
from firebase_admin import credentials , initialize_app
import requests

cred = credentials.Certificate('serviceKey.json')
initialize_app(cred ,
{
    'databaseURL' : 'https://laxz-test.firebaseio.com/' ,
    'databaseAuthVariableOverride' : {
        'uid' : 'laxz-admin'
    }
})

def getdata():
	# TODO error (1) r2
	ques = [None , None , None ,None]
	email = input("Email: ")
	match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
	if match == None:
		print('Bad Syntax')
		raise ValueError('Bad Syntax')
	password = input('Password: ')
	name = input('Name: ')
	acctype = input("Account Type[iCloud:i Google:g Facebook:f]: ")
	if acctype == 'i':
# TODO error (1)
		for i in range(4):
			ques[i] = input('Ques: ')
	elif acctype == 'f' or 'g':
		pass
	else:
		print('Error: Invalid account type.')

	if not email or not password or not name or not acctype:
		print('Error: Data have been bypassing ...')
	else:
		system('cls')
		if(acctype == 'g'):
			acctype = 'Google'
		if(acctype == 'i'):
			acctype = 'iCloud'
		if(acctype == 'f'):
			acctype = 'Facebook'
		showdata(email,password,name,acctype,ques)
		chk = input("Correct ? Enter Cancle[c]: ")
		if chk == 'y' or chk == '' or chk == 'yes' or chk=='Y' or chk=='Yes':
			makeqr(email,password,name,acctype,ques)
			print('Printed chk')
		else:
			print('Cancled Process.')
			pass


def showdata(e,p,n,t,ques):
	print(" Email: {0}\n Password: {1}\n Name: {2}\n Type: {3}\n FirstQuestion: {4}\n SecondQuestion: {5}\n ThirdQuestion: {6}\n DOB: {7}\n".format(e,p,n,t,ques[0],ques[1],ques[2],ques[3]))

def makeqr(e,p,n,t,ques):
	date = datetime.datetime.now().strftime("%y-%m-%d_%H-%M")
	print('Making QR ...')
	if(t == 'iCloud'):
		#print(ques)
		# TODO error (1) r
		q = pyqrcode.create('email:{0}, password:{1}, name:{2}, type:{3}, date:{4}, st:{5}, nd:{6}, rd:{7} DOB: {8}\n'.format(e,p,n,t,date,ques[0],ques[1],ques[2],ques[3]))
	else:
		q = pyqrcode.create('email:{0}, password:{1}, name:{2}, type:{3}, date:{4}'.format(e,p,n,t,date))
    
	q.png('.\qrs\{0}.png'.format(n),scale=6)
	print('QR making: OK.')
	file_name = '.\qrs\{0}.png'.format(n)
	makeqrlogo(file_name,e,p,n,t,ques,date)

def makeqrlogo(file_name,e,p,n,t,ques,date):
	print('Making QR with LOGO ...')
	qrim = PIL.Image.open(file_name)
	qrim = qrim.convert("RGBA")
	box = (125,125,205,205)
	qrim.crop(box)	
	logo = PIL.Image.open('logo.png')
	logo = logo.resize((box[2] - box[0], box[3] - box[1]))
	qrim.paste(logo,box) ############### #qrim.show()
	fileis = '.\doneqrs\{0}_{1}.png'.format(n,date)
	qrim.save(fileis)
	print('QR with logo created and saved.\n Name is:{0}.'.format(fileis))
	#makeprint(fileis)
	i = check_internet()
	if i:
		print('Saving to cloud ...')
		savedb(e,p,n,t,ques,date)
	else:
		print('CAUTION: I THINK THERE IS NO INTERNET.')
		print('DATA WILL BE SAVED TO LOCAL SQL DATABASE')
		#TODO
    #return im

def savedb(e,p,n,t,ques,dt):
	d = dt.split("_")
	date = d[0]
	time = d[1]
	databaseRef = db.reference('/accounts/'+t+'/'+date+'/'+time+'/')
	try:
		databaseRef.set({
			u'email' : e,
			u'password':p,
			u'name':n,
			u'stques':ques[0],
			u'ndques':ques[1],
			u'rdques':ques[2],
			u'DOB':ques[3]
		})
	except Exception as e:
		print(e)
	print('Cloud saved.')
	print('Min Laxz is sleeping here ... zZzZzZz')
	sleep(5)

def check_internet():
	url='https://www.example.com/'
	timeout=3
	try:
		_ = requests.get(url, timeout=timeout)
		return True
	except requests.ConnectionError:
		return False

def makeprint(loc):
	print('Printer Connection: Complete')
	printer_name = win32print.GetDefaultPrinter ()
	hDC = win32ui.CreateDC ()
	hDC.CreatePrinterDC (printer_name)
	scales = 1024, 1024 , 820 , 733
	printable_area = scales[0] , scales[1]
	printer_size = scales[1] , scales[0]
	printer_margins = scales[0] -scales[2] , scales[1] -scales[3]
	for i in range(1 , 3):
		print('Printing in {0} secs'.format((0-i)*(-1)))
		sleep(i)
	file_name = PIL.Image.open (loc)
	ratios = [1.0 * printable_area[0] / file_name.size[0], 1.0 * printable_area[1] / file_name.size[1]]
	scale = min(ratios)
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
	print('Printed .')

while True:
	try:
		system('cls')
		print("Ctrl+C to Stop ### Shaine by laxz ###")
		getdata()
	except KeyboardInterrupt:
		print('\nProgram is Stopped.')
		exit()
	except Exception as e:
		print(e)
















'''error (1)
		#for i in ques:
		#	ques[i] = input(str(ques.keys)+': ')
		#for key , value in ques.items():
		#	if key:
		#		ques[key] = input(key+ ": ")
		related #q = pyqrcode.create('email:{0}, password:{1}, name:{2}, type:{3}, FirstQuestion:{4}, SecondQuestion:{5}, ThirdQuestion:{6}'.format(e,p,n,t,ques['FirstQuestion'],ques['SecondQuestion'],ques['ThirdQuestion']))
		related #ques = { 'FirstQuestion' : None ,  'SecondQuestion': None , 'ThirdQuestion' : None } r2

'''
