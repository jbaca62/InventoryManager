-- Create a new table called 'Cards' in schema 'dbo' // Change name to Products in Production, change db name to jbtradingcards
-- Drop the table if it already exists
IF OBJECT_ID('dbo.Locations', 'U') IS NOT NULL
DROP TABLE dbo.Locations
GO
-- Create the table in the specified schema
CREATE TABLE dbo.Locations
(
   LocationId        INT    NOT NULL  IDENTITY PRIMARY KEY, -- primary key column
   LocationName VARCHAR(50),
   CardId int FOREIGN KEY REFERENCES Cards(CardId),
);
GO