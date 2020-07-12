import sys, uuid
assert sys.version_info >= (3, 5) # make sure we have Python 3.5+
from cassandra.cluster import Cluster

from pyspark.sql import SparkSession, functions, types
spark = SparkSession.builder.appName('business').getOrCreate()

cluster_seeds = ['35.223.238.242','23.236.62.240','35.223.125.82']
keyspace = 'seefood'
table='restaurant'
spark = SparkSession.builder.appName('Load restaurant information to cassandra') \
	.config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()

assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext

def main(inputs):
	session = Cluster(cluster_seeds).connect(keyspace)
	with open('labels.txt') as label_file:
		labels = label_file.read().splitlines()

	filter_cond = ""
	for label in labels:
		filter_cond += " like '%"+label+"%' OR categories"

		
	filter_cond = filter_cond[:-13]


	input_data = spark.read.json(inputs)

	input_data.createOrReplaceTempView("business_table")
	filtered_df = spark.sql("SELECT lower(categories) as food, * FROM business_table where categories"+filter_cond+"")

	new_df = filtered_df.withColumn('food_item', functions.regexp_extract('food', '|'.join(labels), 0))
	new_df.createOrReplaceTempView('food_rating')
	
	food_df = spark.sql("SELECT food_item as dish,MAX(stars) AS max_rating FROM food_rating GROUP BY food_item")
	food_df.createOrReplaceTempView('temp_table')
	
	#get the top restaurants based on food type
	recommendation_df = spark.sql("SELECT food_item,name as restaurant_name,address,latitude, longitude from food_rating JOIN temp_table ON food_rating.food_item = temp_table.dish AND food_rating.stars = temp_table.max_rating GROUP BY food_item,name,address, latitude, longitude")
	recommendation_df = recommendation_df.withColumn("id", functions.monotonically_increasing_id())

	recommendation_df.write.format("org.apache.spark.sql.cassandra").options(table=table, keyspace=keyspace).save()
	session.shutdown() #close the session after all records have been inserted

if __name__ == '__main__':
	inputs = sys.argv[1]
	main(inputs)
