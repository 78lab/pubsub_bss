from flask import Flask
 
app = Flask(__name__)
 
@app.route('/')
@app.route('/index')
def index():
    return '''<!DOCTYPE HTML><html>
  <head>
    <title>Flask app</title>
  </head>
  <body>
    <h1>Hello Flask!</h1>
  </body>
</html>'''

@app.route('/about')
def about():
  return 'About 페이지!!'