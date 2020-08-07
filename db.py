from firebase_admin import db
from firebase_admin import credentials , initialize_app

cred = credentials.Certificate('serviceKey.json')
initialize_app(cred ,
{
    'databaseURL' : 'https://laxz-test.firebaseio.com/' ,
    'databaseAuthVariableOverride' : {
        'uid' : 'laxz-admin'
    }
})
ref = db.reference('/accounts')
