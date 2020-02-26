from sys import exit,executable
from subprocess import check_call
import time.sleep
try:
    from flask import Flask, request, render_template
    import win32print ,win32ui
    import PIL.ImageTk , PIL.Image , PIL.ImageWin
    import datetime , re ,pyqrcode
    from firebase_admin import db
    from firebase_admin import credentials , initialize_app
    import requests
except ImportError:
    check_call([executable, '-m', 'pip', 'install','-r', 'req.txt'])

m = [win32print,win32ui,datetime,re,pyqrcode,requests]
cred = credentials.Certificate('serviceKey.json')
initialize_app(cred ,
{
    'databaseURL' : 'https://laxz-test.firebaseio.com/' ,
    'databaseAuthVariableOverride' : {
        'uid' : 'laxz-admin'
    }
})

app = Flask(__name__)

@app.route('/')
def my_form():
    return render_template('my-form.html')

@app.route('/', methods=['POST'])
def my_form_post():
    ques = [None , None , None]
    date = datetime.datetime.now().strftime("%y-%m-%d_%H-%M")

    email = request.form['email']
    password = request.form['password']
    username = request.form['username']
    acctype = request.form['acctype']
    st = request.form['textst']
    nd = request.form['textnd']
    rd = request.form['textrd']
    dob = request.form['date']

    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
    if match == None:
        print('Bad Syntax')
        raise ValueError('Bad Syntax')
    if acctype == '1':
        acctype = 'iCloud'
        ques[0] = st
        ques[1] = nd
        ques[2] = rd
    elif acctype == '2':
        acctype = 'Google'
    elif acctype == '3':
        acctype = 'Facebook'
    makeqrlogo(makeqr(email,password,username,acctype,ques,dob,date),username,date)
    if check_internet():
    	print('Saving to cloud ...')
    	savedb(email,password,username,acctype,ques,date,dob)
    else:
    	print('CAUTION: I THINK THERE IS NO INTERNET.')
    	print('DATA WILL BE SAVED TO LOCAL SQL DATABASE')
    return 'OK'

def makeqr(e,p,n,t,ques,dob,date):
    print('Making QR ...')
    if(t == 'iCloud'):
    	# TODO error (1) r
    	q = pyqrcode.create('e:{0}, p:{1}, n:{2}, t:{3}, d:{4}, st:{5}, nd:{6}, rd:{7} DOB: {8}\n'.format(e,p,n,t,date,ques[0],ques[1],ques[2],dob))
    else:
    	q = pyqrcode.create('e:{0}, p:{1}, n:{2}, t:{3}, d:{4} , DOB:{5}'.format(e,p,n,t,date,dob))
    q.png('.\qrs\{0}.png'.format(n),scale=6)
    print('QR making: OK.')
    file_name = '.\qrs\{0}.png'.format(n)
    return (file_name)

def makeqrlogo(file_name,n,date):
    print('Making QR with LOGO ...')
    qrim = PIL.Image.open(file_name)
    qrim = qrim.convert("RGBA")
    box = (125,125,205,205)
    qrim.crop(box)	
    logo = PIL.Image.open('logo.png')
    logo = logo.resize((box[2] - box[0], box[3] - box[1]))
    qrim.paste(logo,box)
    fileis = '.\doneqrs\{0}_{1}.png'.format(n,date)
    qrim.save(fileis)
    print('QR with logo created and saved.\n Name is:{0}.'.format(fileis))
    makeprint(fileis)


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

def check_internet():
	url='https://www.example.com/'
	timeout=3
	try:
		_ = requests.get(url, timeout=timeout)
		return True
	except requests.ConnectionError:
		return False

def savedb(e,p,n,t,ques,dt,dob):
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
    		u'DOB':dob
    	})
    except Exception as e:
    	print(e)
    print('Cloud saved.')
    print('Min Laxz is sleeping here ... zZzZzZz')
    time.sleep(5)

if __name__ == '__main__':
    print('Developed by laxz')
    app.run(host='0.0.0.0',port='80' ,debug=True)

