CREATE DATABASE HOTEL_DB;

CREATE OR REPLACE FILE FORMAT FF_CSV
    TYPE = 'CSV'
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    SKIP_HEADER = 1
    NULL_IF = ('NULL', 'null', '')

CREATE OR REPLACE STAGE STG_HOTEL_BOOKINGS
    FILE_FORMAT = FF_CSV;

CREATE TABLE BRONZE_HOTEL_BOOKINGS (
    booking_id STRING,
    hotel_id STRING,
    hotel_city STRING,
    customer_id STRING,
    customer_name STRING,
    customer_email STRING,
    check_in_date STRING,
    check_out_date STRING,
    room_type STRING,
    num_guests STRING,
    total_amount STRING,
    currency STRING,
    booking_status STRING
)

COPY INTO BRONZE_HOTEL_BOOKINGS
FROM @STG_HOTEL_BOOKINGS
FILE_FORMAT = (FORMAT_NAME = FF_CSV)
ON_ERROR = 'CONTINUE';

CREATE TABLE SILVER_HOTEL_BOOKINGS (
    booking_id VARCHAR,
    hotel_id VARCHAR,
    hotel_city VARCHAR,
    customer_id VARCHAR,
    customer_name VARCHAR,
    customer_email VARCHAR,
    check_in_date DATE,
    check_out_date DATE,
    room_type VARCHAR,
    num_guests INTEGER,
    total_amount FLOAT,
    currency VARCHAR,
    booking_status VARCHAR
    
);

INSERT INTO SILVER_HOTEL_BOOKINGS
SELECT
    booking_id,
    hotel_id,
    INITCAP(TRIM(hotel_city)) AS hotel_city, //Captalized the City names
    customer_id,
    INITCAP(TRIM(customer_name)) AS customer_name, //Captalized the customer names and trimmed spaces
    CASE
        WHEN customer_email LIKE '%@%.%' THEN LOWER(TRIM(customer_email))
        ELSE NULL
    END AS customer_email, //Removed the invalid emails
    TRY_TO_DATE(NULLIF(check_in_date, '')) AS check_in_date, //Changed the data type to date
    TRY_TO_DATE(NULLIF(check_out_date, '')) AS check_out_date, //Changed the data type to date
    room_type,
    num_guests,
    ABS(TRY_TO_NUMBER(total_amount)) AS total_amount, //Changed the amounts that were in negative
    currency,
    CASE
        WHEN booking_status='Confirmeeed' THEN 'Confirmed'
        ELSE booking_status
    END AS booking_status // Corrected the spellings
    FROM BRONZE_HOTEL_BOOKINGS
    WHERE TRY_TO_DATE(check_in_date) IS NOT NULL
    AND TRY_TO_DATE(check_out_date) IS NOT NULL
    AND TRY_TO_DATE(check_out_date) >= TRY_TO_DATE(check_in_date); //Removed the rows with check_out_dates lesser than check_in_date

CREATE TABLE GOLD_HOTELBOOKINGS AS
SELECT *, 
    CASE WHEN CURRENCY='INR' THEN ROUND(TOTAL_AMOUNT/83,1)
    WHEN CURRENCY='EUR' THEN TOTAL_AMOUNT*1.1
    ELSE TOTAL_AMOUNT
    END AS REVENUE_USD
FROM SILVER_HOTEL_BOOKINGS;

ALTER TABLE GOLD_HOTELBOOKINGS DROP COLUMN TOTAL_AMOUNT, CURRENCY;


