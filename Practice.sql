

/*
 * 1. Find the total milk production for the year 2023.
 
 
SELECT COUNT(*)
FROM milk_production mp 
WHERE "Year" = 2023

* Should have been SUM
*/



/*
 * 2. Show coffee production data for the year 2015.


SELECT SUM(Value)
FROM coffee_production cp 
WHERE "Year" = 2015
*/




/*
 * 3. Find the average honey production for the year 2022.

 
SELECT AVG(Value)
FROM honey_production hp 
WHERE "Year" = 2022
*/




/*
 * 4. Get the state names with their corresponding ANSI codes from the state_lookup table.

 
 
SELECT  State_ANSI
FROM state_lookup sl 
WHERE "State" = "IOWA"
*/



/*
 * 5. Find the highest yogurt production value for the year 2022.


SELECT MAX(Value)
FROM yogurt_production yp 
WHERE "Year" = 2022
*/



/*
 * 6. Find states where both honey and milk were produced in 2022.


SELECT *
FROM honey_production hp  JOIN milk_production mp 
	ON hp.State_ANSI = mp.State_ANSI
WHERE hp."Year" = 2022 AND mp.State_ANSI = 35


Solution: 
SELECT DISTINCT h.State_ANSI FROM honey_production h
JOIN milk_production m ON h.State_ANSI = m.State_ANSI
WHERE h.Year = 2022 AND m.Year = 2022:
*/




/*
 * 7. Find the total yogurt production for states that also produced cheese in 2022.


SELECT SUM(yp.Value)
FROM yogurt_production yp JOIN cheese_production cp 
	ON yp.State_ANSI = cp.State_ANSI
	
SOLUTON:
SELECT SUM(y.Value)
FROM yogurt_production y
WHERE y.Year = 2022 AND y.State_ANSI IN (
    SELECT DISTINCT c.State_ANSI FROM cheese_production c WHERE c.Year = 2022
);
*/