-- TODO: 
-- This query will return a table with two columns: order_status and Amount. 
-- The first one will have the different order status classes 
-- and the second one the total amount of each.
SELECT 
	order_status,
	SUM(payment_value) AS Amount
FROM 
	olist_order_payments
JOIN 
	olist_orders
USING (order_id)
GROUP BY
	order_status