from views import app
from flask import  request,redirect,url_for,session
from oauth2client import  client, crypt
import json
import rethinkdb as r
from data_classes import user_save

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

        picture="/static/assets/img/user.png"


        url= '/dashboard'
        connection=r.connect(host='localhost',port=28015)
        count=r.db('taggem').table('user').filter({'user_id':idinfo['email']}).count().run(connection)
        
        try:
        	picture=idinfo['picture']
        except:
                picture="/static/assets/img/user.png"


        if count>0:
        	print id_token
        	print "User exist"
        else:
        	print dir(idinfo)
        	new_user=user_save(user_id=idinfo['email'],connection=connection,full_name=idinfo['name'],profile_url=picture)
        	new_user.save_to_db()
        	
        	print ("New user created in database")



        session['logged_user_ID']=idinfo['email']
         
        session['profile']=picture
        session['email']=idinfo['email']
        t=list(r.db('taggem').table('user').filter({'user_id':session['email']}).run(connection))
        session['id']=t
        session['name']= idinfo['name']
        return url

 
