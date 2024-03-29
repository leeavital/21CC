import recipe
import metaInfo
import MySQLdb
import MySQLdb.cursors

import sys



# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
	 abort, render_template, flash
import json
import flask

import auth


# configuration
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

	return conn

@app.before_request
def before_request():
     
   g.db = connect_db()
	
@app.teardown_request
def teardown_request(exception):
	db = getattr(g, 'db', None)
	if db is not None:
		db.close()


app_text = open( "static/index.html" ).read() #wat

@app.route('/')
def homepage():
	return app_text

@app.route('/get_ingredients')
def get_ingredients():
	# execute Query
	cur = g.db.cursor()
	cur.execute("SELECT * FROM ingredients")
	
	print "\n\n\n"

	ingredients = [(x['name'], x['type']) for x in cur.fetchall()] 
	
	return render_template('ingredients.html',  **{'ingredients': ingredients})
   

@app.route('/recipes/recommendations')
def view_ratings():
	import neural_net as nn
	id = session['user_id']
	x = nn.build_net_for_user(id, g.db)
	if x == False:
		print "RETURNING FALSE"
		return flask.Response( json.dumps( {'message': 'Rate more recipes for recommendations'} ), mimetype='application/json' ), 418
	query = "SELECT * from recipes where id in " + str(tuple(x))
	cur = g.db.cursor()
	cur.execute(query)

	testRecipes =  cur.fetchall()

	testRecipes = [{'id': recipe['id'], 'ingredients': '',
					'name': (recipe['name'] + '(' + ing_string(get_ingredient_percentage(str(recipe['id']))) + ")"), 'description': None}
					for recipe in testRecipes]

   	
	return flask.Response( json.dumps( testRecipes ), mimetype='application/json' )


def get_ingredient_percentage(recipe_id):
	ings = []
	cur = g.db.cursor()
	query = "SELECT * FROM recipecombo where recipeid = '{0}'".format(recipe_id)
	cur.execute(query)
	rows = cur.fetchall()
	for row in rows:
		query = "SELECT strippedID FROM ingredients where id = '{0}'".format(row['ingredientid'])
		cur.execute(query)
		strippedID = cur.fetchone()['strippedID']
		sID = "SELECT * from strippedIngredients where id = '{0}'".format(strippedID)
		cur.execute(sID)
		ings.append(cur.fetchone()['name'])

	cur.execute(   "SELECT * FROM userinventory WHERE uid=%d" % session["user_id"] )  
	inven = [x['item'] for x in cur.fetchall()]
	print inven
	print ings
	return (float(len([x for x in inven if x in ings])) / float(len(ings)))

def ing_string(f):
	print f
	if f < .1:
		return "You have FEW ingredients"
	if f < .5:
		return "You have SOME ingredients"
	if f < .8:
		return "You have MANY ingredients"
	else:
		return "You have MOST ingredients"
@app.route('/recipes/training')
def get_training_recipes():
	query = "SELECT * from recipes order by rand() limit 10"
	cur = g.db.cursor()
	cur.execute(query)

	testRecipes =  cur.fetchall()

	testRecipes = [{'id': recipe['id'], 'ingredients': '',
					'name': recipe['name'], 'description': "Read the name"} for recipe in testRecipes]

   	
	return flask.Response( json.dumps( testRecipes ), mimetype='application/json' )



@app.route('/recipes/training/<int:recipe_id>/<int:rating>')
def rate_training_recipe(recipe_id, rating):
	print "SESSION"
	print session
	if rating != -1:
		values = (session['user_id'], recipe_id, rating)
		query = "INSERT INTO userratings(userid, recipeid, score) " +\
		 "VALUES(%d, %d, %d)" % values
	  
		cur = g.db.cursor()

		cur.execute(query)
		g.db.commit()

		return flask.jsonify( {"status" : "ok" } )

@app.route('/recipe/<int:id>')
def view_recipe(id):
	query = "SELECT * FROM recipes WHERE ID = '{0}'"   # Please don't SQL inject me
   	cur = g.db.cursor()
	d = {}
	cur.execute(query.format(id))
	z = cur.fetchone()
	d['name'] = z['name']
	# query = "SELECT name FROM recipecomboe WHERE recipeid='{0}'"
	query = "SELECT * FROM recipecombo JOIN ingredients ON ingredients.id=recipecombo.ingredientid WHERE recipecombo.recipeid={0}"
	cur.execute(query.format(id))

	d['ingredients'] = [x["name"] for x in cur.fetchall()]
	d['pic'] = z['imageurl']
	query = "SELECT * FROM recipetext WHERE recipeid={0}".format( id )
	cur.execute( query )
	d["description"] = cur.fetchone()["recipetexts"]

	d["id"] = id

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

   if "username" in session and "user_id" in session:
	  d = {"username": session["username"]}
   else:
	  d = {}
	  r_code = 401 # unauthorized 401

   response = flask.jsonify( d )
   return response, r_code


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

  
   try:
	  u = auth.log_user_in( try_uname, try_pword, session )
	  r_code = 200
	  d = {"status": "ok"}
   except Exception as e:
	  r_code = 301
	  d = {"error": str(e) }

	   
   response = flask.jsonify( d )

   return response, r_code
   

@app.route("/user_create", methods=["POST"])
def user_create():
   form = json.loads( request.data )
   uname = form["username"]
   password = form["password"]

   query = """INSERT INTO users(name, password) VALUES("%s", MD5("%s"))""" % (uname, password)
    
   g.db.cursor().execute( query )
   g.db.commit()

   u = auth.log_user_in( uname, password, session )

   return flask.jsonify( {"status": "ok"} ) 



@app.route("/inventory", methods=["GET", "PUT"])
def inventory():
   
   if request.method == "GET":
	  cur = g.db.cursor()
   	  cur.execute(   "SELECT * FROM userinventory WHERE uid=%d" % session["user_id"] )  
   	  
   	  

   	  r = flask.Response( json.dumps( cur.fetchall() ) )

   	  r.headers[ "Content-Type" ] = "text/javascript"
   	  return r

   elif request.method == "PUT":
	  item = request.data
	  query = """INSERT INTO userinventory(uid, item) VALUES(%d, "%s")""" % (session["user_id"], item)
	  
	  g.db.cursor().execute( query ) 
	  g.db.commit()

	  return flask.jsonify( {"status": "ok" } )

   else:
	  pass

@app.route( "/inventory/delete/<string:item>" )
def inventory_delete( item  ):
   query = """DELETE FROM userinventory WHERE uid=%d and item="%s" """
   query = query % ( session["user_id"], item )
   print query
   g.db.cursor().execute( query )
   g.db.commit()
   return flask.jsonify( {"status": "ok"} )

@app.route("/recipetiming")
def get_timing(recipeList):
        query = """SElECT * FROM recipes where id = "{0}" """
        cur = g.db.cursor()
        timeList = []
        templist = []
        for item in recipeList:
                cur.execute(query.format(item))
                templist.append((cur.fetchone()['name'],cur.fetchone()['cooktime']))
        sorted(templist,key=itemgetter(1),reverse=True)
        Max = templist[0][1]
        for item in templist:
                timeList.append((item[0],Max-item[1]))
        return timeList

if __name__ == '__main__':
	app.run()	
