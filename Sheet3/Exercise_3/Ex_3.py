from pyspark.sql import SparkSession

"""
join(): (RDD[(K, V)],RDD[(K, W)]) => RDD[(K, (V, W))]
        Two datasets (K, V) and (K, W) are joined together, creating one dataset
        (K, (V, W)), where the key K now has all elements as a pair.
        Example:
            rdd1 = sc.parallelize([('cat', 5), ('dog', 10)])
            rdd2 = sc.parallelize([('cat', 'Tuna')])

            rdd1.join(rdd2)
            => ('cat', (5, 'Tuna'))

sort(): RDD[(K, V)] ⇒ RDD[(K, V)]
        One dataset (K, V) is sorted by the specified value, returning the sorted
        dataset.
        Example:
            rdd = sc.parallelize([('cat', 1),
                                  ('horse', 5),
                                  ('dog', 1)])
            rdd.sort(rdd[0])
            => (('cat', 1), ('dog', 1), ('horse', 5))
            This is pseudocode. RDDs use sortByKey and DFs use sort()

groupBy(): RDD[(K, V)] ⇒ RDD[(K, Seq[V])]
           A dataset of (K, V) pairs, returns a dataset of (K, iterable<V>) pairs
           Example:
               rdd = sc.parallelize([('cat', 1),
                                  ('horse', 5),
                                  ('dog', 1),
                                  ('cat', 5)])
               rdd.groupBy(rdd[0])
               => (('cat', [1, 5]), ('dog', 1), ('horse', 5))
               This is pseudocode, RDDs use groupByKey, DFs use groupBy
"""



# Build the SparkSession
spark = SparkSession.builder \
   .master("local") \
   .appName("Ex_3") \
   .config("spark.executor.memory", "8gb") \
   .getOrCreate()

sc = spark.sparkContext

list1 = [('crocodile', 4), ('cat', 7), ('bird', 2)]
list2 = [('dog', 3), ('fish', 1), ('cat', 2), ('bird', 3)]

rdd1 = sc.parallelize(list1)
rdd2 = sc.parallelize(list2)

rdd3 = rdd1.join(rdd2) # Transformation: [('cat', (7, 2)), ('bird', (2, 3))]
print(rdd3.take(1)) # Action: [('cat', (7, 2))]
print(rdd3.take(2)) # Action: [('cat', (7, 2)), ('bird', (2, 3))]

rdd4 = rdd1.union(rdd2) # Transformation: rdd1 merged with rdd2
print(rdd4.collect()) # Action: returns every element of rdd4

rdd5 = rdd4.groupByKey() # Transformation
rdd5 = rdd5.map(lambda x: (x[0], list(x[1]))) # Also transformation so you don't have <pyspark.resultiterable.ResultIterable object at 0x7f7b60353550> as value
print(rdd5.collect()) # Action
print(rdd5.count()) # Action: Counts the elements => 5