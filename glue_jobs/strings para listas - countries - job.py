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
args = getResolvedOptions(sys.argv, ["JOB_NAME", "INPUT_PATH", "OUTPUT_PATH_BASE"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# =========================
# 1) Ler o Parquet do S3
#    (lê a pasta toda/partições)
# =========================
df = spark.read.parquet(args["INPUT_PATH"])

# =========================
# 2) Função auxiliar: string -> array<string>
#    Estratégia simples:
#    - Cast para string
#    - Troca aspas simples por duplas (JSON válido)
#    - from_json para ArrayType(StringType())
#    - Se ficar null, substitui por array vazio []
# =========================
def to_array(colname):
    s = F.col(colname).cast("string")
    s_json = F.regexp_replace(s, "'", '"')  # 'x' -> "x"
    arr = F.from_json(s_json, ArrayType(StringType()))
    # null -> array vazio
    return F.when(arr.isNull(), F.array().cast(ArrayType(StringType()))).otherwise(arr)

# =========================
# 3) Normalizar colunas
#    countries, genres, studios -> arrays
#    original_language -> string limpa
# =========================
df_norm = (
    df
    # Arrays padronizados
    .withColumn("countries_array", to_array("countries"))
    .withColumn("genres_array", to_array("genres"))
    .withColumn("studios_array", to_array("studios"))
)

# original_language pode estar como string ou lista em string
# Regra simples:
#  - se for lista em string: pega o primeiro item
#  - se for string normal: só trim()
#  - se ficar null: vira string vazia
ol_str = F.col("original_language").cast("string")
ol_json = F.regexp_replace(ol_str, "'", '"')
ol_arr = F.from_json(ol_json, ArrayType(StringType()))
# se ol_arr não for nulo e tiver elementos, pega o primeiro; senão usa a string original
ol_first = F.when(F.size(ol_arr) > 0, ol_arr.getItem(0)).otherwise(ol_str)
df_norm = df_norm.withColumn("original_language_clean", F.trim(F.coalesce(ol_first, F.lit(""))))

# =========================
# 4) Escrita — versão "arrays" (sem explode)
#    Mantém estrutura original + colunas normalizadas
# =========================
output_arrays = f"{args['OUTPUT_PATH_BASE'].rstrip('/')}/normalized_arrays/"
(
    df_norm
    .write
    .mode("overwrite")
    .parquet(output_arrays)
)

# =========================
# 5) Escrita — versões "exploded"
#    Uma linha por elemento (facilita groupby/contagens)
# =========================
# Explode countries
df_countries_exploded = (
    df_norm
    .withColumn("country", F.explode_outer(F.col("countries_array")))
    .withColumn("country", F.trim(F.col("country")))
)
df_countries_exploded.write.mode("overwrite").parquet(f"{args['OUTPUT_PATH_BASE'].rstrip('/')}/countries_exploded/")

# Explode genres
df_genres_exploded = (
    df_norm
    .withColumn("genre", F.explode_outer(F.col("genres_array")))
    .withColumn("genre", F.trim(F.col("genre")))
)
df_genres_exploded.write.mode("overwrite").parquet(f"{args['OUTPUT_PATH_BASE'].rstrip('/')}/genres_exploded/")

# Explode studios
df_studios_exploded = (
    df_norm
    .withColumn("studio", F.explode_outer(F.col("studios_array")))
    .withColumn("studio", F.trim(F.col("studio")))
)
df_studios_exploded.write.mode("overwrite").parquet(f"{args['OUTPUT_PATH_BASE'].rstrip('/')}/studios_exploded/")

# =========================
# 6) Finalizar o job
# =========================
job.commit()
