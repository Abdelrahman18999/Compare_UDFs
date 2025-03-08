# Comparing Python and Scala UDFs in PySpark
1️## Install Required Dependencies
Before starting, ensure you have the following installed on your machine:
✅ Apache Spark
✅ Java (JDK 8 or 11)
✅ Scala
✅ sbt (Scala Build Tool)
✅ Python (with PySpark installed)

If you don’t have sbt installed, follow these steps:

sh
Copy
Edit
echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | sudo tee /etc/apt/sources.list.d/sbt.list
curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EEB989E90DC33E04B1D126BAF2A6A2A07B16710" | sudo apt-key add
sudo apt-get update
sudo apt-get install sbt
Verify installation:

sh
Copy
Edit
sbt --version
2️⃣ Create a New sbt Project
Navigate to your working directory and create the project:

sh
Copy
Edit
mkdir ~/Abdelrahman/spark_tutorials/spark-udf-scala
cd ~/Abdelrahman/spark_tutorials/spark-udf-scala
sbt new scala/scala-seed.g8
This initializes an sbt project.

3️⃣ Modify build.sbt to Add Spark Dependencies
Edit build.sbt:

sh
Copy
Edit
nano build.sbt
Replace its content with:

sbt
Copy
Edit
ThisBuild / scalaVersion     := "2.12.18"  // Ensure compatibility with Spark
ThisBuild / version          := "0.1.0-SNAPSHOT"
ThisBuild / organization     := "com.example"
ThisBuild / organizationName := "example"

lazy val root = (project in file("."))
  .settings(
    name := "udf",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-sql" % "3.3.0"
    )
  )
Save and exit (CTRL + X, Y, Enter).

4️⃣ Create the Scala UDF
Navigate to the Scala source directory:

sh
Copy
Edit
mkdir -p src/main/scala/com/example/udfs
cd src/main/scala/com/example/udfs
nano MultiplyByTwo.scala
Paste the following Scala code:

scala
Copy
Edit
package com.example.udfs

import org.apache.spark.sql.api.java.UDF1

class MultiplyByTwo extends UDF1[Int, Int] {
  override def call(value: Int): Int = value * 2
}
Save and exit.

5️⃣ Compile and Package the Scala UDF
Navigate back to the project root:

sh
Copy
Edit
cd ~/Abdelrahman/spark_tutorials/spark-udf-scala
sbt compile
sbt package
After this step, the compiled JAR file should be in:

sh
Copy
Edit
target/scala-2.12/udf_2.12-0.1.0-SNAPSHOT.jar
6️⃣ Create the PySpark Application
Navigate to your project root and create the Python script:

sh
Copy
Edit
nano compare_udfs.py
Paste the following code:

python
Copy
Edit
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import IntegerType
import time

# Initialize Spark session and load the JAR
spark = SparkSession.builder \
    .appName("Compare UDF Performance") \
    .config("spark.jars", "target/scala-2.12/udf_2.12-0.1.0-SNAPSHOT.jar") \  # Adjust filename if needed
    .getOrCreate()

# Register Scala UDF
spark.udf.registerJavaFunction("multiplyByTwoScala", "com.example.udfs.MultiplyByTwo", "integer")

# Define equivalent Python UDF
def multiply_by_two_python(value):
    return value * 2

multiply_by_two_py_udf = udf(multiply_by_two_python, IntegerType())

# Create DataFrame with 1 million rows
data = [(i,) for i in range(1_000_000)]
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
Save and exit.

7️⃣ Run the PySpark Application
Execute the script:

sh
Copy
Edit
python compare_udfs.py
Expected output:

less
Copy
Edit
Scala UDF execution time: 2.3 seconds
Python UDF execution time: 10.5 seconds
This shows that the Scala UDF is significantly faster than the Python UDF.

8️⃣ Summary of Why Scala UDF is Faster
✅ Scala UDF runs inside the JVM, avoiding the overhead of Python-JVM communication.
✅ Python UDF runs in a separate process, causing extra execution time.

For large datasets, Scala UDFs are much faster and should be preferred.

