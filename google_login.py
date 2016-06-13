from views import app,session
from flask import  request,redirect,url_for
from oauth2client import  client, crypt
import json


CLIENT_ID='316193309283-p2j4rca3lbmcpj749bhij5ea41tf7579.apps.googleusercontent.com'
@app.route('/tokenSignInGoogle', methods=['POST'])
def tokenGoogle():
	id_token=request.form['idtoken']
 
	 
	
	try:
		idinfo=client.verify_id_token(id_token,CLIENT_ID)
		if idinfo['aud'] not in [CLIENT_ID]:
			raise crypt.AppIdentityError("Unrecognized client.")
		if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                	raise crypt.AppIdentityError("Wrong issuer.")
                '''if idinfo['hd'] != APPS_DOMAIN_NAME:
                        raise crypt.AppIdentityError("Wrong hosted domain.")'''

	except crypt.AppIdentityError:
		print "Invalid Token"

        url= '/dashboard'
         
        session['profile']=idinfo['picture']
        session['email']=idinfo['email']
        session['name']= idinfo['name']
        session['auth_token']=id_token
        return url

	print idinfo
	return 'google'
