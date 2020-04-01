from flask import Flask 
from flask import render_template
import redis

def connect_db():
    conexion = redis.StrictRedis(host='127.0.0.1',port=6379,db=0,charset="utf-8", decode_responses=True)
    if (conexion.ping()):
        print ('conectado al servidor de redis')
    else:
        print ('error..')
    return conexion

db = connect_db()

def inicializar():
    db.hmset('episodios',{
        1: 'The Mandalorian',
        2: 'The Child',
        3: 'The Sin',
        4: 'Sanctuary',
        5: 'The Gunslinger',
        6: 'The Prisoner',
        7: 'The Reckoning',
        8: 'Redemption'
    })
    db.hmset('episodiosP',{
        1: 123,
        2: 382,
        3: 99,
        4: 254,
        5: 391,
        6: 725,
        7: 412,
        8: 54
    })
    db.mset ({1:'disponible',2:'disponible',3:'disponible',4:'disponible',5:'disponible',6:'disponible',7:'disponible',8:'disponible'})

def limpiar():
    db.flushdb()

app = Flask (__name__)

@app.route('/')
def index():
    inicializar()
    nombres = db.hgetall('episodios')
    estados = db.mget(1,2,3,4,5,6,7,8)
    return render_template ('/index.html',estados = estados,nombres = nombres)

if __name__ == '__main__':
    app.run(host='localhost',port='5000', debug=False)

