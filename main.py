from bottle import route, run
@route('/')
def main():
	return "<h1>Test</h1>"

run(host='0.0.0.0', port=8080)
