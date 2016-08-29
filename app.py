#!/usr/bin/env python
from flask import Flask, render_template, session, request, url_for
from flask_socketio import SocketIO, emit, join_room, leave_room, \
    close_room, rooms, disconnect
from flask_bootstrap import Bootstrap

import os
import xml.etree.ElementTree as ET

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
Bootstrap(app)
socketio = SocketIO(app, async_mode=async_mode)
thread = None

def parseXml():
    tree = ET.parse('Albums.xml')
    root = tree.getroot()
    global albums
    albums = root.findall('Album')

def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    while True:
        socketio.sleep(10)
        count += 1
        socketio.emit('my response',
                      {'data': 'Server generated event', 'count': count},
                      namespace='/test')

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('my ping', namespace='/test')
def ping_pong():
    emit('my pong')

@socketio.on('ValSlider1', namespace='/test')
def value(message):
    session['receive_count'] = session.get('receive_count', 0) + 1
    print message
    emit('ValSlider1Change',
         {'data':  message},
         broadcast=True)

@socketio.on('power', namespace='/test')
def power_amp():
    print "amp"

@socketio.on('cd', namespace='/test')
def power_amp():
    print "cd"

@socketio.on('platine', namespace='/test')
def power_amp():
    print "platine"

@socketio.on('volmoins', namespace='/test')
def power_amp():
    print "volmoins"

@socketio.on('volplus', namespace='/test')
def power_amp():
    print "volplus"


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    #if thread is None:
        #thread = socketio.start_background_task(target=background_thread)
   # emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', debug=True)
