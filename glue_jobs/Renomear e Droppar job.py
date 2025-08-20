import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from awsgluedq.transforms import EvaluateDataQuality

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Default ruleset used by all target nodes with data quality enabled
DEFAULT_DATA_QUALITY_RULESET = """
    Rules = [
        ColumnCount > 0
    ]
"""

# Script generated for node Amazon S3
AmazonS3_node1755534768008 = glueContext.create_dynamic_frame.from_options(format_options={"quoteChar": "\"", "withHeader": True, "separator": ",", "optimizePerformance": False}, connection_type="s3", format="csv", connection_options={"paths": ["s3://projeto-letterboxd-bucket/raw-data/Movie_Data_File.csv"], "recurse": True}, transformation_ctx="AmazonS3_node1755534768008")

# Script generated for node Change Schema
ChangeSchema_node1755536301032 = ApplyMapping.apply(frame=AmazonS3_node1755534768008, mappings=[("film_title", "string", "film_title", "string"), ("director", "string", "director", "string"), ("average_rating", "string", "average_rating", "float"), ("genres", "string", "genres", "string"), ("runtime", "string", "runtime", "int"), ("countries", "string", "countries", "string"), ("original_language", "string", "original_language", "string"), ("spoken_languages", "string", "spoken_languages", "string"), ("studios", "string", "studios", "string"), ("watches", "string", "watches", "int"), ("list_appearances", "string", "list_appearances", "int"), ("likes", "string", "likes", "int"), ("fans", "string", "fans", "int"), ("½", "string", "votes_0_5", "int"), ("★", "string", "votes_1_0", "int"), ("★½", "string", "votes_1_5", "int"), ("★★", "string", "votes_2_0", "int"), ("★★½", "string", "votes_2_5", "int"), ("★★★", "string", "votes_3_0", "int"), ("★★★½", "string", "votes_3_5", "int"), ("★★★★", "string", "votes_4_0", "int"), ("★★★★½", "string", "votes_4_5", "int"), ("★★★★★", "string", "votes_5_0", "int"), ("total_ratings", "string", "total_ratings", "int")], transformation_ctx="ChangeSchema_node1755536301032")

# Script generated for node Amazon S3
EvaluateDataQuality().process_rows(frame=ChangeSchema_node1755536301032, ruleset=DEFAULT_DATA_QUALITY_RULESET, publishing_options={"dataQualityEvaluationContext": "EvaluateDataQuality_node1755536165420", "enableDataQualityResultsPublishing": True}, additional_options={"dataQualityResultsPublishing.strategy": "BEST_EFFORT", "observations.scope": "ALL"})
AmazonS3_node1755536633590 = glueContext.write_dynamic_frame.from_options(frame=ChangeSchema_node1755536301032, connection_type="s3", format="glueparquet", connection_options={"path": "s3://projeto-letterboxd-bucket/processed-data/", "partitionKeys": []}, format_options={"compression": "snappy"}, transformation_ctx="AmazonS3_node1755536633590")

job.commit()