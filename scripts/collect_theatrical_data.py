"""
Theatrical Release Data Collection
Purpose: Pull 500-1000 movies from TMDb API (2019-2024) with budget/revenue data
Author: Alexandra Lugo
Date: January 2026
"""

import requests
import os
from dotenv import load_dotenv
import pandas as pd
import time
from datetime import datetime
from pathlib import Path

#load env variables
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(dotenv_path=env_path)

TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = os.getenv('TMDB_BASE_URL')

#API rate limiting (TMDb allows 40 requests per 10 seconds)
REQUEST_DELAY = 0.26  # ~3.8 requests/second = safe buffer


class TMDbCollector:
    """Handles TMDb API data collection with rate limiting"""
    
    def __init__(self, api_key, base_url):
        self.api_key = api_key
        self.base_url = base_url
        self.genres_dict = {}  #will store genre_id: genre_name mapping
        
    def get_genres(self):
        """Fetch and store genre mappings"""
        url = f"{self.base_url}/genre/movie/list"
        params = {'api_key': self.api_key, 'language': 'en-US'}
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            genres = response.json()['genres']
            
            #create dict mapping
            self.genres_dict = {g['id']: g['name'] for g in genres}
            print(f"✅ Loaded {len(self.genres_dict)} genres")
            return self.genres_dict
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching genres: {e}")
            return {}
    
    def discover_movies(self, year, page=1):
        """
        Discover movies for a specific year using TMDb's discover endpoint
        This gives us more control than just popular movies
        """
        url = f"{self.base_url}/discover/movie"
        params = {
            'api_key': self.api_key,
            'language': 'en-US',
            'sort_by': 'revenue.desc',  #sort by revenue to get theatrical releases
            'primary_release_year': year,
            'page': page,
            'with_original_language': 'en',  #focus on English-language films
            'with_release_type': 3  # 3 = Theatrical release
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            time.sleep(REQUEST_DELAY)  #rate limiting
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error discovering movies for {year}, page {page}: {e}")
            return None
    
    def get_movie_details(self, movie_id):
        """
        Fetch detailed information for a specific movie
        This includes budget and revenue which we need for ROI analysis
        """
        url = f"{self.base_url}/movie/{movie_id}"
        params = {
            'api_key': self.api_key,
            'language': 'en-US'
        }
        
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            time.sleep(REQUEST_DELAY)  #rate limiting
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error fetching details for movie {movie_id}: {e}")
            return None
    
    def collect_year_data(self, year, max_pages=5):
        """
        Collect movies for a specific year
        max_pages: Number of pages to fetch (20 movies per page)
        """
        print(f"\n{'='*60}")
        print(f"Collecting data for {year}")
        print(f"{'='*60}")
        
        movies_data = []
        
        for page in range(1, max_pages + 1):
            print(f"  Fetching page {page}/{max_pages}...", end=" ")
            
            #get basic movie list
            discover_results = self.discover_movies(year, page)
            
            if not discover_results or 'results' not in discover_results:
                print("❌ No results")
                break
            
            movies = discover_results['results']
            print(f"✅ Found {len(movies)} movies")
            
            #for each movie, get detailed info (budget/revenue)
            for movie in movies:
                movie_id = movie['id']
                details = self.get_movie_details(movie_id)
                
                if details:
                    #extract the data we need
                    movie_data = {
                        'movie_id': movie_id,
                        'title': details.get('title'),
                        'release_date': details.get('release_date'),
                        'budget': details.get('budget', 0),
                        'revenue': details.get('revenue', 0),
                        'runtime': details.get('runtime'),
                        'vote_average': details.get('vote_average'),
                        'vote_count': details.get('vote_count'),
                        'popularity': details.get('popularity'),
                        'original_language': details.get('original_language'),
                        #get primary genre (first one listed)
                        'genre_ids': [g['id'] for g in details.get('genres', [])],
                        'genres': [g['name'] for g in details.get('genres', [])],
                        'primary_genre': details.get('genres', [{}])[0].get('name') if details.get('genres') else None,
                        #production info
                        'production_companies': [c['name'] for c in details.get('production_companies', [])[:3]],  # Top 3
                        'production_countries': [c['iso_3166_1'] for c in details.get('production_countries', [])],
                        #status
                        'status': details.get('status'),
                        'tagline': details.get('tagline'),
                    }
                    
                    movies_data.append(movie_data)
                    
                    #progress indicator
                    if len(movies_data) % 10 == 0:
                        print(f"    Collected {len(movies_data)} movies so far...")
            
            #check if we've hit the last page
            if page >= discover_results.get('total_pages', 0):
                break
        
        print(f"\n✅ Year {year} complete: {len(movies_data)} movies collected")
        return movies_data


def main():
    """Main data collection workflow"""
    
    print("="*60)
    print("TMDb Theatrical Release Data Collection (2019-2024)")
    print("="*60)
    
    #initialize collector
    collector = TMDbCollector(TMDB_API_KEY, TMDB_BASE_URL)

    #load genre mappings
    print("\n📚 Loading genre mappings...")
    collector.get_genres()

    #define years and how many pages per year
    #5 pages = ~100 movies per year = ~600 total movies
    #adjust max_pages if you want more/fewer movies
    years = [2019, 2020, 2021, 2022, 2023, 2024]
    max_pages_per_year = 5 #adjust this (1 page = ~20 movies)

    print(f"\n🎬 Target: ~{len(years) * max_pages_per_year * 20} movies")
    print(f"Years: {years}")
    print(f"Pages per year: {max_pages_per_year}")

    #collect data for all years
    all_movies = []

    start_time = time.time()

    for year in years:
        year_movies = collector.collect_year_data(year, max_pages=max_pages_per_year)
        all_movies.extend(year_movies)

    elapsed_time = time.time() - start_time

    #convert to df
    print(f"\n{'='*60}")
    print("Processing collected data...")
    print(f"{'='*60}")

    df = pd.DataFrame(all_movies)

    #basic data cleaning
    print(f"\nRaw data shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")

    #remove movies with no budget or revenue data
    df_filtered = df[(df['budget'] > 0) & (df['revenue'] > 0)].copy()

    print(f"\nFiltered data shape (budget & revenue > 0): {df_filtered.shape}")
    print(f"Removed{len(df) - len(df_filtered)} movies with missing financial data")

    #calculate roi
    df_filtered['roi'] = ((df_filtered['revenue'] - df_filtered['budget']) / df_filtered['budget']) * 100

    #add profit/loss
    df_filtered['profit'] = df_filtered['revenue'] - df_filtered['budget']

    #add yr column
    df_filtered['release_year'] = pd.to_datetime(df_filtered['release_date']).dt.year

    # Quick summary statistics
    print(f"\n{'='*60}")
    print("Data Summary")
    print(f"{'='*60}")
    print(f"Total movies collected: {len(df_filtered)}")
    print(f"\nMovies per year:")
    print(df_filtered['release_year'].value_counts().sort_index())
    print(f"\nTop 5 genres:")
    print(df_filtered['primary_genre'].value_counts().head())
    print(f"\nBudget range: ${df_filtered['budget'].min():,.0f} - ${df_filtered['budget'].max():,.0f}")
    print(f"Revenue range: ${df_filtered['revenue'].min():,.0f} - ${df_filtered['revenue'].max():,.0f}")
    print(f"ROI range: {df_filtered['roi'].min():.1f}% - {df_filtered['roi'].max():.1f}%")
    print(f"Average ROI: {df_filtered['roi'].mean():.1f}%")
    
    # Save to CSV
    output_dir = project_root / 'data' / 'raw'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    output_file = output_dir / 'theatrical_data_raw.csv'
    df_filtered.to_csv(output_file, index=False)
    
    print(f"\n✅ Data saved to: {output_file}")
    print(f"\n⏱️  Total collection time: {elapsed_time/60:.1f} minutes")
    print(f"📊 Ready for data cleaning (Day 5)!")
    
    # Display sample rows
    print(f"\n{'='*60}")
    print("Sample Data (First 3 Movies)")
    print(f"{'='*60}")
    print(df_filtered[['title', 'release_year', 'primary_genre', 'budget', 'revenue', 'roi']].head(3).to_string())


if __name__ == "__main__":
    main()