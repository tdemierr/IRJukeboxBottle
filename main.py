from bottle import route, run, template, request
import xml.etree.ElementTree as ET
import sys
import logging
import musicbrainz2.webservice as ws
import musicbrainz2.utils as u
import musicbrainzngs as mb

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
@route('/')
def main(albums):
    output = template('index', data=albums)
    return output

def uploadEmpData():
data = request.files.get('file')
data.save('files/',overwrite=True)
if data and data.file:
    return json_dumps("File uploaded successfully")
return json_dumps({'error':'Permission Denied.'})

def uploadEmpDataT():
    data = request.get('choice')
    #data.save('files/',overwrite=True)
    if data:
        return json_dumps("File uploaded successfully")
    return json_dumps({'error':'Permission Denied.'})

def fetchAlbumInfo(id):
    try:
        mb.set_useragent('IRJukebox','0.1.0', 'timotheed@gmail.com')
        release=mb.get_release_by_id(id)
        #inc = ws.ReleaseIncludes(artist=True, releaseEvents=True, labels=True, discs=True, tracks=True, releaseGroup=True)
        #release = q.getReleaseById(id, inc)
        return release
    except ws.WebServiceError, e:
        print 'Error:', e

q = ws.Query()
tree = ET.parse('Albums.xml')
root = tree.getroot()
for album in root.findall('Album'):
    updated = album.find('Updated').text
    if updated != 'Yes':
       # result = fetchAlbumInfo(album.find('id').text)
        if result.get('disc'):
            print(result['disc'])
            #print(result['artist'], id)

    id = album.find('id').text
    artist = album.find('Artist').text



run(host='0.0.0.0', port=8080)
