import recipe
import metaInfo
import json


# all the imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import flask

# configuration
DATABASE = None  # put a DB here
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)

app.config.from_envvar('FLASKR_SETTINGS', silent=True)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])




@app.route('/')
def homepage():
	return "Welcome home!"

@app.route('/get_ingredients')
def get_ingredients():
	query = "SELECT * FROM ingredients"
	# execute Query
	# cur = g.db.execute(query)
	ingredients = ["Salt", "Pepper", "Oregano"] #fetchall
	return render_template('ingredients.html',  **{'ingredients': ingredients})

@app.route('/recipe/<int:id>')
def view_recipe(id):
   query = "SELECT * FROM recipes WHERE ID = " + str(id)  # Please don't SQL inject me
   # cur = g.db.execute(query)
   d = {}
   d['name'] = "SAUCE ON SAUCE ON SAUCE"
   d['ingredients'] = ['sauce', 'saws']
   return flask.jsonify(d)

if __name__ == '__main__':
    app.run()
