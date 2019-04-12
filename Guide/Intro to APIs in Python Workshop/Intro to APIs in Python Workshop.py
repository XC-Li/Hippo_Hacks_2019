# Intro to APIs in Python Workshop
# h/t to @josephofiowa

# We will be using the OMDb Open Movie Database here: http://www.omdbapi.com/

# First, we will import the necessary libraries.
# Pandas is a common python library for data analysis. 
# Requests is the main python library used for making API requests. 
# Time is a library that allows us to pause between API calls to avoid getting rate limited

import pandas as pd
import requests
from time import sleep

# Read IMDb data into a DataFrame: we want a year column!
movies = pd.read_csv('https://raw.githubusercontent.com/josephnelson93/GWDATA/master/imdb_1000.csv')
movies.head()

# Use requests library to interact with a URL
r = requests.get('http://www.omdbapi.com/?apikey=f4e95a92&t=the+shawshank+redemption&r=json&type=movie')

# Check the status: 200 means success, 4xx means error
r.status_code

# View the raw response text
r.text

# Decode the JSON response body into a dictionary
r.json()

# Extracting the year from the dictionary
r.json()['Year']


# What happens if the movie name is not recognized?
r = requests.get('http://www.omdbapi.com/?apikey=f4e95a92&t=blahblahblah&r=json&type=movie')
r.status_code
r.json()


# Define a function to return the year
def get_movie_year(title):
    r = requests.get('http://www.omdbapi.com/?apikey=f4e95a92&t=' + title + '&r=json&type=movie')
    info = r.json()
    if info['Response'] == 'True':
        return int(info['Year'])
    else:
        return None


# Test the function
get_movie_year('The Shawshank Redemption')

get_movie_year('blahblahblah')


# Create a smaller DataFrame for testing
top_movies = movies.head().copy()


# Write a for loop to build a list of years
years = []
for title in top_movies.title:
    years.append(get_movie_year(title))
    sleep(1)


# Check that the DataFrame and the list of years are the same length
assert(len(top_movies) == len(years))


# Save that list as a new column
top_movies['year'] = years

print(top_movies)