import Dependencies._

ThisBuild / scalaVersion     := "2.12.18"  // Make sure this is compatible with Spark
ThisBuild / version          := "0.1.0-SNAPSHOT"
ThisBuild / organization     := "com.example"
ThisBuild / organizationName := "example"

lazy val root = (project in file("."))
  .settings(
    name := "udf",
    libraryDependencies ++= Seq(
      "org.apache.spark" %% "spark-sql" % "3.3.0", // Spark SQL library
      munit % Test
    )
  )

// See https://www.scala-sbt.org/1.x/docs/Using-Sonatype.html for instructions

