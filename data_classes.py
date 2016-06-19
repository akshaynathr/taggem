import rethinkdb as r
class feed_save:
        def __init__(self,id,link,connection,recepients,title='',text='',img_url=''):
		self.user_id=id
		self.title=title
		self.text=text
		self.img_url=img_url
		self.link=link
		self.connection=connection
		self.recepients=recepients

	def save_to_db(self):

                s=r.db('taggem').table('post').insert({'date':r.now(),'user_id':self.user_id,'title':self.title, 'text':self.text, 'img_url':self.img_url, 'link':self.link,'sent_to':self.recepients}).run(self.connection)
		connection=self.connection
		connection.close()
		return s




class user_save:
	def __init__(self,user_id,connection,full_name='',profile_url=''):
		self.user_id=user_id
		self.connection=connection
		self.full_name=full_name
		self.profile_url=profile_url


	def save_to_db(self):
		s=r.db('taggem').table('user').insert({'date':r.now(),'user_id':self.user_id,'full_name':self.full_name,'profile_url':self.profile_url}).run(self.connection)
		connection=self.connection
		connection.close()
		return s

