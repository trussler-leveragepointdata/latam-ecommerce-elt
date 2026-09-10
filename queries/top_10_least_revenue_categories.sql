-- TODO: 
-- This query will return a table with the top 10 least revenue categories 
-- in English, the number of orders and their total revenue. 
-- It will have different columns: 
--      Category, that will contain the top 10 least revenue categories; 
--      Num_order, with the total amount of orders of each category; 
--      Revenue, with the total revenue of each category.

-- HINT: 
-- All orders should have a delivered status and the Category and actual delivery date should be not null.
-- For simplicity, if there are orders with multiple product categories, consider the full order's payment_value in the summation of revenue of each category 
SELECT
    op2.product_category_name AS Category,
    COUNT(DISTINCT oo.order_id) AS Num_order,
    SUM(op.payment_value) AS Revenue
FROM olist_order_payments op
JOIN olist_order_items ooi 
	ON ooi.order_id = op.order_id
JOIN olist_orders oo 
	ON oo.order_id = ooi.order_id
JOIN olist_products op2  
	ON op2.product_id   = ooi.product_id  
WHERE
    oo.order_status = 'delivered' 
AND
    oo.order_delivered_customer_date IS NOT NULL
GROUP BY op2.product_category_name 
ORDER BY Revenue ASC
LIMIT 10