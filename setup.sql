-- Setup script for RetailPriceOptimizer database tables

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Users')
BEGIN
    CREATE TABLE Users (
        UserID INT IDENTITY(1,1) PRIMARY KEY,
        FullName NVARCHAR(100) NOT NULL,
        Username NVARCHAR(50) UNIQUE NOT NULL,
        PasswordHash NVARCHAR(255) NOT NULL,
        CreatedAt DATETIME NOT NULL DEFAULT GETDATE()
    );
END;

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Products')
BEGIN
    CREATE TABLE Products (
        ProductID INT IDENTITY(1,1) PRIMARY KEY,
        ProductName NVARCHAR(150) UNIQUE NOT NULL,
        Category NVARCHAR(50) NOT NULL,
        CostPrice DECIMAL(18,2) NOT NULL CHECK (CostPrice >= 0),
        SellingPrice DECIMAL(18,2) NOT NULL CHECK (SellingPrice >= 0),
        CompetitorPrice DECIMAL(18,2) NOT NULL CHECK (CompetitorPrice >= 0),
        QuantitySold INT NOT NULL DEFAULT 0 CHECK (QuantitySold >= 0)
    );
    CREATE INDEX IX_Products_Category ON Products(Category);
END;

IF NOT EXISTS (SELECT * FROM sys.tables WHERE name = 'Predictions')
BEGIN
    CREATE TABLE Predictions (
        PredictionID INT IDENTITY(1,1) PRIMARY KEY,
        ProductID INT NOT NULL FOREIGN KEY REFERENCES Products(ProductID) ON DELETE CASCADE,
        CurrentPrice DECIMAL(18,2) NOT NULL CHECK (CurrentPrice >= 0),
        RecommendedPrice DECIMAL(18,2) NOT NULL CHECK (RecommendedPrice >= 0),
        ExpectedDemand INT NOT NULL CHECK (ExpectedDemand >= 0),
        ExpectedRevenue DECIMAL(18,2) NOT NULL CHECK (ExpectedRevenue >= 0),
        ExpectedProfit DECIMAL(18,2) NOT NULL CHECK (ExpectedProfit >= 0),
        PredictionDate DATETIME NOT NULL DEFAULT GETDATE()
    );
    CREATE INDEX IX_Predictions_ProductID ON Predictions(ProductID);
END;
