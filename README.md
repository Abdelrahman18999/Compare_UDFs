# Comparing Python and Scala UDFs in PySpark

This project compares the execution performance of Python UDFs vs. Scala UDFs in PySpark by measuring the execution time of a simple function applied to a large dataset.

## Overview

Why compare Python and Scala UDFs?

Python UDFs run in a separate process, leading to inter-process communication overhead.

Scala UDFs run directly in the JVM, providing better performance.

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
python --version```
