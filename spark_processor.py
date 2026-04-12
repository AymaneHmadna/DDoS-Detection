from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType
from pyspark.sql.functions import col, from_json, when
spark = SparkSession.builder \
    .appName("CyberSentinel_FinalDemo") \
    .config("spark.cassandra.connection.host", "cassandra") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0,com.datastax.spark:spark-cassandra-connector_2.12:3.3.0") \
    .getOrCreate()
spark.sparkContext.setLogLevel("ERROR")
print("Strict surveillance of Port 6666...")
raw_stream = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "broker:29092") \
    .option("subscribe", "network-traffic") \
    .load()
schema = StructType([
    StructField("ip", StringType()),
    StructField("ports_accessed", IntegerType()),
    StructField("session_duration", DoubleType()),
    StructField("errors", IntegerType()),
    StructField("timestamp", DoubleType()),
    StructField("target", StringType())
])
df_parsed = raw_stream.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")
final_df = df_parsed.withColumn("prediction_label", 
    when(col("ports_accessed") == 6666, "DDoS Attack (Massive)")
    .otherwise("Safe User")
)
query_cassandra = final_df.select(
        col("ip"), 
        col("ports_accessed").alias("count"), 
        col("timestamp").cast("timestamp").alias("last_seen"), 
        col("prediction_label").alias("prediction")
    ) \
    .writeStream \
    .foreachBatch(lambda df, epoch_id: df.write \
        .format("org.apache.spark.sql.cassandra") \
        .mode("append") \
        .options(table="resultats_ips", keyspace="projet_logs") \
        .save()) \
    .start()
query_hdfs = final_df.select("ip", "ports_accessed", "prediction_label").writeStream \
    .format("json") \
    .option("path", "hdfs://namenode:9000/data_lake/traffic_logs") \
    .option("checkpointLocation", "hdfs://namenode:9000/checkpoints/final_demo") \
    .start()
spark.streams.awaitAnyTermination()