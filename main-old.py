from gevent import monkey; monkey.patch_all()
from bottle import Bottle, route, run, template, get, ServerAdapter, WSGIRefServer,request
import xml.etree.ElementTree as ET
import json
import logging
import musicbrainz2.webservice as ws
import musicbrainz2.utils as u
import musicbrainzngs as mb

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


items = {1: 'first item', 2: 'second item'}
items2 = {10: 'first item', 20: 'second item'}


from threading import Thread
import time

    # a simple json test main page
@route('/')
def jsontest():
    return template('index', request=request, a=items)

@route('/getallitems.json')
def shop_aj_getallitems():
        return (items)

@route('/_add_numbers')
def add_numbers():
    """Add two numbers server side, ridiculous but well..."""
    a = request.params.get('a', 0, type=int)
    b = request.params.get('b', 0, type=int)
    return json.dumps({'result': a+b})

class MyServer(WSGIRefServer):
    def run(self, app): # pragma: no cover
        from wsgiref.simple_server import WSGIRequestHandler, WSGIServer
        from wsgiref.simple_server import make_server
        import socket

        class FixedHandler(WSGIRequestHandler):
            def address_string(self): # Prevent reverse DNS lookups please.
                return self.client_address[0]
            def log_request(*args, **kw):
                if not self.quiet:
                    return WSGIRequestHandler.log_request(*args, **kw)

        handler_cls = self.options.get('handler_class', FixedHandler)
        server_cls  = self.options.get('server_class', WSGIServer)

        if ':' in self.host: # Fix wsgiref for IPv6 addresses.
            if getattr(server_cls, 'address_family') == socket.AF_INET:
                class server_cls(server_cls):
                    address_family = socket.AF_INET6

        srv = make_server(self.host, self.port, app, server_cls, handler_cls)
        self.srv = srv ### THIS IS THE ONLY CHANGE TO THE ORIGINAL CLASS METHOD!
        srv.serve_forever()

    def shutdown(self): ### ADD SHUTDOWN METHOD.
        self.srv.shutdown()
        # self.server.server_close()

def begin():
    run(server=server)

server = MyServer(host="0.0.0.0", port=8080)
Thread(target=begin).start()
time.sleep(10)
items=items2
time.sleep(20) # Shut down server after 2 seconds
server.shutdown()

#@route('/login', method='POST')
#def do_login():
#   return "<p>Your login information was correct.</p>"

def fetchAlbumInfo(id):
    try:
        #mb.set_useragent('IRJukebox','0.1.0', 'timotheed@gmail.com')
        #release=mb.get_release_by_id(id)
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
        print 'NO'
       # result = fetchAlbumInfo(album.find('id').text)
       # if result.get('disc'):
        #    print(result['disc'])
            #print(result['artist'], id)

    id = album.find('id').text
    artist = album.find('Artist').text



