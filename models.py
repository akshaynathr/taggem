import rethinkdb as r
from rethinkdb.errors import RqlRuntimeError


#database setup function

def dbSetUp():
    connection=r.connect(host='localhost',port=28015)
    try:
        r.db_create('taggem').run(connection)
        r.db('taggem').table_create('test').run(connection)
        print("Database setup completed")
    except RqlRuntimeError:
        print("Database already exist")
    finally:
        connection.close()

