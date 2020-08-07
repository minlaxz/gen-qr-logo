######################################################################
##        This is developed by ~Min Laxz~  Under GNU license        ##
## This mean you can FREELY share this script to improve print job  ##
##          This script is orginnaly developed by Min Laxz          ##
##             Project Decscrition is aviable in github             ##
##               https://github.com/minlaxz/qrprint/                ##
#######################################################################

from flask import Flask, request, render_template

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

ml = [win32print,win32ui,PIL.ImageTk,PIL.Image,PIL.ImageWin,pyqrcode,datetime,re,requests]

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
    #return (email+'-'+password+'-'+username+'-'+acctype+'-'+st+'-'+nd+'-'+rd+'-'+dob)

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
    qrim.paste(logo,box) ############### #qrim.show()
    fileis = '.\doneqrs\{0}_{1}.png'.format(n,date)
    qrim.save(fileis)
    print('QR with logo created and saved.\n Name is:{0}.'.format(fileis))
	#makeprint(fileis)

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
    sleep(5)

if __name__ == '__main__':
   app.run(host='0.0.0.0',port='80' ,debug=False)

#while True:
#    try:
#        system('cls')
#        print("Ctrl+C to Stop ### Shaine by laxz ###")
#        app.run(host='0.0.0.0',port='80' ,debug=False)
#    except TypeError:
#        pass
#    except Exception as e:
#        print(e)
#
