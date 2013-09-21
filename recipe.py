class Recipe():

	 def __init__(self, title, metaInfo, ingredients, steps):
		self.title = title
		self.metaInfo = metaInfo
		self.ingredients = ingredients
		self.steps = steps

	 def __str__(self):
		return self.title
