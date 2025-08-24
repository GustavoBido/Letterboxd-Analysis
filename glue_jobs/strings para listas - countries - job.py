import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
import pyspark.sql.functions as F
from pyspark.sql.types import ArrayType, StringType

# =========================
# 0) Inicialização do Glue
# =========================
args = getResolvedOptions(sys.argv, ["JOB_NAME", "INPUT_PATH", "OUTPUT_PATH"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# =========================
# 1) Ler o Parquet do S3
# =========================
df = spark.read.parquet(args["INPUT_PATH"])

# =========================
# 2) Função para converter a coluna "countries" para array
#    Esta função lida tanto com strings tipo lista ("['A', 'B']") quanto strings simples ("A").
# =========================
def to_array(colname):
    s = F.trim(F.col(colname).cast("string"))
    s_json = F.regexp_replace(s, "'", '"')
    arr_from_json = F.from_json(s_json, ArrayType(StringType()))
    arr_from_string = F.array(s)

    final_arr = F.when(s.startswith("["), arr_from_json).otherwise(arr_from_string)
    return F.coalesce(final_arr, F.array().cast(ArrayType(StringType())))

# =========================
# 3) Aplicar a transformação APENAS em "countries" e explodir
# =========================
# O resultado terá uma linha para cada país de um filme, com as colunas 'genres' e 'studios' inalteradas.

df_final = (
    df
    # 1. Cria uma coluna temporária com os países em formato de array.
    .withColumn("countries_array", to_array("countries"))

    # 2. "Explode" a coluna de array para criar a nova coluna "country".
    #    Usamos explode_outer para não perder filmes que não tenham país listado.
    .withColumn("country", F.explode_outer(F.col("countries_array")))

    # 3. Remove a coluna original "countries" e a coluna temporária "countries_array"
    #    para manter o resultado limpo.
    .drop("countries", "countries_array")
)

(
    df_final
    .write
    .mode("overwrite")
    .parquet(args["OUTPUT_PATH"])
)

job.commit()