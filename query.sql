SELECT
    u.user_id,
    u.name AS user_name,
    u.country,
    o.order_id,
    o.order_date,
    p.product_name,
    p.category,
    oi.quantity,
    oi.line_total,
    r.rating,
    SUM(o.total_amount) OVER (PARTITION BY u.user_id) AS total_spent_per_user,
    (
        SELECT COUNT(DISTINCT inner_o.order_id)
        FROM orders AS inner_o
        WHERE inner_o.user_id = u.user_id
    ) AS orders_per_user
FROM orders AS o
JOIN users AS u ON o.user_id = u.user_id
JOIN order_items AS oi ON oi.order_id = o.order_id
JOIN products AS p ON p.product_id = oi.product_id
LEFT JOIN reviews AS r
    ON r.user_id = u.user_id
   AND r.product_id = p.product_id
ORDER BY o.order_date DESC, u.user_id ASC;

