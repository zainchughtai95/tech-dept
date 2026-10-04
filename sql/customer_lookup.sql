-- Support lookup. Leading wildcard and a function on the filter column.

SELECT *
FROM customers c
WHERE LOWER(c.email) = 'ada@example.com'
   OR c.phone LIKE '%555'
ORDER BY c.created_at;
