--- Création de la base
CREATE DATABASE beautyanalytics;

\c beautyanalytics

CREATE TABLE brands (
    brand_id SERIAL PRIMARY KEY,
    brand_name TEXT NOT NULL
)

CREATE TABLE category (
    category_id SERIAL PRIMARY KEY,
    category_name TEXT NOT NULL
)

-- id,brand,category,name,size,rating,number_of_reviews,love,price,value_price,URL,MarketingFlags,MarketingFlags_content,options,details,how_to_use,ingredients,online_only,exclusive,limited_edition,limited_time_offer
--- Table produits
CREATE TABLE products (
    product_id SERIAL PRIMARY KEY,
    product_name TEXT NOT NULL,
    category_id INT REFERENCES category(category_id),
    price FLOAT,
    rating FLOAT,
    love
);

-- "total_neg_feedback_count","price_usd","is_recommended","total_pos_feedback_count","submission_time","skin_tone","eye_color","skin_type","hair_color","product_name","brand_name"
--- Table reviews
CREATE TABLE reviews (
    review_id SERIAL PRIMARY KEY,
    product_id  INT REFERENCES products(product_id),
    brand_id    INT REFERENCES brands(brand_id),
    review_date DATE, -- submission time
    total_neg_feedback_count INT,
    total_pos_feedback_count INT,
    price_usd FLOAT,
    is_recommended BOOLEAN
);

--- Table metadata
CREATE TABLE metadata (
    metadata_id SERIAL PRIMARY KEY,
    dataset_name TEXT NOT NULL,
    filename TEXT,
    source TEXT,
    nb_rows INT,
    ingestion_date TIMESTAMP
);
