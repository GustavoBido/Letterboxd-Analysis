CREATE TABLE filmes_nota_alta_nao_famosos
WITH (
    format = 'PARQUET',
    external_location = 's3://projeto-letterboxd-bucket/gems-data/' 
) AS
-- FILMES (DE TODOS OS PAÍSES) COM NOTA BASTANTE ALTA, MAS NÃO TÃO FAMOSOS
WITH calculos AS (
    SELECT
        film_title,
        total_ratings,
        CAST(
            (
                (0.5 * votes_0_5) + (1.0 * votes_1_0) + (1.5 * votes_1_5) + (2.0 * votes_2_0) + (2.5 * votes_2_5) + 
                (3.0 * votes_3_0) + (3.5 * votes_3_5) + (4.0 * votes_4_0) + (4.5 * votes_4_5) + (5.0 * votes_5_0)
            ) AS DOUBLE
        ) / total_ratings AS nota_media
    FROM processed_data
)
SELECT
    film_title,
    total_ratings,
    nota_media
FROM calculos
WHERE 
    total_ratings BETWEEN 1000 AND 50000 
    AND nota_media > 4.0 
ORDER BY nota_media DESC, total_ratings DESC;