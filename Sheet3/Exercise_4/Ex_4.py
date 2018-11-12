from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.types import *

# Build the SparkSession
spark = SparkSession.builder \
   .master("local") \
   .appName("Ex_4") \
   .config("spark.executor.memory", "8gb") \
   .getOrCreate()

sc = spark.sparkContext

rdd = sc.textFile('/home/nico/Uni/11_Semester/Verteilte Systeme/Git/vs-1819/Sheet3/CaliforniaHousing/cal_housing.data')

# Load in the header
header = sc.textFile('/home/nico/Uni/11_Semester/Verteilte Systeme/Git/vs-1819/Sheet3/CaliforniaHousing/cal_housing.domain')

rdd = rdd.map(lambda line: line.split(","))

# Map the RDD to a DF

df = rdd.map(lambda line: Row(longitude=line[0],
                              latitude=line[1],
                              housingMedianAge=line[2],
                              totalRooms=line[3],
                              totalBedRooms=line[4],
                              population=line[5],
                              households=line[6],
                              medianIncome=line[7],
                              medianHouseValue=line[8])).toDF()

# Write a custom function to convert the data type of DataFrame columns
def convertColumn(df, names, newType):
  for name in names:
     df = df.withColumn(name, df[name].cast(newType))
  return df

# Assign all column names to `columns`
columns = ['households', 'housingMedianAge',
           'latitude', 'longitude',
           'medianHouseValue', 'medianIncome',
           'population', 'totalBedRooms', 'totalRooms']

# Conver the `df` columns to `FloatType()`
df = convertColumn(df, columns, FloatType())

print("\x1b[0;31;40m" + "Latitude of northernmost household from california:" + '\x1b[0m')
df.select('latitude').sort('latitude', ascending=False).show(1)
print("")

print("\x1b[0;31;40m" + "Most common household size:" + '\x1b[0m')
maximum = df.groupBy('households').count()
maximum.sort('count', ascending=False).show(1)
print("")

print("\x1b[0;31;40m" + "The highest ratio of bedroom per population" + '\x1b[0m')
df.select('population', 'totalBedrooms', df['totalBedrooms']/df['population']).sort('(totalBedrooms / population)', ascending=False).show(1)
"""
Answers to the questions:

    Collect should not be used on large datasets, because the driver can run out of memory.
    You can instead use the take(n) method if you want to print a few elements of
    the RDD.
    Also possible are methods like top(), first(), takeSample(), takeOrdered(n)
    In general, you should limit the results as much as possible, just like in SQL.

    Dataframes are used for structured data, you can use:
        high level expressions
        perform SQL queries to explore data and gain columnar access
    Dataframes are faster using Python
    The data represantation is better to look at because you get a spreadsheet representation with show()
"""