import MySQLdb
import MySQLdb.cursors

def init():
	db = MySQLdb.connect(host="ec2-54-219-48-12.us-west-1.compute.amazonaws.com",user="test_user",passwd="mypass")
	cur = db.cursor()
	cur.execute('CREATE DATABASE IF NOT EXISTS prod')
def createIngredients():
	db = MySQLdb.connect(host="ec2-54-219-48-12.us-west-1.compute.amazonaws.com",user="test_user",passwd="mypass",db="prod")
	cur = db.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS ingredients (id INT AUTO_INCREMENT, name CHAR(30), type CHAR(30), UNIQUE KEY (name), PRIMARY KEY (id))')

def createRecipes():
	db = MySQLdb.connect(host="ec2-54-219-48-12.us-west-1.compute.amazonaws.com",user="test_user",passwd="mypass",db="prod")
	cur = db.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS recipes (id INT AUTO_INCREMENT, name CHAR(30) UNIQUE, votes INT NOT NULL, salty INT NOT NULL, sweet INT NOT NULL, spicy INT NOT NULL, savory INT NOT NULL, filling INT NOT NULL, cuisine CHAR(30) NOT NULL, PRIMARY KEY (id))')

def createUsers():
	db = MySQLdb.connect(host="ec2-54-219-48-12.us-west-1.compute.amazonaws.com",user="test_user",passwd="mypass",db="prod")
	cur = db.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT, name CHAR(30), password CHAR(32), UNIQUE KEY (name), PRIMARY KEY (id))')

def createRatings():
	db = MySQLdb.connect(host="ec2-54-219-48-12.us-west-1.compute.amazonaws.com",user="test_user",passwd="mypass",db="prod")
	cur = db.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS userratings (userid INT NOT NULL, recipeid INT NOT NULL, score INT NOT NULL)')

def createRecipecombo():
	db = MySQLdb.connect(host="ec2-54-219-48-12.us-west-1.compute.amazonaws.com",user="test_user",passwd="mypass",db="prod")
	cur = db.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS recipecombo (recipeid INT NOT NULL, ingredientid INT NOT NULL)')
def populate():
	db = MySQLdb.connect(host="ec2-54-219-48-12.us-west-1.compute.amazonaws.com",user="test_user",passwd="mypass",db="prod", cursorclass=MySQLdb.cursors.DictCursor)
	cur = db.cursor()
	cur.execute("INSERT INTO recipes (name,votes,salty,sweet,spicy,savory,filling,cuisine) VALUES ('moms_spagetti','200','10','10','10','10','10','super')")
	cur.execute("INSERT INTO users (name,password) VALUES ('Ben', md5('benlovesboys')),('Sean',md5('kettle'))")
	cur.execute("INSERT INTO ingredients (name, type) VALUES ('salt','spice'),('pepper','spice'),('spagetti','starch'),('scott_tenormans_parents','long pig'),('tomato_sauce','sauce')")
	cur.execute("SELECT id FROM recipes WHERE name = 'moms_spagetti'")
	cur.fetchone()
	cur.execute("COMMIT")



def main():
	init()
	createIngredients()
	createRecipes()
	createUsers()
	createRatings()
	createRecipecombo()
	populate()
	# SALTY SWEET SPICY SAVORY FILLING CUISINE

main()
