from flask import Flask, render_template, request,redirect,url_for,jsonify
from flask.ext.cors import CORS
from OpenSSL import SSL
import requests
import json
import gdata.gauth
import gdata.contacts.client
import pickle
import gdata.contacts.service
from data_classes import feed_save
import rethinkdb as r

app=Flask(__name__)
CORS(app)
app.secret_key='akshaytaggem '
import google_login
from google_login import session
import test
from models import dbSetUp
import mail
import api
import contactsAPI
#SSL  temporary
context = SSL.Context(SSL.SSLv23_METHOD)
context.use_privatekey_file('server.key')
context.use_certificate_file('server.crt')
dbSetUp()


notification=[{ "item": { "time":123 , "user":"akshay"} }]

notification=json.dumps(notification)
msg="Welcome to Dashboard. Here you can find all your shared stuffs. We keep it safe here."
# dbSetUp()

@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_error/404.html')


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method=='GET':
            return render_template('login.html')
    
     

@app.route('/dashboard')
def dashboard():

    return render_template('dashboard1.html',notification=notification,profile_pic=session['profile'],name=session['name'],msg=msg)



@app.route('/settings')
def settings():
        if 'google_contact_synced' in session:
            return render_template('settings.html',profile_pic=session['profile'],name=session['name'],sync=True,id=session['google_contact_synced'])

	if 'GOOGLE_COOKIE_CONSENT' in session:
            auth_token=pickle.loads(session['google_auth_token'])
            print (dir(auth_token))
            print (auth_token.token_expiry)
            print((gdata.contacts.client.DEFAULT_BATCH_URL))

    		#Create a data client, in this case for the Contacts API
            gd_client = gdata.contacts.client.ContactsClient()
            #client=gdata.contacts.service.ContactsService(source='taggem')
    		#Authorize it with your authentication token
            auth_token.authorize(gd_client)
            query = gdata.contacts.client.ContactsQuery()
            query.max_results = 10000000

            # query.alt = 'json'

    		# #Get the data feed

            feed = gd_client.GetContacts(q=query)

           
            print  (feed.entry)
            print  len(feed.entry)
            contact_list=[]
            for entry in feed.entry:
                if not entry.name is None:
                    family_name = entry.name.family_name is None and " " or entry.name.family_name.text
                    full_name = entry.name.full_name is None and " " or entry.name.full_name.text
                    given_name = entry.name.given_name is None and " " or entry.name.given_name.text
                    # print  full_name
                

                    for email in entry.email:
                        if email.primary and email.primary == 'true':
                            # print '    %s' % (email.address)
                            contact={'name':full_name,'email':email.address}
                            contact_list.append(contact)

            # print contact_list
            connection=r.connect(host='localhost',port=28015)
            count=r.db('taggem').table('contacts').filter({'user_id':session['logged_user_ID']}).count().run(connection)
            if count >0:
                id=list(r.db('taggem').table('user').filter({'user_id':session['logged_user_ID']}).run(connection))[0]['id']
            else :
                r.db('taggem').table('contacts').insert({'user_id':session['logged_user_ID'],'contacts':contact_list}).run(connection)
                user=list(r.db('taggem').table('user').filter({'user_id':session['logged_user_ID']}).run(connection))
                print ("Contacts saved in database")
                id=user[0]['id']
            connection.close()
            session['google_contact_synced']=id
            print id

            return render_template('settings.html',profile_pic=session['profile'],name=session['name'],sync=True,id= session['google_contact_synced'])


        connection=r.connect(host='localhost',port=28015)
        count=r.db('taggem').table('contacts').filter({'user_id':session['logged_user_ID']}).count().run(connection)
        if count >0:
            id=list(r.db('taggem').table('user').filter({'user_id':session['logged_user_ID']}).run(connection))[0]['id']
        else :
            r.db('taggem').table('contacts').insert({'user_id':session['logged_user_ID'],'contacts':contact_list}).run(connection)
            user=list(r.db('taggem').table('user').filter({'user_id':session['logged_user_ID']}).run(connection))
            print ("Contacts saved in database")
            id=user[0]['id']
        connection.close()
        id=id.replace(' ','')
        if id!='':
            session['google_contact_synced']=id
            sync=False
            print id
            return render_template('settings.html',profile_pic=session['profile'],name=session['name'],sync=True,id= session['google_contact_synced'])
        else:

            return render_template('settings.html',profile_pic=session['profile'],name=session['name'],sync=False)

@app.route('/feed')
def feed():
    return render_template('discover1.html',profile_pic=session['profile'],name=session['name'])


@app.route('/signup')
def signup():
	return redirect(url_for('login'))





@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))



@app.route('/newsfeed')
def newsfeed():
    print "TEST:::::::::::"
    feed_list=[]
    connection=r.connect(host='localhost',port=28015)
    feed_db=r.db('taggem').table('post').filter({'user_id':'akshaynathr@gmail.com'}).order_by(r.asc('date')).run(connection)
    count=r.db('taggem').table('post').filter({'user_id':'akshaynathr@gmail.com'}).run(connection)
    print feed_db
    for f in feed_db:
        feed_list.append(f)
    #     print "A"
    # feed={'img_url':'http://girltalkhq.com/wp-content/uploads/2013/09/Image-11.jpg', 'link':'http://www.google.com', 'title':'Colors and paints','text':'Learn more about colors and arts'}
    # feed2={'img_url':'http://girltalkhq.com/wp-content/uploads/2013/09/Image-11.jpg', 'link':'http://www.google.com', 'title':'Colors and paints','text':'Learn more about colors and arts'}
  
    # feed_list.append(feed)
    # feed_list.append(feed2)
    feedJSON=jsonify({'feed':feed_list})


    return feedJSON




@app.route('/obj')
def obj():
    connection=r.connect(host='localhost',port=28015)

    new_feed=feed_save(id="123456",link='http://www.google.com',title='Test Link',text="Blah blah blah",img_url="http://img",connection=connection)
    output=new_feed.save_to_db()

    return  str(output)


@app.route('/auth',methods=['POST'])
def auth():
    data=request.get_json()
    print data
    id=data['id']
    connection=r.connect(host='localhost',port=28015)
    count=r.db('taggem').table('user').filter({'id':id}).count().run(connection)
    if count > 0:
        return "1"
    else :
        return "0"


