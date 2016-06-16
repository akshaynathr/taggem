import gdata.gauth
import gdata.contacts.client
from views import app 
import json
import requests
from requests import session
from flask import redirect, url_for,render_template,request,session 
from models import r
import pickle

CLIENT_ID = '316193309283-p2j4rca3lbmcpj749bhij5ea41tf7579.apps.googleusercontent.com'
CLIENT_SECRET = '0p26EhbsQnlfT5Onwfm3nQNE'
SCOPES=["https://www.google.com/m8/feeds/"]
USER_AGENT = ''


@app.route('/test')
def test():
# The client id and secret can be found on your API Console.
    
# Authorization can be requested for multiple APIs at once by specifying multiple scopes separated by # spaces.
   # SCOPES = ['https://docs.google.com/feeds/', 'https://www.google.com/calendar/feeds/']  
    
    
# Save the token for later use.
    token = gdata.gauth.OAuth2Token(
        client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=' '.join(SCOPES),
        user_agent=USER_AGENT)

    
 
    print (dir(token))
    session['google_auth_token']=pickle.dumps(token)
    #session['google_auth_toke']=gdata.gauth.token_to_blob(token)

    return redirect(
       token.generate_authorize_url(redirect_uri='https://localhost:8000/contacts'))




@app.route('/contacts')
def contacts():
    auth_token =  pickle.loads(session['google_auth_token'])
    print ("auth_token")
    print (dir(auth_token))

    #Fetch the auth_token that we set in our base view
    #auth_token = requests.session['google_auth_token']
    

    #The code that google sends in case of a successful authentication
    code = request.args.get('code')
    print "code "
    print code

    #print code

    if code and auth_token:
        #Set the redirect url on the token
        auth_token.redirect_uri = 'https://localhost:8000/contacts'

        #Generate the access token
        auth_token.get_access_token(code)

        session['google_auth_token'] = pickle.dumps(auth_token)

        #Populate a session variable indicating successful authentication
        session['GOOGLE_COOKIE_CONSENT'] = code
        print "DONE"


        

        #Redirect to your base page
        return redirect('/settings')


    #If user has not authenticated the app   
    return redirect('/settings')
