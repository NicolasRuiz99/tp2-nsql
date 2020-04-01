from flask import Flask, request
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
    #inicializar()
    estados = {}
    for i in range (8):
        estados[str(i+1)] = db.get(i+1)
        if (estados[str(i+1)] == None):
            estados[str(i+1)] = 'disponible'
            db.set(i+1,'disponible')
    nombres = db.hgetall('episodios')
    precios = db.hgetall('episodiosP')
    return render_template ('/index.html',estados = estados,nombres = nombres,precios = precios)

@app.route('/reservar',methods=['GET'])
def reservar():
    nombre = ''
    ep = request.args.get('episodio')
    precio = request.args.get('precio')
    if (db.exists(ep)):
        estado = db.get(ep)
        if estado == 'disponible':
            nombre = db.hget('episodios',ep)
            if (precio == db.hget('episodiosP',ep)):
                resp = True
                db.set(ep,'reservado')
                db.expire(ep,240)
            else:
                resp = False
        else:
            resp = False
    else:
        resp = False
    return render_template ('/reservar.html',resp = resp,nombre = nombre,precio = precio,nro = ep)

@app.route('/alquilar',methods=['GET'])
def alquilar():
    ep = request.args.get('nro')
    precio = request.args.get('precio')
    if (db.exists(ep)):
        estado = db.get(ep)
        if estado != 'alquilado':
            if (precio == db.hget('episodiosP',ep)):
                resp = True
                db.set(ep,'alquilado')
                db.expire(ep,86400)
            else:
                resp = False
        else:
            resp = False
    else:
        resp = False
    return render_template ('/pago.html',resp = resp,nro = ep,precio = precio)

if __name__ == '__main__':
    app.run(host='localhost',port='5000', debug=False)

