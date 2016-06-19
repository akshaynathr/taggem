import rethinkdb as r


def authorize_id(id):
    connection=r.connect(host="localhost",port=28015)

    count=r.db('taggem').table('user').filter({'id':id}).count().run(connection)
    if count > 0:
        return 1
    else :
        return 0
