SELECT 
  o.orderNumber,
  o.orderDate, 
  c.customerName, 
  c.city, 
  c.country, 
  od.quantityOrdered, 
  p.productName
FROM orders AS o
LEFT OUTER JOIN customers AS c
  ON o.customerNumber = c.customerNumber
LEFT OUTER JOIN orderdetails AS od
  ON o.orderNumber = od.orderNumber
LEFT OUTER JOIN products AS p
  ON p.productCode = od.productCode 
WHERE 
  DATE(o.orderDate)
    BETWEEN '2004-08-01' AND '2004-12-01'
  AND
  p.productName = '1992 Ferrari 360 Spider red'
ORDER BY 
  c.country;