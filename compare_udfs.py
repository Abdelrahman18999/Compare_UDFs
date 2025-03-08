from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import IntegerType
import time

# Initialize Spark session and load the JAR
spark = SparkSession.builder \
    .appName("Compare UDF Performance") \
    .master("local[*]") \
    .config("spark.jars", "target/scala-2.12/udf_2.12-0.1.0-SNAPSHOT.jar") \
    .config("spark.eventLog.enabled", "true") \
    .config("spark.eventLog.dir", "file:///tmp/spark-logs") \
    .getOrCreate()

# Register Scala UDF
spark.udf.registerJavaFunction("multiplyByTwoScala", "com.example.udfs.MultiplyByTwo", "integer")

# Define equivalent Python UDF
def multiply_by_two_python(value):
    return value * 2

multiply_by_two_py_udf = udf(multiply_by_two_python, IntegerType())

# Create DataFrame with 1 million rows
data = [(i,) for i in range(1000000)]
df = spark.createDataFrame(data, ["value"])

# Measure execution time for Scala UDF
start_time = time.time()
df.withColumn("result_scala", col("value")).selectExpr("multiplyByTwoScala(value) as result").count()
scala_time = time.time() - start_time

# Measure execution time for Python UDF
start_time = time.time()
df.withColumn("result_python", multiply_by_two_py_udf(col("value"))).count()
python_time = time.time() - start_time

# Print results
print(f"Scala UDF execution time: {scala_time:.4f} seconds")
print(f"Python UDF execution time: {python_time:.4f} seconds")

# Stop Spark session
spark.stop()
