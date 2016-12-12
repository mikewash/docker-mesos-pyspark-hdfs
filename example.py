import sys
import pyspark
#from random import random
import random as ran
import string

master = sys.argv[1]

conf = pyspark.SparkConf()
conf.setMaster("mesos://{}:5050".format(master))
conf.setAppName('my_test_app')
conf.set('spark.mesos.coarse', 'true')
conf.set('spark.executor.uri', 'http://d3kbcqa49mib13.cloudfront.net/spark-2.0.2-bin-hadoop2.7.tgz')

array = []
sc = pyspark.SparkContext(conf=conf)
num_of_words = 10000

for i in range(num_of_words):
    random = ''.join([ran.choice(string.ascii_letters + string.digits) for n in xrange(1)])
    array.append(random)

lines = sc.parallelize(array) 
wordcounts = lines.map( lambda x: x.replace(',',' ').replace('.',' ').replace('-',' ').lower()) \
        .flatMap(lambda x: x.split()) \
        .map(lambda x: (x, 1)) \
        .reduceByKey(lambda x,y:x+y) \
        .map(lambda x:(x[1],x[0])) \
        .sortByKey(True) 
print wordcounts.take(50)
