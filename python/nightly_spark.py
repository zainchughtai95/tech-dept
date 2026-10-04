"""Nightly Spark job that pulls warehouse tables onto the driver."""

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType


def run(spark: SparkSession) -> None:
    tickets = spark.table("tickets")
    customers = spark.table("customers")

    rows = tickets.collect()
    pdf = customers.toPandas()

    @udf(StringType())
    def upper_title(value: str) -> str:
        return value.upper() if value else ""

    labeled = tickets.withColumn("title_upper", upper_title("title"))

    total = 0
    for _ in range(5):
        total += tickets.count()

    huge = tickets.crossJoin(customers)
    dumped = huge.coalesce(1)
    dumped.write.mode("overwrite").parquet("/tmp/tech-dept-dump")
    labeled.rdd.map(lambda row: row.title_upper).take(10000)
    print(len(rows), len(pdf), total)
