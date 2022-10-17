import boto3
import sys

from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
import pandas as pd
from awsglue.dynamicframe import DynamicFrame
import json
from pyspark import SparkConf

endpoint_url = "http://localstack:4566"
region_name = "sa-east-1"

def main():
    s3 = boto3.client("s3", endpoint_url=endpoint_url, 
                                region_name=region_name,
                                aws_access_key_id="key",
                                aws_secret_access_key="secret")
    result = s3.list_buckets()
     

    args = getResolvedOptions(sys.argv, ["JOB_NAME"])

    conf = ( SparkConf()
        .set('spark.hadoop.fs.s3a.access.key', 'key')
        .set('spark.hadoop.fs.s3a.secret.key', 'secret')
        .set('spark.hadoop.fs.s3a.endpoint', 'http://localstack:4566')
        .set('spark.hadoop.fs.s3a.path.style.access','true')
        .set('spark.hadoop.fs.s3a.connection.ssl.enabled','false')
    )


    spark = SparkContext.getOrCreate(conf=conf)
    context = GlueContext(spark)
 
    job = Job(context)
    job.init(args['JOB_NAME'], args)


    data = [("James","","Smith","36636","M","60000", "2022"),
        ("Michael","Rose","","40288","M","70000", "2022"),
        ("Robert","","Williams","42114","M","400000", "2022"),
        ("Maria","Anne","Jones","39192","F","500000", "2022"),
        ("Jen","Mary","Brown","","F","0", "2022")]

    columns = ["first_name","middle_name","last_name","dob","gender","salary", "year"]
    pysparkDF = context.spark_session.createDataFrame(data = data, schema = columns)

    dynamicFrame = DynamicFrame.fromDF(pysparkDF, context, "df")
    
    context.write_dynamic_frame.from_options(
        frame = dynamicFrame,
        connection_type = "s3",
        connection_options = {"path": "s3://bkt/historico", "partitionKeys": ["year"]},
        format = "parquet")

    job.commit()


if __name__ == "__main__":
    main()