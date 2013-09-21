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
	cur.execute("SELECT name FROM ingredients")
	
	print "\n\n\n"

	ingredients = [(x['name'], x['type']) for x in cur.fetchall()] 

	return render_template('ingredients.html',  **{'ingredients': ingredients})

@app.route('/recipe/<int:id>')
def view_recipe(id):
   query = "SELECT * FROM recipes WHERE ID = " + str(id)  # Please don't SQL inject me
   # cur = g.db.execute(query)
   d = {}
   d['name'] = "SAUCE ON SAUCE ON SAUCE"
   d['ingredients'] = ['sauce', 'saws']
   return flask.jsonify(d)


@app.route('/recommendations')
def recommendations():
   dummy = [ {"id": x, "title": "title " + str(x)} for x in range( 0, 10 ) ]
   # can't use flask.jsonify because it won't take a list
   return flask.Response(json.dumps( dummy ),  mimetype='application/json')


if __name__ == '__main__':
	app.run()
