from flask import Flask 
from flask import render_template
import redis

def connect_db():
    conexion = redis.StrictRedis(host='127.0.0.1',port=6379,db=0)
    if (conexion.ping()):
        print ('conectado al servidor de redis')
    else:
        print ('error..')
    return conexion

app = Flask (__name__)

@app.route('/')
def index():
    con = connect_db()
    #con.mset ({'The Mandalorian':'disponible','The Child':'disponible','The Sin':'disponible','Sanctuary':'disponible','The Gunslinger':'disponible','The Prisoner':'disponible','The Reckoning':'disponible','Redemption':'disponible'})
    return render_template ('/index.html')

@app.route('/listado')
def about():
    con = connect_db()
    return str(con.keys ('*'))

if __name__ == '__main__':
    app.run(host='localhost',port='5000', debug=False)

