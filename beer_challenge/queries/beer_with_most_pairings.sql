SELECT
    b.id,
    name,
    tagline,
    first_brewed,
    abv,
    COUNT(food_pairing) AS pairing_count,
    AVG(abv) AS average_abv
FROM beers AS b
INNER JOIN food_pairings_pandas AS fp ON b.id = fp.id
GROUP BY b.id, name, tagline, first_brewed, abv
ORDER BY pairing_count DESC
LIMIT 1;
