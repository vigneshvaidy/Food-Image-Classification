import sys,uuid
from cassandra.cluster import Cluster

assert sys.version_info >= (3, 5) # make sure we have Python 3.5+

from pyspark import SparkConf, SparkContext
from pyspark.sql import SparkSession, functions, types

cluster_seeds = ['35.223.238.242','23.236.62.240','35.223.125.82']
keyspace = 'seefood'
table='nutrients'
spark = SparkSession.builder.appName('Load Nutrients data to cassandra') \
	.config('spark.cassandra.connection.host', ','.join(cluster_seeds)).getOrCreate()

assert spark.version >= '2.4' # make sure we have Spark 2.4+
spark.sparkContext.setLogLevel('WARN')
sc = spark.sparkContext

def main(inputs):
	
	session = Cluster(cluster_seeds).connect(keyspace)
	nutrients_df = spark.read.format("CSV").option("header","true").load(inputs)
	nutrients_df = nutrients_df.fillna("0.0")

	# extract food label names
	with open('labels.txt') as label_file:
		labels = label_file.read().splitlines()

	#Create a filtering condition based on labels
	filter_cond = ""
	for label in labels:
		filter_cond += " like '%"+label+"%' OR food_name"

	filter_cond = filter_cond[:-13]	 


	nutrients_df.createOrReplaceTempView('nutrients')
	nutrients_df = spark.sql("SELECT id as food_id, LOWER(name) as food_name, FLOAT(calories) as calories, FLOAT(`protein (g)`) as proteins, FLOAT(`fat (g)`) as fat, FLOAT(`carbohydrate (g)`) as carbs, FLOAT(`sugars (g)`) as sugars, FLOAT(`water (g)`) as water, FLOAT(`monounsat (g)`) as monounsat, FLOAT(`polyunsat (g)`) as polyunsat, FLOAT(`calcium (g)`) as calcium, FLOAT(`sodium (g)`) as sodium, FLOAT(`fiber (g)`) as fiber, FLOAT(`vitaminc (g)`) as vitaminc FROM nutrients")
	nutrients_df.createOrReplaceTempView('nutrients_cleaned')
	
	#filtered records
	filtered_nutrients = spark.sql("SELECT * from nutrients_cleaned where food_name"+filter_cond)
	

	#regex to extract label names and create a column with those labels
	new_df = filtered_nutrients.withColumn('food_item', functions.regexp_extract('food_name', '|'.join(labels), 0))

	new_df.createOrReplaceTempView('nutrients_enhanced')
	aggregated_df = spark.sql("SELECT food_item, AVG(calories) as avg_calorie,MAX(calories) as max_calorie, MIN(calories) as min_calorie, AVG(proteins) as avg_proteins, AVG(fat) as avg_fat,AVG(carbs) as avg_carbs, AVG(sugars) as avg_sugars, AVG(water) as avg_water, AVG(monounsat) as avg_monounsat, AVG(polyunsat) as avg_polyunsat , AVG(calcium) as avg_calcium , AVG(sodium) as avg_sodium, AVG(fiber) as avg_fiber, AVG(vitaminc) as avg_vitc  from nutrients_enhanced GROUP BY food_item")
	aggregated_df.show()

	aggregated_df.write.format("org.apache.spark.sql.cassandra") \
	.options(table=table, keyspace=keyspace).save()
	session.shutdown()
	
   
if __name__ == '__main__':
	inputs = sys.argv[1]
	main(inputs)