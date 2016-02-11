from settings import *
import urls

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run('127.0.0.1', 8000)
