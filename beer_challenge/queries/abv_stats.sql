CREATE TABLE IF NOT EXISTS abv_stats
(
    "min" DOUBLE PRECISION,
    "max" DOUBLE PRECISION,
    average DOUBLE PRECISION,
    "year" TEXT,
    "month" TEXT,
    "day" TEXT
);

DO
$$
DECLARE
    timedelta INTEGER;
BEGIN
   WITH max_date AS (SELECT DATE(COALESCE(MAX("year" || '-' || "month" || '-' || "day"), '2023-05-01')) AS max_date
                  FROM abv_stats)

    SELECT current_date - (SELECT max_date FROM max_date)  INTO timedelta;
    IF timedelta > 0 THEN
        INSERT
INTO abv_stats
SELECT min(abv)                                             AS "min",
       max(abv)                                             AS "max",
       avg(abv)                                             AS average,
       EXTRACT(YEAR FROM current_date)::text                AS "year",
       LPAD(EXTRACT(MONTH FROM current_date)::text, 2, '0') AS "month",
       LPAD(EXTRACT(DAY FROM current_date)::text, 2, '0')   AS "day"
FROM beers;
    END IF;
END
$$;
