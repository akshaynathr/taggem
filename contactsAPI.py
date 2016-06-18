from api import api
import rethinkdb as r
from flask_restful import Resource
from flask import request


def authenticate(id):
	conn=r.connect(host='localhost',port=28015)
	count=r.db('taggem').table('user').filter({'id':id}).count().run(conn)
	user=list(r.db('taggem').table('user').filter({'id':id}).run(conn))
	if count>0:
		user_id= user[0]['user_id']
		conn.close()
		return user_id
	else:
		return ''
	
class contactsfeed(Resource):

	def post(self):
		data=request.get_json()
		print data
		id=data['id']
		access=authenticate(id)
		if access != '' :
			conn=r.connect(host='localhost',port=28015)
			contacts=list(r.db('taggem').table('contacts').filter({'user_id':access}).run(conn))
			conn.close()
			return {'result':contacts}


		else:
			return {'result':'Error'}


api.add_resource(contactsfeed,'/contacts')