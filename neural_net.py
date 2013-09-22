
def build_net_for_user(uID, connection):
	from pybrain.tools.shortcuts import buildNetwork
	from pybrain.supervised.trainers import BackpropTrainer
	from pybrain.datasets import SupervisedDataSet
	cur = connection.cursor()
	query = "SELECT * from users WHERE id = %d"% uID
	print query
	cur.execute(query)
	user = cur.fetchone()
	print user

	net = buildNetwork(6, 10, 1, bias = True)


	ds = SupervisedDataSet(6, 1)

	ratedRecipesQuery  = "SELECT * from userratings where userid = %d" % uID 
	cur.execute(ratedRecipesQuery)
	ratedRecipes = cur.fetchall()
	
	ratedRecipes2 = {}
	for x in ratedRecipes:
		print x
		ratedRecipes2[int(x['recipeid'])] = x['score']/10.0
	print ratedRecipes2.keys()
	recipeQuery = "SELECT * FROM recipes where id in " + str(tuple(ratedRecipes2.keys()))

	print recipeQuery
	cur.execute(recipeQuery)

	recipes = cur.fetchall()

	if len(recipes) < 4:
		return False

	for recipe in recipes:
		print "RECIPE IS: "+str(recipe)
		rating = ratedRecipes2[recipe['id']]
		print recipe
		scores = [recipe['salty'], recipe['savory'], recipe['spicy'] , recipe['filling'], recipe['sour'], recipe['sweet']]
		ds.addSample(scores, rating)

	print ds
	
	trainer = BackpropTrainer(net, ds)

	z = trainer.trainUntilConvergence(maxEpochs = 1000)
	print z

	while z[-1][-1] > .05:
		trainer = BackpropTrainer(net, ds)

		z = trainer.trainUntilConvergence(maxEpochs = 1000)	
		print z

	q = "SELECT * FROM recipes"
	cur.execute(q)
	d = {}
	for x in cur.fetchall():
		ans = net.activate([x['salty'], x['savory'], x['spicy'], x['filling'], x['sour'], x['sweet']])
		d[ans[0]] = x

	s = sorted(d.keys())
	print str(d[s[0]]['name'])

	return str([d[s[x]]['id'] for x in range(5)])

