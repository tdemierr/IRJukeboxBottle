#!/usr/bin/env python
from flask import Flask, render_template, session, request, url_for, send_from_directory, send_file
from flask_socketio import SocketIO, emit
#from flask_bootstrap import Bootstrap

from getrelease import getRelease

import os
import xml.etree.ElementTree as ET

import time

import json, requests

from Disc import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.debug=False
async_mode = None
# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.

#Bootstrap(app)
socketio = SocketIO(app, async_mode=async_mode)

listAlbums=[]

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


def downloadImage(url, id):
    try:
        r = requests.get(url)
        with open('CoverArt' + os.path.sep +id + '.jpg', "wb") as code:
            code.write(r.content)
        return True
    except:
        return False

def updateXML():
    print "exe"
    tree = ET.parse('Albums.xml')
    root = tree.getroot()
    global albums
    albums = root.findall('Album')
    for album in albums:
        id = album.find('id').text
        if album.find('Updated').text == 'Yes':
            album.find('Cover').text = id + '.jpg'
        if (id is not None) and (album.find('Updated').text != "Text") and (album.find('Updated').text != "Yes"):
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

    tree.write('output.xml', encoding="utf-8")


def parseXML():
    global listAlbums
    tree = ET.parse('output.xml')
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
    print os.getcwd()
    return send_from_directory('C:\Users\Tim\PycharmProjects\IRJukeboxBottle\CoverArt',
                               filename)
   # return send_file(url_for('static',filename=path), mimetype='image/png')
    #fullpath = "./CoverArt/" + path
    #resp = Flask.make_response(open(fullpath).read())
    #resp.content_type = "image/jpeg"
    #return resp
    #return send_from_directory(url_for('CoverArt', filename=str(path)))

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
def cd():
    print "cd"

@socketio.on('platine', namespace='/test')
def platine():
    print "platine"

@socketio.on('volmoins', namespace='/test')
def volmoins():
    print "volmoins"

@socketio.on('volplus', namespace='/test')
def volplus():
    print "volplus"

@socketio.on('disqueplus', namespace='/test')
def disqueplus():
    print "disqueplus"

@socketio.on('disquemoins', namespace='/test')
def disquemoins():
    print "disquemoins"


@socketio.on('connect', namespace='/test')
def test_connect():
    global thread
    #if thread is None:
        #thread = socketio.start_background_task(target=background_thread)
   # emit('my response', {'data': 'Connected', 'count': 0})


@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected', request.sid)


@socketio.on('AlbumSelect', namespace='/test')
def AlbumSelect(message):
    albumID = int(message)
    session['receive_count'] = session.get('receive_count', 0) + 1
    print url_cover('CoverArt', filename=listAlbums[indexMatching(listAlbums, lambda x: x.JukeboxID == albumID)].Cover)
    emit('AlbumCoverCurrent', {'data': url_cover('CoverArt', filename=listAlbums[indexMatching(listAlbums, lambda x: x.JukeboxID == albumID)].Cover)}, broadcast=True)
    print "JukeID:", albumID
    emit('AlbumCoverPrevious', {'data': url_cover('CoverArt', filename=getPrevious(albumID))}, broadcast=True)
    emit('AlbumCoverNext', {'data': url_cover('CoverArt', filename=getNext(albumID))}, broadcast=True)
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
        return listAlbums[0].Cover
    else:
        return listAlbums[indexMatching(listAlbums, lambda x: x.JukeboxID == id)+1].Cover

def getPrevious(id):
    global listAlbums
    if indexMatching(listAlbums, lambda x: x.JukeboxID == id) == 0:
        return listAlbums[len(listAlbums)-1].Cover
    else:
        return listAlbums[indexMatching(listAlbums, lambda x: x.JukeboxID == id)-1].Cover


def __init__():
    print "init"
    updateXML()
    parseXML()

    thread = None
    print ("launch server")
    socketio.run(app, host='0.0.0.0', debug=True)



if __name__ == '__main__':

    __init__()
