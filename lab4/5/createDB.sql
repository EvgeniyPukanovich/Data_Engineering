CREATE TABLE IF NOT EXISTS Countries (
    country TEXT PRIMARY KEY,
    cpi_country REAL,
    cpi_change_country REAL,
    gdp_country REAL,
    gross_tertiary_education_enrollment REAL,
    gross_primary_education_enrollment_country REAL,
    life_expectancy_country REAL,
    tax_revenue_country_country REAL,
    total_tax_rate_country REAL,
    population_country INTEGER,
    latitude_country REAL,
    longitude_country REAL
);

CREATE TABLE IF NOT EXISTS Companies (
    name TEXT PRIMARY KEY,
    rank INTEGER,
    headquarter TEXT,
    ceo TEXT,
    market_capitalization REAL,
    total_employees INTEGER,
    sectors TEXT,
    url TEXT
)

CREATE TABLE IF NOT EXISTS Billionaires (
    rank INTEGER PRIMARY KEY,
    finalWorth REAL,
    category TEXT,
    personName TEXT,
    age INTEGER,
    country TEXT,
    city TEXT,
    source TEXT,
    industries TEXT,
    countryOfCitizenship TEXT,
    organization TEXT,
    selfMade INTEGER,
    status TEXT,
    gender TEXT,
    birthDate TEXT,
    lastName TEXT,
    firstName TEXT,
    title TEXT,
    date TEXT,
    state TEXT,
    residenceStateRegion TEXT,
    birthYear INTEGER,
    birthMonth INTEGER,
    birthDay INTEGER,
    cpi_country REAL,
    FOREIGN KEY (country) REFERENCES Countries(country),
    FOREIGN KEY (source) REFERENCES Companies(name)
)