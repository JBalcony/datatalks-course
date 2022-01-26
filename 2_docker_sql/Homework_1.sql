-- Homework Week 1 by JBalcony for DataTalks.Club Data Engineering course

-- Question 3:
SELECT count(*)
FROM yellow_taxi_trips
WHERE tpep_pickup_datetime BETWEEN '2021-01-15' AND '2021-01-15 23:59:59'
-- Added 23:59:59 so nothing starts on 16'th 00:00:00
    
    --Alternative
    SELECT count(*)
    FROM yellow_taxi_trips
    WHERE tpep_pickup_datetime::timestamp::date = '2021-01-15'
    --::timestamp::date  gives us only date, without timestamp


-- Question 4:
SELECT tpep_pickup_datetime::timestamp::date
FROM yellow_taxi_trips
GROUP BY tpep_pickup_datetime
ORDER BY max(tip_amount) DESC
LIMIT 1

-- Question 5
SELECT
    CONCAT(zpu."Borough", '/', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", '/', zdo."Zone") AS "dropoff_loc",
    COUNT(1) AS "trip_count"
FROM yellow_taxi_trips t 
    JOIN taxi_zones zpu ON t."PULocationID" = zpu."LocationID"
    JOIN taxi_zones zdo ON t."DOLocationID" = zdo."LocationID"
WHERE t."PULocationID" = (
		SELECT "LocationID"
		FROM taxi_zones zpu
		WHERE zpu."Zone" IN ('Central Park'))
GROUP BY 1, 2 
ORDER BY "trip_count" DESC
    

-- Question 6
SELECT
    CONCAT(zpu."Zone", '/', zdo."Zone") AS "matched_zones",
    AVG(t."total_amount") AS "total_amount_average"
FROM yellow_taxi_trips t 
    JOIN taxi_zones zpu ON t."PULocationID" = zpu."LocationID"
    JOIN taxi_zones zdo ON t."DOLocationID" = zdo."LocationID"
GROUP BY 1
ORDER BY 2 DESC