import sys
import pyspark
from random import random

zookeeper = sys.argv[1]
hadoop_ip = sys.argv[2]

print(zookeeper)
print(hadoop_ip)

src = 'hdfs://{}:8020/sample.txt'.format(hadoop_ip)
conf = pyspark.SparkConf()
#conf.setMaster('mesos://zk://{}/mesos'.format(zookeeper))
conf.setMaster("mesos://172.31.34.240:5050")
conf.setAppName('my_test_app')
conf.set('spark.mesos.coarse', 'true')
#conf.set("spark.cores.max", "2")
#conf.set("spark.executor.memory", "1g")

print("binary")
# this must be a _prebuilt_ spark archive, i.e. a spark binary package
# you can build it and host it yourself if you like.
#conf.set('spark.executor.uri', 'hdfs://172.17.0.2/spark-2.0.2-bin-hadoop2.7.tgz')
conf.set('spark.executor.uri', 'http://d3kbcqa49mib13.cloudfront.net/spark-2.0.2-bin-hadoop2.7.tgz') 

sc = pyspark.SparkContext(conf=conf)
NUM_SAMPLES = 91100000
def sample(p):
    x, y = random(), random()
    return 1 if x*x + y*y < 1 else 0

count = sc.parallelize(xrange(0, NUM_SAMPLES)).map(sample) \
             .reduce(lambda a, b: a + b)
print("Pi is roughly %f" % (4.0 * count / NUM_SAMPLES))
