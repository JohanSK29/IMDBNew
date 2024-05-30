DROP TABLE IF EXISTS Movies CASCADE;

CREATE TABLE IF NOT EXISTS Movies(
    pk serial unique not null PRIMARY KEY,
    category varchar(30),
    item varchar(30),
    variety varchar(30),
    unit varchar(10),
    price float
);

DELETE FROM Movies;

CREATE INDEX IF NOT EXISTS Movies_index
ON Movies (category, item, variety);

DROP TABLE IF EXISTS Sell;

CREATE TABLE IF NOT EXISTS Sell(
    farmer_pk int not null REFERENCES Farmers(pk) ON DELETE CASCADE,
    Movies_pk int not null REFERENCES Movies(pk) ON DELETE CASCADE,
    available boolean default true,
    PRIMARY KEY (farmer_pk, Movies_pk)
);

CREATE INDEX IF NOT EXISTS sell_index
ON Sell (farmer_pk, available);

DELETE FROM Sell;

DROP TABLE IF EXISTS MoviesOrder;

CREATE TABLE IF NOT EXISTS MoviesOrder(
    pk serial not null PRIMARY KEY,
    customer_pk int not null REFERENCES Customers(pk) ON DELETE CASCADE,
    farmer_pk int not null REFERENCES Farmers(pk) ON DELETE CASCADE,
    Movies_pk int not null REFERENCES Movies(pk) ON DELETE CASCADE,
    created_at timestamp not null default current_timestamp
);

DELETE FROM MoviesOrder;

CREATE OR REPLACE VIEW vw_produce
AS
SELECT p.category, p.item, p.variety,
       p.unit, p.price, s.available,
       p.pk as produce_pk,
       f.full_name as farmer_name,
       f.pk as farmer_pk
FROM Produce p
JOIN Sell s ON s.produce_pk = p.pk
JOIN Farmers f ON s.farmer_pk = f.pk
ORDER BY available, p.pk;