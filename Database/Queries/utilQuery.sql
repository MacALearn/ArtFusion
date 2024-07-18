

--CREATION

-- Create Categories table
CREATE TABLE Categories (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName VARCHAR(50) UNIQUE
);



-- Insert static categories into the Categories table
INSERT INTO Categories (CategoryName)
VALUES 
    ( 'Academic_Art'),
    ( 'Art_Nouveau'),
    ( 'Japanese_Art'),
    ( 'Primitivism'),
    ( 'Realism'),
    ( 'Symbolism'),
    ( 'Western_Medieval');


-- Create Images table
CREATE TABLE Images (
    ImageID INT IDENTITY(1,1) PRIMARY KEY,
    ImagePath VARCHAR(255),
);

-- Create LinkImageToCategory table
CREATE TABLE LinkImageCategory (
    ImageID INT,
    CategoryID INT,
    FOREIGN KEY (ImageID) REFERENCES Images(ImageID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- Create DominantColors table
CREATE TABLE DominantColors (
    ColorID  INT IDENTITY(1,1) PRIMARY KEY,
    Red INT,
	Green INT,
	Blue INT
);

-- Create ImageLinkForDominantColor table
CREATE TABLE LinkImageColor (
    ImageID INT,
    ColorID INT,
    FOREIGN KEY (ImageID) REFERENCES Images(ImageID),
    FOREIGN KEY (ColorID) REFERENCES DominantColors(ColorID)
);
