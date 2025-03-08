package com.example.udfs

import org.apache.spark.sql.api.java.UDF1

class MultiplyByTwo extends UDF1[Int, Int] {
  override def call(value: Int): Int = value * 2
}
