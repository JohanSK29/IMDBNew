DROP TABLE IF EXISTS Movies CASCADE;


CREATE TABLE IF NOT EXISTS Movies(
    pk serial unique not null PRIMARY KEY,
    Genre varchar(50),
    Moviename varchar(255),
    Mainactor varchar(100),
    Summary TEXT,
    ReleaseDate DATE,
    BrainRotScore FLOAT
);


CREATE OR REPLACE VIEW vw_produce
AS
SELECT p.Genre,p.Moviename, p.MainActor, p.Summary,
       p.ReleaseDate, p.BrainRotScore
FROM Movies p