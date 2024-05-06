# SQLAlchemy Challenge
From Module 10: Advanced SQL from the Data Analytics Boot Camp by Monash University and EdX.

By implementing skills learnt throughout the module, an attempt at the challenge has been submitted here.

## Contents
Resources
- `hawaii.sqlite` file
- 2 `.csv` files

SurfsUp
- `app.py` file
- `climate_starter.ipynb` file

## Explanation
### Part 1: Analyse and Explore Climate Data
#### Precipitation Analysis
Precipitation data from the last 12 months of the data was queried. The resulting data was added to a `Pandas DataFrame` and plotted using the Pandas `plot` function. The `.describe()` function was used to calculate the summary and statistics for the resulting data. 

#### Station Analysis
The number of stations was queried and the most active station **(USC00519281)** was found using the `.count` function. Using this station ID, the minimum, maximum, and average temperature for the last 12 months was found **(12.2, 29.4, 22.04 respectively)**. Temperature data for the last 12 months was also found using two filters to get data from the last 12 months only for the most active station. A histogram was plotted to show temperature frequency.

### Part 2: Design Your Climate App
Routes for `/api/v1.0/precipitation`, `/api/v1.0/stations`, and `/api/v1.0/tobs` were created by taking the query in the `.ipynb` file and adding the results to a list. `jsonify` was not used because the results were returned in `JSON` formatting automatically.

The API dynamic routes were completed by implementing the `start` and `end` as variables into the paramaters.

## Credits
Credits to my friend, NT, who helped with the following:
- `.julianday`
- `.scalar_subquery()`
- Advised to create the function in `app.py` as it was used twice (prevents repetition)
- Some formatting advice to make the code look neater visually

All resources were given.