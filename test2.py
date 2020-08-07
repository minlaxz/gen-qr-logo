import subprocess
from os import chdir,popen
#\path\to\env\Scripts\activate

subprocess.check_call(['py', '-m', 'virtualenv', 'laxzenv'])
chdir('laxzenv\Scripts')
popen('activate')
#subprocess.check_call(['python', '-m', 'qrcode'])
popen('py -m qrcode')