import recipe
import metaInfo
import MySQLdb
import MySQLdb.cursors



# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
import json


# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import flask

# configuration
DATABASE = "ec2-54-219-48-12.us-west-1.compute.amazonaws.com"
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
def connect_db():
	

	conn = MySQLdb.connect(host=DATABASE, port=3306, user='test_user',
						   passwd='mypass', db='Test1234',
						   cursorclass=MySQLdb.cursors.DictCursor)
	print "CONNECTION: \n\n\n"

	return conn

@app.before_request
def before_request():
   try:
	  g.db = connect_db()
   except:
	  print "passed..."
	
@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()


@app.route('/')
def homepage():
	return "Welcome home!"

@app.route('/get_ingredients')
def get_ingredients():
	# execute Query
	cur = g.db.cursor()
	cur.execute("SELECT * FROM ingredients")
	
	print "\n\n\n"

	ingredients = [(x['name'], x['type']) for x in cur.fetchall()] 
	
	return render_template('ingredients.html',  **{'ingredients': ingredients})


@app.route('/user_ratings/<int:id>')
def view_ratings(id):
	from neural_net import *
	x = build_net_for_user(id, g.db)
	return x

@app.route('/recipe/<int:id>')
def view_recipe(id):
   query = "SELECT * FROM recipes WHERE ID = " + str(id)  # Please don't SQL inject me
   d = {}
   d['name'] = "SAUCE ON SAUCE ON SAUCE"
   d['ingredients'] = ['sauce', 'saws']
   return flask.jsonify(d)


@app.route('/recommendations')
def recommendations():
   dummy = [ {"id": x, "name": "name " + str(x)} for x in range( 0, 10 ) ]
   # can't use flask.jsonify because it won't take a list
   return flask.Response(json.dumps( dummy ),  mimetype='application/json')


@app.route('/current_user')
def current_user():
   """if the session is logged in, return an object containing the user
      data. Else return an empty object"""
   
   response = None  
   r_code = 200  
   d = {}

   if "username" in session:
	  d = {"username": request.session.username}
   else:
	  d = {}
	  r_code = 401 # unauthorized 401

   response = flask.jsonify( d )
   response.headers[ "Status" ] = r_code 
   return response


@app.route("/login", methods=["POST"])
def login():
   try_pword = request.form["password"]
   
   r_code = 200
   d = {}

   query = """SELECT COUNT(*) AS matched FROM users WHERE password=MD5("%s")""" % try_pword
   cur = g.db.cursor()
   cur.execute(query)
   
   num_matches = cur.fetchone()["matched"]
   
   if num_matches == 0:
	  r_code = 401 
	  d = {"error": "bad password"}
   else:
	  r_code = 401  # unauthorized
	  d = {"status": "ok"}


   response = flask.jsonify( d )
   response.headers["status"] = r_code

   return response
   

@app.route("/user_create", methods=["POST"])
def user_create():
   uname = request.form["username"]
   password = request.form["password"]

   query = """INSERT INTO users(username, password) VALUES("%s", MD5("%s"))""" % (uname, password)
    

   return query
	  

if __name__ == '__main__':
	app.run()
