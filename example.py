import sys
import pyspark

zookeeper = sys.argv[1]
hadoop_ip = sys.argv[2]

print(zookeeper)
print(hadoop_ip)

src = 'hdfs://{}:8020/sample.txt'.format(hadoop_ip)
conf = pyspark.SparkConf()
conf.setMaster('mesos://zk://{}/mesos'.format(zookeeper))
conf.setAppName('my_test_app')
conf.set("spark.cores.max", "2")
conf.set("spark.executor.memory", "2g")
conf.set('spark.mesos.extra.cores', '1')

print("binary")
# this must be a _prebuilt_ spark archive, i.e. a spark binary package
# you can build it and host it yourself if you like.
conf.set('spark.executor.uri', 'spark-1.5.0-bin-hadoop2.6.tgz')

sc = pyspark.SparkContext(conf=conf)

lines = sc.textFile(src)
print("HEY")
words = lines.flatMap(lambda x: x.split(' '))
word_count = (words.map(lambda x: (x, 1)).reduceByKey(lambda x, y: x+y))
print("DONE")
print(word_count.collect())
