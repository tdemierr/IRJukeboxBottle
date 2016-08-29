from flask import Flask, render_template
from flask_socketio import SocketIO, emit

import xml.etree.ElementTree as ET

from gevent.wsgi import WSGIServer
from threading import Thread
import time

albums = None
thread = None

app = Flask(__name__)
app.debug = True
#app.use_reloader=True

socketio = SocketIO(app)

values = {
    'slider1': 25,
    'slider2': 0,
}


def parseXml():
    tree = ET.parse('Albums.xml')
    root = tree.getroot()
    global albums
    albums = root.findall('Album')

@app.route('/')
def index():
    #global thread
    #if thread is None:
    #    thread = Thread(target=boucle)
     #   thread.start()
    return render_template('index.html', **values)

def boucle():
    time.sleep(1)
    print("hello")
    time.sleep(2)

@app.route('/Choix')
def choix():
    print "Choix Fait"
    return render_template('index.html', **values)

@socketio.on('connect')
def connect(message):
    print message

@socketio.on('value changed')
def value_changed(message):
    print "Change"
    values[message['who']] = message['data']
    print message
    emit('update value', message, broadcast=True)



if __name__ == '__main__':
    parseXml()
    socketio.run(app, host='0.0.0.0')
    print("Test")


