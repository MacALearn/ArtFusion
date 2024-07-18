-- Create Categories table
CREATE TABLE Categories (
    CategoryID INT IDENTITY(1,1) PRIMARY KEY,
    CategoryName VARCHAR(50) UNIQUE NOT NULL
);

-- Insert static categories into the Categories table
INSERT INTO Categories (CategoryName)
VALUES
    ('Academic_Art'),
    ('Art_Nouveau'),
    ('Japanese_Art'),
    ('Primitivism'),
    ('Realism'),
    ('Symbolism'),
    ('Western_Medieval'),
    ('Other');

-- Create Images table
CREATE TABLE Images (
    ImageID INT IDENTITY(1,1) PRIMARY KEY,
    ImagePath VARCHAR(255) NOT NULL
);

-- Create LinkImageCategory table
CREATE TABLE LinkImageCategory (
    ImageID INT NOT NULL,
    CategoryID INT NOT NULL,
    FOREIGN KEY (ImageID) REFERENCES Images(ImageID),
    FOREIGN KEY (CategoryID) REFERENCES Categories(CategoryID)
);

-- Create DominantColors table
CREATE TABLE DominantColors (
    ColorID INT IDENTITY(1,1) PRIMARY KEY,
    Red INT NOT NULL,
    Green INT NOT NULL,
    Blue INT NOT NULL
);

-- Create LinkImageColor table
CREATE TABLE LinkImageColor (
    ImageID INT NOT NULL,
    ColorID INT NOT NULL,
    FOREIGN KEY (ImageID) REFERENCES Images(ImageID),
    FOREIGN KEY (ColorID) REFERENCES DominantColors(ColorID)
);
