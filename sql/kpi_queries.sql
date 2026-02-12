-- Average Medical Cost
SELECT AVG(charges) FROM insurance;

-- Average Cost by Smoking Status
SELECT smoker, AVG(charges)
FROM insurance
GROUP BY smoker;

-- Average Cost by Region
SELECT region, AVG(charges)
FROM insurance
GROUP BY region;

-- Top 5 Highest Charges
SELECT age, bmi, smoker, charges
FROM insurance
ORDER BY charges DESC
LIMIT 5;
