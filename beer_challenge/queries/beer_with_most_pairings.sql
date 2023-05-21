SELECT
    b.id,
    b.name,
    b.tagline,
    b.first_brewed,
    b.abv,
    COUNT(fp.food_pairing) AS pairing_count,
    AVG(b.abv) OVER () AS average_abv
FROM beers AS b
INNER JOIN food_pairings_pandas AS fp ON b.id = fp.id
GROUP BY b.id, b.name, b.tagline, b.first_brewed, b.abv
ORDER BY pairing_count DESC
LIMIT 1;
