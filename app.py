from pyspark.sql import SparkSession
from pyspark.sql.functions import col, from_json
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("PySpark-HDFS-Streaming") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Define Schema for Sensor Data
schema = StructType([
    StructField("sensor_id", StringType(), True),
    StructField("temperature", DoubleType(), True),
    StructField("timestamp", StringType(), True)
])

# Read Stream from HDFS input directory
df_stream = spark.readStream \
    .schema(schema) \
    .json("hdfs://namenode:9000/data/input")

# Simple Transformation: Filter high temperature anomalies (> 30.0)
df_filtered = df_stream.filter(col("temperature") > 30.0)

# Write Stream to Console output
query = df_filtered.writeStream \
    .outputMode("append") \
    .format("console") \
    .start()

query.awaitTermination()