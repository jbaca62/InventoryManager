-- Create a new table called 'Cards' in schema 'dbo' // Change name to Products in Production, change db name to jbtradingcards
-- Drop the table if it already exists
-- IF OBJECT_ID('dbo.Cards', 'U') IS NOT NULL
-- DROP TABLE dbo.Cards
-- GO
-- Create the table in the specified schema
CREATE TABLE Cards
(
   CardId        INT    NOT NULL  IDENTITY PRIMARY KEY, -- primary key column
   CardName      VARCHAR(50)  NOT NULL,
   CardTag  VARCHAR(50)  NOT NULL,
   Box  VARCHAR(50)  NOT NULL,
   Rarity VARCHAR(50) NOT NULL,
   PriceLow DECIMAL(18,2)  NOT NULL,
   PriceAvg DECIMAL(18,2)  NOT NULL,
   PriceHigh DECIMAL(18,2)  NOT NULL,
   Quantity INT  NOT NULL,
   Location VARCHAR(50)  NOT NULL,
   Description     VARCHAR(512)  NOT NULL,
   ImageURL    VARCHAR(512)  NOT NULL,
   Listings VARCHAR(50) NOT NULL
);
GO