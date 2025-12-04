import pandas as pd
import numpy as np

df = pd.read_csv('netflix_large_clean.csv')

#Seperate
movies = df[df["type"] == "Movie"].copy()
TvShows = df[df["type"] == "TV Show"].copy()




#1. Covert Duration to numeric
movies['duration_min']=movies['duration'].str.replace('min','').astype(int)
TvShows['seasons']=TvShows['duration'].str.replace('Season','').str.replace('s', '').astype(int)
print(movies)
print(TvShows)

#2. Step by step split genre into column
df['genre_list'] = df['listed_in'].str.split(', ')
genres = df.explode('genre_list')
genres = genres.rename(columns={'genre_list':'genre'})
#print(genres)

#3. Count
genres['genre'].value_counts()
print(genres)




# 4. Average duration of movies by genre

# First, we need to create a dataframe with movies and their genres
movies_with_genre = movies.copy()
movies_with_genre['genre_list'] = movies_with_genre['listed_in'].str.split(', ')

# Explode the genre list to have one row per movie-genre combination
movies_by_genre = movies_with_genre.explode('genre_list')
movies_by_genre = movies_by_genre.rename(columns={'genre_list': 'genre'})

# Calculate the average duration by genre
avg_duration_by_genre = movies_by_genre.groupby('genre')['duration_min'].mean().sort_values(ascending=False)

print("\nAverage Duration of Movies by Genre:")
print(avg_duration_by_genre)


#5. Average number of seasons by genre (TV shows)

# First, we need to create a dataframe with TV shows and their genres
tvshows_with_genre = TvShows.copy()
tvshows_with_genre['genre_list'] = tvshows_with_genre['listed_in'].str.split(', ')

# Explode the genre list to have one row per show-genre combination
tvshows_by_genre = tvshows_with_genre.explode('genre_list')
tvshows_by_genre = tvshows_by_genre.rename(columns={'genre_list': 'genre'})

# Calculate the average seasons by genre
avg_seasons_by_genre = tvshows_by_genre.groupby('genre')['seasons'].mean().sort_values(ascending=False)

print("\nAverage Number of Seasons by Genre (TV Shows):")
print(avg_seasons_by_genre)


#6. Simple visualization

import matplotlib.pyplot as plt

# Top genres
genres['genre'].value_counts().head(10).plot(kind='bar')
plt.show()

# Movie duration distribution
movies['duration_min'].plot(kind='hist', bins=20, title="Movie Duration")
plt.show()


