from flask_restful import Resource ,Api 
from flask import request
from views import app
from Fetch import fetch
import rethinkdb as r
api=Api(app)

import mail
from data_classes import feed_save
from authorize import authorize_id
import rethinkdb as r

class MailSender(Resource):
	def post(self):
			
		#try:
                data=request.get_json()
                print data
                id=data['id']
                conn=r.connect(host='localhost',port='28015')
                user=list(r.db('taggem').table('user').filter({'id':id}).run(conn))
                print user
                name=user[0]['full_name']
            
                access=authorize_id(id)
                if access ==1:
                        recepient=data['recepient']
                        msg=data['msg']
                        link=data['link']
                        print recepient
                        print msg
                        print link
                        t=fetch(link,msg)
                        connection=r.connect(host='localhost',port='28015')
                        email='akshaynathr@gmail.com'
                        saved_feed=feed_save(id=email,link=t['link'],connection=connection,recepients=recepient,title=t['title'],text=t['description'],img_url=t['imageurl'])
                        result=saved_feed.save_to_db()
                        print result

                        mail.send_mail(recepient,msg,link,name=name)
                        print ("Mail sent")
                        return "done"
                else:
                        return "Error"
		#except Exception as e:
			




api.add_resource(MailSender,'/mail')
