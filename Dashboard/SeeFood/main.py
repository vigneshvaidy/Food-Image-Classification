import logging

from flask import Flask,render_template,request
from cassandra.cluster import Cluster
from recipe_scraper import find_recipes

app = Flask(__name__)


@app.route('/')
def hello():
	return render_template('calorie_chart.html')

@app.route('/nutrients')
def calc_nutrients():
	food_label = request.args.get('label')
	keyspace = 'seefood'
	table='nutrients'
	cluster_seeds = ['35.223.238.242']
	cluster = Cluster(cluster_seeds,port=9042)
	session = cluster.connect(keyspace)

	rows = session.execute("SELECT * from "+table+" where food_item = '"+food_label+"'")
	for row in rows:
		return render_template('nutrient_chart.html',data = food_label) 
		#str((row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12],row[13],row[14]))	

@app.route('/restaurants')
def find_restaurants():
	food_label = request.args.get('label')
	keyspace = 'seefood'
	table='restaurant'
	cluster_seeds = ['35.223.238.242']
	cluster = Cluster(cluster_seeds,port=9042)
	session = cluster.connect(keyspace)

	rows = session.execute("SELECT * from "+table+" where food_item = '"+food_label+"' ALLOW FILTERING")
	record_list = []
	for row in rows:
		record_list.append(str((row[0],row[1],row[2],row[3],row[4],row[5])))
	
	return render_template('business_visual.html',data = food_label)



@app.route('/recipes')
def search_recipes():
	food_label = request.args.get('label')
	list_dishes = find_recipes(food_label)
	return(str(list_dishes[0][1]))
	return "Recipe Stuff : {}".format(food_label)
	return render_template('image_card.html',data = food_label)

@app.errorhandler(500)
def server_error(e):
	logging.exception('An error occurred during a request.')
	return """
	An internal error occurred: <pre>{}</pre>
	See logs for full stacktrace.
	""".format(e), 500


if __name__ == '__main__':
	# This is used when running locally. Gunicorn is used to run the
	# application on Google App Engine. See entrypoint in app.yaml.
	app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_flex_quickstart]