# Comparing Python and Scala UDFs in PySpark

This pyspark application compares the execution performance of Python UDFs vs. Scala UDFs in PySpark by measuring the execution time of a simple function applied to a large dataset.

![UDF](https://docs.aws.amazon.com/images/prescriptive-guidance/latest/tuning-aws-glue-for-apache-spark/images/worker-nodes.png)


## Overview

Why compare Python and Scala UDFs?

Python UDFs run in a separate process, leading to inter-process communication overhead.
Pyspark wrapper will call Java wrapper using the **PY4J** connection allows a python application to call a Java application, and the Java wrapper runs Scala core in JVM.

Scala UDFs run directly in the JVM, providing better performance.

**NOTE-** Scala/Java UDFs not faster than Python UDF in all cases but the majority yes.

This guide will walk you through setting up and testing both UDFs step by step.

## 1. Prerequisites

Make sure you have the following installed:
✅ Apache Spark
✅ Java (JDK 8 or 11)
✅ Scala
✅ sbt (Scala Build Tool)
✅ Python (with PySpark installed)

To check the installations:
```
spark-submit --version
java -version
scala -version
sbt --version
python --version
```

If sbt is missing, install it using:
```
echo "deb https://repo.scala-sbt.org/scalasbt/debian all main" | sudo tee /etc/apt/sources.list.d/sbt.list
curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EEB989E90DC33E04B1D126BAF2A6A2A07B16710" | sudo apt-key add
sudo apt-get update
sudo apt-get install sbt
```

**sbt (Scala Build Tool) is a build tool for Scala and Java projects, similar to Maven or Gradle. It is primarily used for:**

* Compiling Scala/Java code
* Managing dependencies (like Spark libraries)
* Building and packaging JAR files
* Running tests and applications

**Why do we need sbt in this project?**
We used sbt to compile and package the Scala UDF into a JAR file.
The JAR file is then loaded into PySpark, allowing us to use the Scala UDF in our PySpark application.


## 2. Create an sbt Project

Navigate to your working directory and initialize an sbt project:
```
mkdir /path/to/spark-udf-scala
cd /path/to/spark-udf-scala
sbt new scala/scala-seed.g8
```

## 3. Configure build.sbt

Edit the build.sbt file:
```
nano build.sbt
```
Replace its content with:
```
ThisBuild / scalaVersion     := "2.12.18"
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
```
## 4.Create a Scala UDF

Navigate to the Scala source directory:
```
mkdir -p src/main/scala/com/example/udfs
cd src/main/scala/com/example/udfs
nano MultiplyByTwo.scala
```
Paste the following Scala code: (You can replace it with your own UDF)
```
package com.example.udfs

import org.apache.spark.sql.api.java.UDF1

class MultiplyByTwo extends UDF1[Int, Int] {
  override def call(value: Int): Int = value * 2
}
```

## 5. Compile and Package the Scala UDF

Navigate back to the project root (where your pyspark application, src, and target exist) and run the following:
```
sbt compile
sbt package
```
This will generate a jar file like this in target directory:
``` target/scala-2.12/udf_2.12-0.1.0-SNAPSHOT.jar ```

## 6. . Create a PySpark Application

Navigate to your project directory and create a Python script

## 7. Run the PySpark Application

Execute the script:
```spark-submit --jars target/scala-2.12/udf_2.12-0.1.0-SNAPSHOT.jar compare_udfs.py```

# Expected Output
```
Scala UDF execution time: 4.6415 seconds
Python UDF execution time: 0.8573 seconds
```
