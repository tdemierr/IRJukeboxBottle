#!/usr/bin/env python
from flask import Flask, render_template, session, request, url_for, send_from_directory, send_file
from flask_socketio import SocketIO, emit
#from flask_bootstrap import Bootstrap

from getrelease import getRelease

import os
import xml.etree.ElementTree as ET

import threading
import time

import json, requests

from threading import Timer

from Disc import *
try:
    from IRManager import *
except:
    print "No lirc"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'

app.debug = False
async_mode = None
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.

thread = None
IRManager

#Bootstrap(app)
socketio = SocketIO(app, async_mode=async_mode)

listAlbums=[]

selectedRelease = 1
currentVolume = 0

def getImageUrl(url):
    resp = requests.get(url)
    print resp
    if resp.status_code == requests.codes.ok:
        data = json.loads(resp.text)
        if data["images"][0]["thumbnails"]["large"]:
            return data["images"][0]["thumbnails"]["large"]
        else:
            return None
    else:
        return None
def curPath():
    return os.getcwd() + os.path.sep

def downloadImage(url, id):
    try:
        r = requests.get(url)
        with open(curPath() +'CoverArt' + os.path.sep +id + '.jpg', "wb") as code:
            code.write(r.content)
        return True
    except:
        return False

def updateXML():
    print "exe"
    tree = ET.parse(curPath() +'Albums.xml')
    root = tree.getroot()
    global albums
    albums = root.findall('Album')
    for album in albums:
        id = album.find('id').text
        if album.find('Updated').text == 'Yes':
            album.find('Cover').text = id + '.jpg'
        if (id is not None) and (album.find('Updated').text != "Text") and (album.find('Updated').text != "Yes"):
            print id
            tracks, realease, artist = getRelease(id)
            tracksel = ET.SubElement(album, 'Tracks')
            album.find('Title').text =realease
            album.find('Artist').text =artist
            for track in tracks:
                  trackel = ET.SubElement(tracksel, 'Track')
                  titleel = ET.SubElement(trackel, 'Title')
                  titleel.text=track.title
                  durationel = ET.SubElement(trackel, 'Duration')
                  durationel.text=str(track.duration)

            album.find('Updated').text = "Text"
            CoverUrl=getImageUrl("http://coverartarchive.org/release/" + id)
            if CoverUrl is not None:
                if album.find('Updated').text is not "Yes":
                    downloadImage(CoverUrl, id)
                    album.find('Updated').text="Yes"

    tree.write(curPath+'output.xml', encoding="utf-8")


def parseXML():
    global listAlbums
    tree = ET.parse(curPath() +'output.xml')
    root = tree.getroot()
    global albums
    albums = root.findall('Album')
    for album in albums:
        lastDisc=Disc(album.find('Title').text, album.find('Artist').text, album.find('Cover').text, album.find('JukeboxId').text)
        listAlbums.append(lastDisc)
    listAlbums=sorted(listAlbums, key=lambda disc: disc.JukeboxID)


def background_thread():
    """Example of how to send server generated events to clients."""
    count = 0
    global selectedRelease
    while True:
        count += 1
        codeIR = IRManager.nextCode()
        if codeIR:
            print codeIR[0]
        socketio.sleep(1)

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

def url_cover(endpoint, **values):
    if endpoint == 'CoverArt':
            filename = values.get('filename', None)
            if filename and file is not 'None':
                return  '/' + endpoint + '/' + filename
            else:
                return '/' + endpoint + '/' + 'vinyl.png'

@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode, listAlbums=listAlbums)

@app.route('/CoverArt/<path:filename>')
def sendfile(filename):
    return send_from_directory(os.getcwd()+ os.path.sep +"CoverArt",
                               filename)

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
    global IRManager
    IRManager.sendPowerAmp()

@socketio.on('cd', namespace='/test')
def cd():
    global IRManager
    if IRManager.jukeboxPower == 0:
        IRManager.sendPowerCD()
        IRManager.jukeboxPower = 1
    IRManager.sendChangeCD()


@socketio.on('platine', namespace='/test')
def platine():
    global IRManager
    IRManager.sendChangeLinePlatine()

@socketio.on('volmoins', namespace='/test')
def volmoins():
    global IRManager
    IRManager.sendVolMoins()

@socketio.on('volplus', namespace='/test')
def volplus():
    global IRManager
    IRManager.sendVolPlus()

@socketio.on('disqueplus', namespace='/test')
def disqueplus(message):
    selectedReleaseID = int(message)
    print "Sel:",selectedReleaseID
    socketio.emit('AlbumCoverCurrent', {'data': url_cover('CoverArt', filename=listAlbums[getNext(selectedReleaseID)].Cover)}, broadcast=True, namespace='/test')
    socketio.emit('AlbumCoverCurrentID', {'data': listAlbums[getNext(selectedReleaseID)].JukeboxID}, broadcast=True, namespace='/test')
    socketio.emit('AlbumCoverPrevious', {'data': url_cover('CoverArt', filename=listAlbums[indexMatching(listAlbums, lambda x: x.JukeboxID == selectedReleaseID)].Cover)}, broadcast=True, namespace='/test')
    socketio.emit('AlbumCoverNext', {'data': url_cover('CoverArt', filename=listAlbums[getNext2(selectedReleaseID)].Cover)}, broadcast=True, namespace='/test')

@socketio.on('disquemoins', namespace='/test')
def disquemoins(message):
    selectedReleaseID = int(message)
    socketio.emit('AlbumCoverCurrent', {'data': url_cover('CoverArt', filename=listAlbums[getPrevious(selectedReleaseID)].Cover)}, broadcast=True, namespace='/test')
    socketio.emit('AlbumCoverCurrentID', {'data': listAlbums[getPrevious(selectedReleaseID)].JukeboxID}, broadcast=True, namespace='/test')
    socketio.emit('AlbumCoverPrevious', {'data': url_cover('CoverArt', filename=listAlbums[getPrevious2(selectedReleaseID)].Cover)}, broadcast=True, namespace='/test')
    socketio.emit('AlbumCoverNext', {'data': url_cover('CoverArt', filename=listAlbums[indexMatching(listAlbums, lambda x: x.JukeboxID == selectedReleaseID)].Cover)}, broadcast=True, namespace='/test')


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread, selectedRelease
    socketio.emit('AlbumCoverCurrent', {'data': url_cover('CoverArt', filename=listAlbums[indexMatching(listAlbums, lambda x: x.JukeboxID == selectedRelease)].Cover)}, broadcast=True, namespace='/test')
    socketio.emit('AlbumCoverCurrentID', {'data': selectedRelease}, broadcast=True, namespace='/test')
    socketio.emit('AlbumCoverPrevious', {'data': url_cover('CoverArt', filename=listAlbums[getPrevious(selectedRelease)].Cover)}, broadcast=True, namespace='/test')
    socketio.emit('AlbumCoverNext', {'data': url_cover('CoverArt', filename=listAlbums[getNext(selectedRelease)].Cover)}, broadcast=True, namespace='/test')
    if thread is None:
        thread = socketio.start_background_task(target=background_thread)
   # emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('AlbumSelect', namespace='/test')
def albumSelect(message):
    global IRManager
    albumID = int(message)
    session['receive_count'] = session.get('receive_count', 0) + 1

    socketio.emit('AlbumCoverCurrent', {'data': url_cover('CoverArt', filename=listAlbums[indexMatching(listAlbums, lambda x: x.JukeboxID == albumID)].Cover)}, broadcast=True, namespace='/test')
    socketio.emit('AlbumCoverPrevious', {'data': url_cover('CoverArt', filename=listAlbums[getPrevious(albumID)].Cover)}, broadcast=True, namespace='/test')
    socketio.emit('AlbumCoverNext', {'data': url_cover('CoverArt', filename=listAlbums[getNext(albumID)].Cover)}, broadcast=True, namespace='/test')

    IRManager.changeDisc(albumID)
    #emit('AlbumCoverPrevious', {'data': getPrevious(albumID),  'count': 0})
    #emit('AlbumCoverNext', {'data': getNext(albumID),  'count': 0})

def indexMatching(seq, condition):
    for i,x in enumerate(seq):
        if condition(x):
            return i
    return -1

def getNext(id):
    global listAlbums
    if indexMatching(listAlbums, lambda x: x.JukeboxID == id) >= len(listAlbums)-1:
        return 0
    else:
        return indexMatching(listAlbums, lambda x: x.JukeboxID == id)+1

def getNext2(id):
    global listAlbums
    if indexMatching(listAlbums, lambda x: x.JukeboxID == id) == len(listAlbums)-1:
        return 1
    elif indexMatching(listAlbums, lambda x: x.JukeboxID == id) == len(listAlbums)-2:
        return 0
    else:
        return indexMatching(listAlbums, lambda x: int(x.JukeboxID) == id)+2

def getPrevious(id):
    global listAlbums
    if indexMatching(listAlbums, lambda x: int(x.JukeboxID) == id) == 0:
        return len(listAlbums)-1
    else:
        return indexMatching(listAlbums, lambda x: int(x.JukeboxID) == id)-1

def getPrevious2(id):
    global listAlbums
    if indexMatching(listAlbums, lambda x: x.JukeboxID == id) == 0:
        return len(listAlbums)-2
    elif indexMatching(listAlbums, lambda x: x.JukeboxID == id) == 1:
        return len(listAlbums)-1
    else:
        return indexMatching(listAlbums, lambda x: int(x.JukeboxID) == id)-2

def __init__():
    print "init"
    global IRManager
    updateXML()
    parseXML()
    IRManager = IRManager("AMP", "CDJUKEBOX")
    thread = None
    print ("launch server")
    socketio.run(app, host='0.0.0.0', debug=True)



if __name__ == '__main__':

    __init__()
