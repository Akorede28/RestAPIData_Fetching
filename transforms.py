from pyspark.sql import SparkSession
import json

def transform():
    spark = SparkSession.builder.getOrCreate()
    spark.sparkContext.setLogLevel("WARN")

    datafram = spark.read.json("c:/Users/daniel/Downloads/code/RestAPIData_Fetching/github.json")
    datafram.printSchema()
    datafram.show(False)

    datafram.write.option("header","true").csv("c:/Users/daniel/Downloads/code/RestAPIData_Fetching/git.csv")
    # print(df)
    # datafram.show()

if __name__ == "__main__":
    pass
