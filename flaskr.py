import recipe
import metaInfo
import MySQLdb
import MySQLdb.cursors

import sys



# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
import json


# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import flask

# configuration
print sys.argv
if len(sys.argv) == 2 and sys.argv[ 1 ] == "debug":
   print "using debug..."
   DATABASE= "localhost"
   DEBUG = True
   SECRET_KEY = 'development key'
   USERNAME = 'root'
   PASSWORD = 'root'
   DB_USER = 'root'
   DB_PASS = 'root'
else:
   DATABASE = "ec2-54-219-48-12.us-west-1.compute.amazonaws.com"
   DEBUG = True
   SECRET_KEY = 'development key'
   USERNAME = 'admin'
   PASSWORD = 'default'
   DB_USER = "test_user"
   DB_PASS = 'mypass'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)
def connect_db():
	

	conn = MySQLdb.connect(host=DATABASE, port=3306, user=DB_USER,
						   passwd=DB_PASS, db='prod',
						   cursorclass=MySQLdb.cursors.DictCursor)
	print "CONNECTION: \n\n\n"

	return conn

@app.before_request
def before_request():
     
   g.db = connect_db()
	
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
	import neural_net as nn
	x = nn.build_net_for_user(id, g.db)
	return x

@app.route('/recipes/training')
def get_training_recipes():
	ids = tuple([x for x in range(1,12)])
	query = "SELECT * FROM recipes where id in " + str(ids)
	cur = g.db.cursor()
	cur.execute(query)

	testRecipes =  cur.fetchall()

	testRecipes = [{'id': recipe['id'], 'ingredients': ['Nothing Yet'],
					'name': recipe['name'], 'description': "Read the name"} for recipe in testRecipes]

   	
	return flask.Response( json.dumps( testRecipes ), mimetype='application/json' )



@app.route('/recipes/training/<int:recipe_id>/<int:rating>')
def rate_training_recipe(recipe_id, rating):
	if rating != -1:
		values = (session['user_id'], recipe_id, rating)
		# query = "INSERT INTO userratings VALUES( " + str(values) + ")"
		query = "INSERT INTO userratings(userid, recipeid, score) " +\
		 "VALUES(%d, %d, %d)" % values
	  
		cur = g.db.cursor()

		cur.execute(query)
		g.db.commit()

		return flask.jsonify( {"status" : "ok" } )

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
   
   
   # we have to use json.loads instead of request.form
   # because angularjs sends all post requests as 
   # multipart (???)
   form = json.loads( request.data )
   try_pword = form["password"]
   try_uname = form["username"]
   
   r_code = 200
   d = {}

   query = """SELECT COUNT(*) AS matched, name, id  FROM users WHERE password=MD5("%s") AND name="%s";""" % (try_pword, try_uname)
   cur = g.db.cursor()
  
   print query 
   cur.execute(query)
   
   match = cur.fetchone() 
   num_matches = match["matched"]
   matched_uname = match["name"]
   
   if num_matches == 0:
	  r_code = 401 
	  d = {"error": "bad password"}
   else:
	  session["username"] = match["name"]
	  session["user_id"] = match["id"]
	  r_code = 401  # unauthorized
	  d = {"status": "ok"}


   response = flask.jsonify( d )
   response.headers["status"] = r_code

   return response
   

@app.route("/user_create", methods=["POST"])
def user_create():
   form = json.loads( request.data )
   uname = form["username"]
   password = form["password"]

   query = """INSERT INTO users(name, password) VALUES("%s", MD5("%s"))""" % (uname, password)
    
   g.db.cursor().execute( query )
   g.db.commit()

   return flask.jsonify( {"status": "ok"} ) 

if __name__ == '__main__':
	app.run()
